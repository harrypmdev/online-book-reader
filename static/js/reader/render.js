/* A module for render functions utilised in the reader app. 

Public Functions:
renderPage -- render a page of text.
setPageNumbers -- update the page numbers to reflect the passed arguments.
*/

/**
 * Render a page of text in the reader app.
 * @param {String[]} page The page that should be rendered.
 */
export function renderPage(page) {
    let content = "";
    for (let line of page) {
        content += line += "<br>";
    }
    document.getElementById('book-text').innerHTML = content;
}

/**
 * Update the page numbers on the reader app.
 * @param {Number} pageNumber The current page number.
 * @param {Number} totalPages The total number of pages for the
 * book on this screen size.
 */
export function setPageNumbers(pageNumber, totalPages) {
    let pageNumberElement = document.querySelector('#page-number');
    let nextButtonElement = document.querySelector('#next-button');
    pageNumberElement.innerHTML = `${pageNumber+1} of ${totalPages}`;
    pageNumberElement.setAttribute('data-page-number', pageNumber);
    if (pageNumber >= totalPages-1) {
        nextButtonElement.style.visibility = 'hidden';
        document.querySelector('#bookmark').setAttribute('data-final-page', 'true');
    } else {
        nextButtonElement.style.visibility = 'visible';
        document.querySelector('#bookmark').setAttribute('data-final-page', 'false');
    }
    document.querySelector('#previous-button').style.visibility = pageNumber <= 0 ?
    'hidden' : 'visible';
}