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
    let tokenMeta = document.querySelector('meta[name="csrf-token"]');
    let csrfToken = tokenMeta.getAttribute('content');
    let bookText = document.getElementById('book-text');
    let url = bookText.getAttribute('data-ajax-update-url');
    let bookID = bookText.getAttribute('data-book-id');
    const response = await progressAjaxFetch(
        url, csrfToken, progress, 
        bookID, length
    );
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    let data = await response.json();
    if (!data.completion.includes('Progress updated.')) {
        throw new Error(`Error updating progress: ${data.completion}`);
    }
}

/**
 * Return book from server. Uses book ID from book-text element.
 * Saves book to session as 'textList', so only needs needs to be
 * retrieved from server once per reader app load.
 * @param {Number} lineWidth The maximum amount of characters that should
 * be in each line of the book.
 * @return {String[]} The book as an array of every line of the
 * book. Most lines start with the line's original line number, 
 * separated from the text content of the line with the character '𓀴'.
 */
export async function getBookFromServer(lineWidth) {
    let tokenMeta = document.querySelector('meta[name="csrf-token"]');
    let csrfToken = tokenMeta.getAttribute('content');
    let bookText = document.getElementById('book-text');
    let bookID = bookText.getAttribute('data-book-id');
    let url = bookText.getAttribute('data-ajax-url');
    const response = await bookAjaxFetch(url, csrfToken, lineWidth, bookID);
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    let data = await response.json();
    sessionStorage.setItem("textList", JSON.stringify(data));
    return data;
}

/**
 * Post progress to server for a specific UserBook.
 * @param {String} url The url for the API endpoint.
 * @param {String} csrfToken The CSRF token.
 * @param {Number} progress The progress that should be posted - a book line
 * number. 
 * @param {Number} bookID The UserBook id for the book that should be fetched.
 * @param {Number} length The line number of the last line of the book, so a
 * percentage can be calculated.
 * @return {JSON} The fetched JSON from the API endpoint, if fetch is successful returns
 * a JSON with value 'completion' which indicates status of progress update.
 */
async function progressAjaxFetch(url, csrfToken, progress, bookID, length) {
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

/**
 * Asynchronously fetch a book from the server.
 * @param {String} url The url for the API endpoint.
 * @param {String} csrfToken The CSRF token.
 * @param {Number} lineWidth The max amount of characters that should be
 * able to fit on one line of the book.
 * @param {Number} bookID The UserBook id for the book that should be fetched.
 * @return {JSON} The fetched JSON from the API endpoint, if successful is an array
 * of strings, each string being a line in the book.
 */
async function bookAjaxFetch(url, csrfToken, lineWidth, bookID) {
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
     });
}