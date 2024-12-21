/* A module for ajax functions to get and post data to and from the server.

Public Functions:
postProgressToServer -- post book progress to server.
getBookFromServer -- get book from server and save it to session.
*/

/**
 * Post book progress to server.
 * @param {Number} progress The user's progress through the book
 * as a line number.
 * @param {Number} length The line number of the final line
 * of the book, i.e, the books total length.
 */
export async function postProgressToServer(progress, length) {
    let bookText = document.getElementById('book-text')
    let url = bookText.getAttribute('data-ajax-update-url');
    let csrfToken = bookText.getAttribute('data-csrf-token');
    let bookID = bookText.getAttribute('data-book-id');
    const response = await _progressAjaxFetch(
        url, csrfToken, progress, 
        bookID, length
    );
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    let data = await response.json()
    if (!data['completion'].includes('Progress updated.')) {
        throw new Error(`Error updating progress: ${data['completion']}`);
    }
}

/**
 * Return book from server. Uses book ID from book-text element.
 * Saves book to session as 'textList', so only needs needs to be
 * retrieved from server once per reader app load.
 * @param {Number} lineWidth The maximum amount of characters that should
 * be in each line of the book.
 * @returns {String[]} The book as an array of every line of the
 * book. Most lines start with the line's original line number, 
 * separated from the text content of the line with the character '𓀴'.
 */
export async function getBookFromServer(lineWidth) {
    let bookText = document.getElementById('book-text')
    let bookID = bookText.getAttribute('data-book-id');
    let url = bookText.getAttribute('data-ajax-url');
    let csrfToken = bookText.getAttribute('data-csrf-token');
    const response = await _bookAjaxFetch(url, csrfToken, lineWidth, bookID);
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    let data = await response.json()
    sessionStorage.setItem("textList", JSON.stringify(data));
    return data
}

async function _progressAjaxFetch(url, csrfToken, progress, bookID, length) {
    // Ajax call to post progress to server.
    return await fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrfToken,
        }, 
        body:JSON.stringify({
            'progress': progress,
            'book_id': bookID,
            'length': length,
            })
    });
}

async function _bookAjaxFetch(url, csrfToken, lineWidth, bookID) {
    // Ajax call to fetch book from server.
    return await fetch(url, {
        method:'POST',
        headers:{
         'Content-Type':'application/json',
         'X-CSRFToken':csrfToken,
        }, 
        body:JSON.stringify({
         'num': lineWidth,
         'book_id': bookID,
         })
     })
}