import { postProgressToServer, getBookFromServer } from './ajaxFunctions.js';
import { calculateCharacterLimit, getLineTotal} from './calculatePage.js';
import { getLastLineNumber } from './numbering.js';
import { setPageByTurns, setPageByProgress } from './setPage.js';
import { enableAllButtons, disableAllButtons, 
    makeSpinnerInvisible, makeSpinnerVisible } from './utility.js';

document.addEventListener('DOMContentLoaded', loadPage, false);
window.onresize = handleResize;

async function loadPage(e, progress="default", bookmarkClicked=true) {
    addReaderEventListeners();
    let bookText = document.getElementById('book-text');
    let chars = calculateCharacterLimit(bookText);
    bookText.setAttribute('data-char-limit', chars);
    bookText.setAttribute('data-lines', getLineTotal(bookText));
    let book = await getBookFromServer(chars);
    enableAllButtons();
    makeSpinnerInvisible();
    bookText.setAttribute('data-last-line-number', getLastLineNumber(book));
    if (progress == "default") {
        let pageNumberEl = document.getElementById('page-number');
        progress = parseInt(pageNumberEl.getAttribute('data-progress'));
    }
    if (Number(progress) > 0 && bookmarkClicked) {
        bookmarkDone();
    }
    setPageByProgress(progress)
}

function handleResize() {
    let pageNumberEl = document.getElementById('page-number');
    let progress = parseInt(pageNumberEl.getAttribute('data-progress'));
    let bookmark = document.querySelector('#bookmark');
    let clicked = true;
    if (bookmark.getAttribute('data-clicked') == 'false') {
        bookmarkReady();
        clicked = false;
    }
    loadPage(Event, progress, clicked);
    document.getElementById('book-text').innerText = "";
    disableAllButtons();
}

function addReaderEventListeners() {
    document.querySelector('#next-button').addEventListener('click', handleNextClick);
    document.querySelector('#previous-button').addEventListener('click', handlePreviousClick);
    document.querySelector('#bookmark').addEventListener('click', handleBookMarkClick);
}

async function handleNextClick() {
    let bookmark = document.querySelector('#bookmark');
    let startPage = Number(bookmark.getAttribute('data-bookmarked-page'));
    let currentPage = (await setPageByTurns(1)) + 1;
    if (startPage == currentPage) {
        bookmarkDone();
    } else {
        bookmarkReady();
    }
}

async function handlePreviousClick() {
    let bookmark = document.querySelector('#bookmark');
    let startPage = Number(bookmark.getAttribute('data-bookmarked-page'));
    let currentPage = (await setPageByTurns(-1)) + 1;
    if (startPage == currentPage && currentPage != 1) {
        bookmarkDone();
    } else {
        bookmarkReady();
    }
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
    }
}

function bookmarkDone() {
    let bookmark = document.querySelector('#bookmark')
    bookmark.innerHTML = 'Bookmarked<i class="fa-solid fa-bookmark fa-lg ml-2"></i>';
    bookmark.classList.remove('btn-warning');
    bookmark.classList.add('btn-success');
    bookmark.setAttribute('disabled', '');
    bookmark.setAttribute('data-clicked', 'true');
}



function bookmarkReady() {
    let bookmark = document.querySelector('#bookmark')
    bookmark.innerHTML = 'Bookmark Page<i class="fa-regular fa-bookmark fa-lg ml-2"></i>';
    bookmark.classList.add('btn-warning');
    bookmark.classList.remove('btn-success');
    bookmark.removeAttribute('disabled');
    bookmark.setAttribute('data-clicked', 'false');
}

async function updateProgress() {
    let bookText = document.querySelector('#book-text');
    let pageNumber = document.querySelector('#page-number');
    let progress = pageNumber.getAttribute('data-progress');
    let length = bookText.getAttribute('data-last-line-number');
    postProgressToServer(progress, length);
}