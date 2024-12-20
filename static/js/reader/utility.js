export function getBookFromSession() {
    return JSON.parse(sessionStorage.getItem('text_list'));
}

export function calculateProgress(progress) {
    let bookText = document.querySelector('#book-text');
    let bookmark = document.querySelector('#bookmark');
    let length = bookText.getAttribute('data-last-line-number');
    if (bookmark.getAttribute('data-final-page') == 'true') {
        return length;
    } else {
        return progress;
    }
}
