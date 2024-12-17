function $(id) { return document.getElementById(id); }

//window.onresize = function(){ location.reload(); }
document.addEventListener('DOMContentLoaded', function() {
    let bookText = document.getElementById('book-text');
    bookText.setAttribute('data-lines', getLineTotal(bookText));
    bookText.setAttribute('data-char-limit', calculateCharacterLimit(bookText));
    let progress = document.getElementById('page-number').getAttribute('data-progress')
    console.log("PROGRESS: " + progress);
    setPageContentByProgress(progress)
}, false);

$('next-button').addEventListener('click', function() {
    bookmarkReady();
    pageNumberElement = document.getElementById('page-number')
    setPageByTurns(1);
})

$('previous-button').addEventListener('click', function() {
    bookmarkReady();
    pageNumberElement = document.getElementById('page-number')
    setPageByTurns(-1);
})

document.querySelector('#bookmark').addEventListener('click', async function() {
    bookmarkDone();
    try {
        await updateProgress(this.getAttribute('data-progress'), this.getAttribute('data-length'));
    } catch {
        alert('Sorry, there was an issue bookmarking this page.');
    }
})

function bookmarkDone() {
    let bookmark = document.querySelector('#bookmark')
    bookmark.innerHTML = 'Bookmarked<i class="fa-solid fa-bookmark fa-lg ml-2"></i>';
    bookmark.classList.remove('btn-warning');
    bookmark.classList.add('btn-success');
    bookmark.classList.add('disabled');
}

function bookmarkReady() {
    let bookmark = document.querySelector('#bookmark')
    bookmark.innerHTML = 'Bookmark Page<i class="fa-regular fa-bookmark fa-lg ml-2"></i>';
    bookmark.classList.add('btn-warning');
    bookmark.classList.remove('btn-success');
    bookmark.classList.remove('disabled');
}

/**
 * Return a boolean to indicate whether a paragraph element's text is larger
 * than its viewport.
 * @param {Element} el The element for which the text should be evaluated.
 * @returns {boolean} Whether or not the text is larger. 'true' if it is
 * larger, 'false' if it is not.
 */
function isOver(el) {
    return el.scrollHeight > el.offsetHeight;
}

/**
 * Return the total number of lines that can fit vertically
 * in a paragraph element.
 * @param  {Element} el the element for which the number of lines should
 * be counted.
 * @return {integer} The number of lines counted.
 */
function getLineTotal(el) {
    let originalContent = el.innerText;
    el.innerText = "";
    let i = 0;
    while (!isOver(el)) {
      i++;
      el.innerText += `\n`;
    }
    el.innerText = originalContent;
    return i - 1;
}

/**
 * Return the total number of characters that can fit horizontally
 * in one line of a paragraph element.
 * @param  {Element} el the element for which the number of characters
 * should be counted.
 * @return {integer} The number of characters counted.
 */
function calculateCharacterLimit(el) {
    let originalContent = el.innerText;
    el.innerHTML = '<span class="charcount">#</span>'.repeat(150);
    let allSpans = document.getElementsByClassName('charcount');
    let prevSpan;
    let i = 0;
    for (let span of allSpans) {
        i++;
        if (typeof prevSpan != undefined && parseInt(span.offsetTop) > prevSpan) {
            el.innerText = originalContent;
            return i - 1;
        }
        prevSpan = parseInt(span.offsetTop);
    }
    return 0;
}

function setPageContentByProgress(progress) {
    let bookText = document.getElementById('book-text');
    let lines = parseInt(bookText.getAttribute('data-lines'));
    let characters = parseInt(bookText.getAttribute('data-char-limit'));
    getBook(characters).then((text_list) => {
        let bookInPages = splitIntoNumberedPages(text_list, lines);
        let pageNumber;
        for (const [i, page] of bookInPages.entries()) {
            if ((Number(progress) < page.num)) {
                pageNumber = i-1;
                break
            }
        }
        setPageNumbers(pageNumber, bookInPages.length);
        setPageContent(bookInPages, 0);
    })
}

function setPageByTurns(turns){
    let bookText = document.getElementById('book-text');
    let lines = parseInt(bookText.getAttribute('data-lines'));
    let characters = parseInt(bookText.getAttribute('data-char-limit'));
    getBook(characters).then((text_list) => {
        let bookInPages = splitIntoNumberedPages(text_list, lines);
        document.querySelector('#bookmark').setAttribute('data-length', text_list.length);
        setPageContent(bookInPages, turns);
    });
}

function setPageContent(bookInPages, turns) {
    let pageNumberElement = document.querySelector('#page-number');
    let pageNumber = pageNumberElement.getAttribute('data-page-number');
    pageNumber = Number(pageNumber)+Number(turns);
    let page = bookInPages[pageNumber];
    renderPage(page.content);
    setPageNumbers(pageNumber, bookInPages.length);
    document.querySelector('#bookmark').setAttribute('data-progress', page.num);
}

function renderPage(page) {
    let content = "";
    for (let line of page) {
        content += line += "<br>";
    }
    document.getElementById('book-text').innerHTML = content;
}

function splitIntoNumberedPages(book, pageSize) {
    let numberedPages = [];
    splitIntoPages(book, pageSize).forEach((page) => {
        for (let line of page) {
            if (hasNumLabel(line)) {
                let [num, text] = getNumAndText(line);
                numberedPages.push({
                    "num": num,
                    "content": removeNumbers(page)
                });
                break;
            }
        }
    })
    return numberedPages;
}

function removeNumbers(text_list) {
    return text_list.map((line) => {
        if (hasNumLabel(line)) {
            return getNumAndText(line)[1];
        }
        return line;
    })
    
}

function splitIntoPages(book, pageSize) {
    let pages = [];
    for (let i = 0; i < book.length; i += pageSize) {
        pages.push(book.slice(i, i + pageSize));
    }
    return pages;
}

function hasNumLabel(line) {
    return line.includes("𓀴");
}

function getNumAndText(line) {
    let lines = line.split("𓀴");
    return [lines[0], lines[1]];
}

async function updateProgress(progress, length) {
    let bookText = document.getElementById('book-text')
    let url = bookText.getAttribute('data-ajax-update-url');
    let csrfToken = bookText.getAttribute('data-csrf-token');
    let bookID = bookText.getAttribute('data-book-id');
    const response = await fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrfToken,
        }, 
        body:JSON.stringify({
            'progress': progress,
            'book_id': bookID,
            'length': length,
            })
    });
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    let data = await response.json()
    if (!data['completion'].includes('Progress updated.')) {
        throw new Error(`Error updating progress: ${data['completion']}`);
    }
}

async function getBook(line_width, caching=true) {
    let bookText = document.getElementById('book-text')
    let bookID = bookText.getAttribute('data-book-id');
    if (sessionStorage.getItem("id") == bookID && 
    sessionStorage.getItem("line-width") == line_width && caching) {
        return JSON.parse(sessionStorage.getItem('text_list'));
    }
    let url = bookText.getAttribute('data-ajax-url');
    let csrfToken = bookText.getAttribute('data-csrf-token');
    const response = await fetch(url, {
       method:'POST',
       headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrfToken,
       }, 
       body:JSON.stringify({
        'num': line_width,
        'book_id': bookID,
        })
    })
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    let data = await response.json()
    sessionStorage.setItem("id", bookID);
    sessionStorage.setItem("line-width", line_width);
    sessionStorage.setItem("text_list", JSON.stringify(data));
    return data

}

function setPageNumbers(pageNumber, totalPages) {
    let pageNumberElement = document.querySelector('#page-number');
    pageNumberElement.innerHTML = `${pageNumber} of ${totalPages}`;
    pageNumberElement.setAttribute('data-page-number', pageNumber);
    document.querySelector('#next-button').style.visibility = pageNumber >= totalPages ?
    'hidden' : 'visible';
    document.querySelector('#previous-button').style.visibility = pageNumber <= 1 ?
    'hidden' : 'visible';
}
