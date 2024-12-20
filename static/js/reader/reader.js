import { postProgressToServer, getBookFromServer } from './ajaxFunctions.js';
import { calculateCharacterLimit, getLineTotal} from './calculatePage.js';
import { getLastLineNumber } from './numbering.js';
import { setPageByTurns, setPageByProgress } from './setPage.js';
import { enableAllButtons, disableAllButtons} from './utility.js';

window.onresize = handleResize;

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
    document.querySelector('#spin-holder').classList.remove('invisible')
    document.querySelector('#spin-holder').classList.add('visible')
    disableAllButtons();
}

document.addEventListener('DOMContentLoaded', loadPage, false);

async function loadPage(e, progress="default", bookmarkClicked=true) {
    let bookText = document.getElementById('book-text');
    bookText.setAttribute('data-lines', getLineTotal(bookText));
    let chars = calculateCharacterLimit(bookText);
    bookText.setAttribute('data-char-limit', chars);
    let book = await getBookFromServer(chars);
    enableAllButtons();
    document.querySelector('#spin-holder').classList.add('invisible')
    document.querySelector('#spin-holder').classList.remove('visible')
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

document.querySelector('#next-button').addEventListener('click', async function() {
    let bookmark = document.querySelector('#bookmark');
    let startPage = Number(bookmark.getAttribute('data-bookmarked-page'));
    let currentPage = (await setPageByTurns(1)) + 1;
    if (startPage == currentPage) {
        bookmarkDone();
    } else {
        bookmarkReady();
    }
})

document.querySelector('#previous-button').addEventListener('click', async function() {
    let bookmark = document.querySelector('#bookmark');
    let startPage = Number(bookmark.getAttribute('data-bookmarked-page'));
    let currentPage = (await setPageByTurns(-1)) + 1;
    if (startPage == currentPage && currentPage != 1) {
        bookmarkDone();
    } else {
        bookmarkReady();
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

async function updateProgress() {
    let bookText = document.querySelector('#book-text');
    let pageNumber = document.querySelector('#page-number');
    let progress = pageNumber.getAttribute('data-progress');
    let length = bookText.getAttribute('data-last-line-number');
    postProgressToServer(progress, length);
}