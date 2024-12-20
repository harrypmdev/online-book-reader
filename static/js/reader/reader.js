import { postProgressToServer, getBook } from './ajaxFunctions.js';
import { calculateCharacterLimit, getLineTotal} from './calculatePage.js';
import { setPageNumbers, renderPage } from './render.js';

function $(id) { return document.getElementById(id); }
window.onresize = async function() {
    let bookmark = document.querySelector('#bookmark');
    if (bookmark.getAttribute('data-clicked') == 'false') {
        await handleBookMarkClick();
    } else {
        updateProgress();
    }
    let pageNumberEl = document.getElementById('page-number');
    let progress = parseInt(pageNumberEl.getAttribute('data-progress'));
    console.log("Sending progress: " + progress);
    loadPage(progress=progress);
    alert("Refreshing or resizing the window may affect how we present your book. " +
        "Your page has been bookmarked so your progress is not affected."
    );
}

//window.onresize = function(){ location.reload(); }
document.addEventListener('DOMContentLoaded', loadPage, false);

function loadPage(e, progress="default") {
    let bookText = document.getElementById('book-text');
    bookText.setAttribute('data-lines', getLineTotal(bookText));
    bookText.setAttribute('data-char-limit', calculateCharacterLimit(bookText));
    if (progress == "default") {
        let pageNumberEl = document.getElementById('page-number');
        progress = parseInt(pageNumberEl.getAttribute('data-progress'));
    }
    if (Number(progress) > 0) {
        bookmarkDone();
    }
    console.log("PROGRESS: at time ot setPageContentByProgress: "+ progress);
    setPageContentByProgress(progress)
}

$('next-button').addEventListener('click', async function() {
    let bookmark = document.querySelector('#bookmark');
    let startPage = Number(bookmark.getAttribute('data-bookmarked-page'));
    let currentPage = (await setPageByTurns(1)) + 1;
    if (startPage != currentPage) {
        bookmarkReady();
    } else {
        bookmarkDone();
    }
})

$('previous-button').addEventListener('click', async function() {
    let bookmark = document.querySelector('#bookmark');
    let startPage = Number(bookmark.getAttribute('data-bookmarked-page'));
    let currentPage = (await setPageByTurns(-1)) + 1;
    if (startPage != currentPage) {
        bookmarkReady();
    } else {
        bookmarkDone();
    }
})

document.querySelector('#bookmark').addEventListener('click', handleBookMarkClick)

function bookmarkDone() {
    let bookmark = document.querySelector('#bookmark')
    bookmark.innerHTML = 'Bookmarked<i class="fa-solid fa-bookmark fa-lg ml-2"></i>';
    bookmark.classList.remove('btn-warning');
    bookmark.classList.add('btn-success');
    bookmark.setAttribute('disabled', '');
    bookmark.setAttribute('data-clicked', 'true');
}

async function handleBookMarkClick() {
    bookmarkDone();
    let pageNumberEl = document.querySelector('#page-number');
    let pageNumber = Number(pageNumberEl.getAttribute('data-page-number')) + 1;
    document.querySelector('#bookmark').setAttribute('data-bookmarked-page', pageNumber);
    try {
        await updateProgress();
    } catch(error) {
        alert('Sorry, there was an issue bookmarking this page.');
        console.log("Error: " + error.message);
    }
}

function bookmarkReady() {
    let bookmark = document.querySelector('#bookmark')
    bookmark.innerHTML = 'Bookmark Page<i class="fa-regular fa-bookmark fa-lg ml-2"></i>';
    bookmark.classList.add('btn-warning');
    bookmark.classList.remove('btn-success');
    bookmark.removeAttribute('disabled');
    bookmark.setAttribute('data-clicked', 'false');
}

async function getNumberedBook() {
    let book = await getBook();
    let bookText = document.querySelector('#book-text');
    let lines = parseInt(bookText.getAttribute('data-lines'));
    return splitIntoNumberedPages(book, lines);
}

async function setPageContentByProgress(progress) {
    let bookInPages = await getNumberedBook();
    let pageNumber = bookInPages.length - 1;
    for (const [i, page] of bookInPages.entries()) {
        if ((Number(progress) < page.num)) {
            pageNumber = i-1;
            break
        }
    }
    document.querySelector('#bookmark').setAttribute('data-bookmarked-page', pageNumber+1);
    setPageNumbers(pageNumber, bookInPages.length);
    setPageContent(bookInPages, 0);
}

async function setPageByTurns(turns){
    let bookText = document.getElementById('book-text');
    let lines = parseInt(bookText.getAttribute('data-lines'));
    let characters = parseInt(bookText.getAttribute('data-char-limit'));
    let text_list = await getBook(characters)
    let bookInPages = splitIntoNumberedPages(text_list, lines);
    document.querySelector('#bookmark').setAttribute('data-length', text_list.length);
    return setPageContent(bookInPages, turns);
}

function getLastLineNumber(book) {
    for (let line of book.reverse()) {
        if (hasNumLabel(line)) {
            return Number(getNumAndText(line)[0]);
        }
    }
}

function setPageContent(bookInPages, turns) {
    let pageNumberElement = document.querySelector('#page-number');
    let pageNumber = pageNumberElement.getAttribute('data-page-number');
    pageNumber = Number(pageNumber)+Number(turns);
    let page = bookInPages[pageNumber];
    renderPage(page.content);
    setPageNumbers(pageNumber, bookInPages.length);
    document.querySelector('#bookmark').setAttribute('data-progress', page.num);
    return pageNumber;
}

async function updateProgress() {
    let bookText = document.querySelector('#book-text');
    let chars = parseInt(bookText.getAttribute('data-char-limit'))
    let text_list = await getBook(chars);
    let bookmark = document.querySelector('#bookmark');
    let progress = bookmark.getAttribute('data-progress');
    let length = getLastLineNumber(text_list);
    if (bookmark.getAttribute('data-final-page') == 'true') {
        progress = length;
    }
    console.log("Length: " + length);
    console.log("Progress: " + progress);
    postProgressToServer(progress, length);
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
