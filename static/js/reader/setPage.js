import { setPageNumbers, renderPage } from './render.js';
import { calculateProgress } from './utility.js';
import { getNumberedBook } from './numbering.js';

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

export async function setPageByProgress(progress) {
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
    document.querySelector('#page-number').setAttribute('data-progress', progress);
}

export async function setPageByTurns(turns){
    let bookInPages = getNumberedBook();
    return setPageContent(bookInPages, turns);
}