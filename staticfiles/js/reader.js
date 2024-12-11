function $(id) { return document.getElementById(id); }

//window.onresize = function(){ location.reload(); }
document.addEventListener('DOMContentLoaded', function() {
    let bookText = document.getElementById('book-text');
    bookText.setAttribute('data-lines', getLineTotal(bookText));
    console.log(bookText.getAttribute('data-lines'))
    bookText.setAttribute('data-char-limit', calculateCharacterLimit(bookText));
    console.log(bookText.getAttribute('data-char-limit'))
    let pageNumber = document.getElementById('page-number').getAttribute('data-page-number')
    setPageContent(pageNumber)
}, false);

$('next-button').addEventListener('click', function() {
    pageNumberElement = document.getElementById('page-number')
    let pageNumber = parseInt(pageNumberElement.getAttribute('data-page-number'))
    pageNumberElement.setAttribute('data-page-number', pageNumber+1)
    setPageContent(pageNumber + 1, )
})

$('previous-button').addEventListener('click', function() {
    pageNumberElement = document.getElementById('page-number')
    let pageNumber = parseInt(pageNumberElement.getAttribute('data-page-number'))
    pageNumberElement.setAttribute('data-page-number', pageNumber-1)
    setPageContent(pageNumber - 1)
})

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
    el.innerHTML = '<span>#</span>'.repeat(150);
    let allSpans = document.getElementsByTagName('span');
    let prevSpan;
    let i = 0;
    for (let span of allSpans) {
        i++;
        console.log(span.offsetTop);
        if (typeof prevSpan != undefined && parseInt(span.offsetTop) > prevSpan) {
            el.innerText = originalContent;
            return i - 1;
        }
        prevSpan = parseInt(span.offsetTop);
    }
    return 0;
}
      

function setPageContent(pageNumber) {
    let bookText = document.getElementById('book-text');
    let lines = parseInt(bookText.getAttribute('data-lines'));
    let characters = parseInt(bookText.getAttribute('data-char-limit'));
    let content = "";
    let start = lines*(pageNumber-1);
    getBook(characters).then((text_list) => {
        let totalPages = Math.floor(text_list.length / lines) + 1;
        setPageNumbers(pageNumber, totalPages);
        let end = Math.min(text_list.length, start+lines);
        // console.log(
        //     "Here's the rundown:\n" +
        //     `Evaluated lines: ${lines} ` + "\n" +
        //     `Evaluated characters in one line: ${characters}` + "\n" +
        //     `Calculated starting line: ${start}` + `\n` +
        //     `Calculated ending line: ${end}`
        // );
        for (let line of text_list.slice(start, end)) {
            content += line += "<br>"
        }
        bookText.innerHTML = content
    })
}

async function getBook(line_width, caching=true) {
    let bookText = document.getElementById('book-text')
    bookID = bookText.getAttribute('data-book-id');
    if (sessionStorage.getItem("id") == bookID && 
    sessionStorage.getItem("line-width") == line_width && caching) {
        return JSON.parse(sessionStorage.getItem('text_list'));
    }
    url = bookText.getAttribute('data-ajax-url');
    csrfToken = bookText.getAttribute('data-csrf-token');
    console.log(url);
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
    $('page-number').innerHTML = `${pageNumber} of ${totalPages}`
    $('next-button').style.display = pageNumber >= totalPages ?
    'none' : 'inline';
    $('previous-button').style.display = pageNumber <= 1 ?
    'none' : 'inline';
}
