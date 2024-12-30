/* A module for functions that set the current page. 

Public Functions:
setPageByProgress -- set the current page with a 'progress' value,
                     a number for a specific line in the book.
setPageByTurns -- set the current page with turns (one page turn
                  forward, 2 page turns backwards etc.).
*/

import { setPageNumbers, renderPage } from './render.js';
import { calculateProgress } from './utility.js';
import { getNumberedBook } from './numbering.js';

/**
 * Set and display the current page by means of a progress value.
 * @param {Number} progress The progress value in question, a number for a 
 * specific line in the book.
 * @return {Number} The page number for the newly set page.
 */
export async function setPageByProgress(progress) {
    let bookInPages = await getNumberedBook();
    let pageNumber = bookInPages.length - 1;
    for (const [i, page] of bookInPages.entries()) {
        if ((Number(progress) < page.num)) {
            pageNumber = i-1;
            break;
        }
    }
    document.querySelector('#bookmark').setAttribute('data-bookmarked-page', pageNumber+1);
    setPageNumbers(pageNumber, bookInPages.length);
    let currentPage = setPageContent(bookInPages, 0);
    /* Set progress back to progress value given by function user, so switching
    screen size does not gradually move page back or forward in book.
    */
    document.querySelector('#page-number').setAttribute('data-progress', progress);
    return currentPage;
}

/**
 * Set and display the current page by number of turns.
 * @param {Number} turns The number of pages that should be turned forward or
 * backward. 1 goes forward by one page, -3 goes backwards 3 pages, 5 goes forward
 * 5 pages, etc.
 * @return {Number} The page number for the newly set page.
 */
export async function setPageByTurns(turns){
    let bookInPages = getNumberedBook();
    return setPageContent(bookInPages, turns);
}

/**
 * Display page content to the user. Set bookmark element's data-progress
 * attribute to the now current progress.
 * @param {Object[]} bookInPages The book split into numbered pages, as 
 * returned by the getNumberedBook function.
 * @param {Number} turns The number of page turns forward or backward
 * (negative numbers) the book should turn before displaying content. 
 * @return {Number} The page number for the newly set page.
 */
function setPageContent(bookInPages, turns) {
    let pageNumberElement = document.querySelector('#page-number');
    let pageNumber = pageNumberElement.getAttribute('data-page-number');
    pageNumber = Number(pageNumber)+Number(turns);
    let page = bookInPages[pageNumber];
    renderPage(page.content);
    setPageNumbers(pageNumber, bookInPages.length);
    let progress = calculateProgress(page.num);
    document.querySelector('#page-number').setAttribute('data-progress', progress);
    return pageNumber;
}