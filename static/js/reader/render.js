export function renderPage(page) {
    let content = "";
    for (let line of page) {
        content += line += "<br>";
    }
    document.getElementById('book-text').innerHTML = content;
}

export function setPageNumbers(pageNumber, totalPages) {
    let pageNumberElement = document.querySelector('#page-number');
    pageNumberElement.innerHTML = `${pageNumber+1} of ${totalPages}`;
    pageNumberElement.setAttribute('data-page-number', pageNumber);
    if (pageNumber >= totalPages-1) {
        document.querySelector('#next-button').style.visibility = 'hidden';
        document.querySelector('#bookmark').setAttribute('data-final-page', 'true');
    } else {
        document.querySelector('#next-button').style.visibility = 'visible';
        document.querySelector('#bookmark').setAttribute('data-final-page', 'false');
    }
    document.querySelector('#previous-button').style.visibility = pageNumber <= 0 ?
    'hidden' : 'visible';
}