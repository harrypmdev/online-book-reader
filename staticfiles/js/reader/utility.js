/* A module for simple utility functions utilised in the reader app. 

Public Functions:
getBookFromSession -- retrieve the book stored in the current session.
calculateProgress -- return progress accounting for whether the user
                     is on the last page of the book.
enableAllButtons -- enable book, next and previous buttons on reader app.
disableAllButtons -- disable book, next and previous buttons on reader app.
makeSpinnerInvisible -- make loading spinner invisible.
makeSpinnerVisible -- make loading spinner visible.
*/

/**
 * Return the book stored in the current session.
 * If not book stored in session, returns null.
 * @returns {String[]} The book stored as an array of every line 
 * of the book. Maximum line width is whatever was established
 * when book was saved to session.
 */
export function getBookFromSession() {
    return JSON.parse(sessionStorage.getItem('textList'));
}

/**
 * Correct the progress number if user is reading final page of book
 * so that 100% progress can be achieved. Otherwise, return the 
 * progress number unchanged.
 * @param {Number} progress The progress number for the current page,
 * not accounting for whether the user is on the last page.
 * @returns {Number} The progress number accounting for whether the
 * user is on the last page of the book.
 */
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

/**
 * Enable all buttons on the reader app page - bookmark, previous and next
 * buttons.
 */
export function enableAllButtons() {
    document.querySelector('#bookmark').removeAttribute('disabled');
    document.querySelector('#previous-button').removeAttribute('disabled');
    document.querySelector('#next-button').removeAttribute('disabled');
}

/**
 * Disable all buttons on the reader app page - bookmark, previous and next
 * buttons.
 */
export function disableAllButtons() {
    document.querySelector('#bookmark').setAttribute('disabled', '');
    document.querySelector('#previous-button').setAttribute('disabled', '');
    document.querySelector('#next-button').setAttribute('disabled', '');  
}

/**
 * Make the loading spinner invisible, including in cases where it has
 * been set to visible in JS (such as upon screen resizing).
 */
export function makeSpinnerInvisible() {
    document.querySelector('#spin-holder').classList.add('invisible');
    document.querySelector('#spin-holder').classList.remove('visible');
}

/**
 * Make the loading spinner visible, including in cases where it has
 * been set to invisible in JS (such as upon page loading).
 */
export function makeSpinnerVisible() {
    document.querySelector('#spin-holder').classList.remove('invisible');
    document.querySelector('#spin-holder').classList.add('visible');
}