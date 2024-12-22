/* A script to add functionality to the reader app, including client-side
pagination and saving book progress using the bookmark button.
*/

import { postProgressToServer, getBookFromServer } from './ajaxFunctions.js';
import { calculateCharacterLimit, calculateLineTotal} from './calculatePage.js';
import { getLastLineNumber } from './numbering.js';
import { setPageByTurns, setPageByProgress } from './setPage.js';
import { enableAllButtons, disableAllButtons, 
    makeSpinnerInvisible, makeSpinnerVisible } from './utility.js';

document.addEventListener('DOMContentLoaded', handleLoadPage);
// Add event listener upon window resizing so page content can adjust.
window.addEventListener('resize', handleResize);

/**
 * Handle the loading of the page. Sets the book-text element's
 * data-char-limit and data-lines attributes.
 * @param {Event} event The event that triggers the callback. 
 * @param {Number} progress The current progress through the book.
 * By default is a placeholder which tells the function to take the
 * progress value from the HTML attributes set by the server.
 * @param {Boolean} bookmarkClicked Whether or not the page should load
 * with the bookmark button already clicked. 'true' by default.
 */
async function handleLoadPage(event, progress=-1, bookmarkClicked=true) {
    addReaderButtonEventListeners();
    let bookText = document.getElementById('book-text');
    let chars = calculateCharacterLimit(bookText);
    bookText.setAttribute('data-char-limit', chars);
    bookText.setAttribute('data-lines', calculateLineTotal(bookText));
    let book = await getBookFromServer(chars);
    enableAllButtons();
    makeSpinnerInvisible();
    bookText.setAttribute('data-last-line-number', getLastLineNumber(book));
    if (progress == -1) {
        let pageNumberEl = document.getElementById('page-number');
        progress = parseInt(pageNumberEl.getAttribute('data-progress'));
    }
    if (Number(progress) > 0 && bookmarkClicked) {
        bookmarkDone();
    }
    setPageByProgress(progress);
}

/**
 * Handle resizing of the window. Reloads the page taking into account the
 * new screen size, without losing track of the user's current (possibly
 * unsaved) progress.
 */
function handleResize() {
    let pageNumberEl = document.getElementById('page-number');
    let progress = parseInt(pageNumberEl.getAttribute('data-progress'));
    let bookmark = document.querySelector('#bookmark');
    let clicked = true;
    if (bookmark.getAttribute('data-clicked') == 'false') {
        bookmarkReady();
        clicked = false;
    }
    handleLoadPage(Event, progress, clicked);
    document.getElementById('book-text').innerText = "";
    makeSpinnerVisible();
    disableAllButtons();
}

/**
 * Add event listeners for all buttons in the reader app 
 * (bookmark, next and previous).
 */
function addReaderButtonEventListeners() {
    document.querySelector('#next-button').addEventListener('click', handleNextClick);
    document.querySelector('#previous-button').addEventListener('click', handlePreviousClick);
    document.querySelector('#bookmark').addEventListener('click', handleBookMarkClick);
}

/**
 * Handle the next page button's click event.
 * Loads the next page and sets the bookmark to the appropriate state.
 */
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

/**
 * Handle the previous page button's click event.
 * Loads the previous page and sets the bookmark to the appropriate state.
 */
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

/**
 * Handle the bookmark's click event.
 * Posts updated progress to server and sets bookmark's data-bookmarked-page
 * attribute to the bookmarked page number.
 */
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

/**
 * Disable bookmark functionality and change appearance to reflect this.
 */
function bookmarkDone() {
    let bookmark = document.querySelector('#bookmark');
    bookmark.innerHTML = 'Bookmarked<i class="fa-solid fa-bookmark fa-lg ml-2"></i>';
    bookmark.classList.remove('btn-warning');
    bookmark.classList.add('btn-success');
    bookmark.setAttribute('disabled', '');
    bookmark.setAttribute('data-clicked', 'true');
}

/**
 * Enable bookmark functionality and change appearance to reflect this.
 */
function bookmarkReady() {
    let bookmark = document.querySelector('#bookmark');
    bookmark.innerHTML = 'Bookmark Page<i class="fa-regular fa-bookmark fa-lg ml-2"></i>';
    bookmark.classList.add('btn-warning');
    bookmark.classList.remove('btn-success');
    bookmark.removeAttribute('disabled');
    bookmark.setAttribute('data-clicked', 'false');
}

/**
 * Post user's progress for this book to the server using page-number element's
 * data-progress attribute (the current book progress) and book-text element's
 * data-last-line-number attribute (the last line of the entire book so the
 * percentage of completion can be calculated on the server-side).
 */
async function updateProgress() {
    let bookText = document.querySelector('#book-text');
    let pageNumber = document.querySelector('#page-number');
    let length = bookText.getAttribute('data-last-line-number');
    let progress = pageNumber.getAttribute('data-progress');
    postProgressToServer(progress, length);
}