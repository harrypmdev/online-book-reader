/* A module for functions that aid in the processing of the book's
line numbers.

Public Functions:
getNumberedBook -- return the reader app's current book from the session,
                   split into pages with the line number of the first line 
                   of the page.
getLastLineNumber -- return the line number of the last line 
                     in the passed book.
*/

import { getBookFromSession } from "./utility.js";

/**
 * Return the book currently stored in the session split into numbered pages
 * as per the line height of the book-text element.
 * @returns {Object[]} An array of objects (pages). Each object has two
 * values: 'num' (the line number of the first line of the page), and
 * 'content' (the content of the page as an array of strings). The array is
 * ordered from first page to last page.
 */
export function getNumberedBook() {
    let book = getBookFromSession();
    let bookText = document.querySelector('#book-text');
    let lines = parseInt(bookText.getAttribute('data-lines'));
    return _splitIntoNumberedPages(book, lines);
}

/**
 * Return the line number of the last line in a given text (such
 * as a whole book or a page).
 * @param {String[]} textList A text such as book or page stored as an array
 * of every line of the text, including line numbers on relevant lines.
 * @returns {Number} The line number of the last line.
 */
export function getLastLineNumber(textList) {
    for (let line of textList.reverse()) {
        if (_hasNumLabel(line)) {
            return Number(_getNumAndText(line)[0]);
        }
    }
}

function _splitIntoNumberedPages(book, pageSize) {
    /* Take a whole book and split it into numbered pages according to
    the pageSize value passed to the function, the number of lines on one 
    page. Return a list of objects, each with the line number of the first
    line of their page and the page content ('num' and 'content' respectively).
    */
    let numberedPages = [];
    _splitIntoPages(book, pageSize).forEach((page) => {
        for (let line of page) {
            if (_hasNumLabel(line)) {
                let [num, text] = _getNumAndText(line);
                numberedPages.push({
                    "num": num,
                    "content": _removeNumbers(page)
                });
                break;
            }
        }
    })
    return numberedPages;
}

function _splitIntoPages(book, pageSize) {
    /* Take a whole book and split it into pages according to the pageSize
    value passed to the function, the number of lines on one page. 
    */
    let pages = [];
    for (let i = 0; i < book.length; i += pageSize) {
        pages.push(book.slice(i, i + pageSize));
    }
    return pages;
}

function _removeNumbers(textList) {
    // Remove any line numbers from a list of strings such as a page.
    return textList.map((line) => {
        if (hasNumLabel(line)) {
            return getNumAndText(line)[1];
        }
        return line;
    })
}

function _hasNumLabel(line) {
    /* Return bool indicating whether a given line has a line number label -
    true if does, false if does not.
    */
    return line.includes("𓀴");
}

function _getNumAndText(line) {
    /* Take a line with a line number and split it into two values:
    the line number, and the text content of the line, in that order.
    */
    let lines = line.split("𓀴");
    return [lines[0], lines[1]];
}
