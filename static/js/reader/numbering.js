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
 * @return {Object[]} An array of objects (pages). Each object has two
 * values: 'num' (the line number of the first line of the page), and
 * 'content' (the content of the page as an array of strings). The array is
 * ordered from first page to last page.
 */
export function getNumberedBook() {
    let book = getBookFromSession();
    let bookText = document.querySelector('#book-text');
    let lines = parseInt(bookText.getAttribute('data-lines'));
    return splitIntoNumberedPages(book, lines);
}

/**
 * Return the line number of the last line in a given text (such
 * as a whole book or a page).
 * @param {String[]} textList A text such as book or page stored as an array
 * of every line of the text, including line numbers on relevant lines.
 * @return {Number} The line number of the last line.
 */
export function getLastLineNumber(textList) {
    for (let line of textList.reverse()) {
        if (hasNumLabel(line)) {
            return Number(getNumAndText(line)[0]);
        }
    }
}

/**
 * Take a whole book and split it into numbered pages according to
 * the pageSize value passed to the function, the number of lines on one 
 * page.
 * @param {String[]} book The book, as an array of strings, which should
 * be split into numbered pages. 
 * @param {Number} pageSize The amount of lines that should be on one page. 
 * @return {Object[]} An array of objects, each with the line number of the 
 * first line of their page and the page content ('num' and 'content'
 * respectively).
 */
function splitIntoNumberedPages(book, pageSize) {
    let numberedPages = [];
    splitIntoPages(book, pageSize).forEach((page) => {
        for (let line of page) {
            if (hasNumLabel(line)) {
                let num = getNumAndText(line)[0];
                numberedPages.push({
                    "num": num,
                    "content": removeNumbers(page)
                });
                break;
            }
        }
    });
    return numberedPages;
}

/**
 * Take a whole book and split it into pages according to the pageSize
 * value passed to the function, the number of lines on one page.
 * @param {String[]} book The book, as an array of strings, which should
 * be split into pages. 
 * @param {Number} pageSize The amount of lines that should be on one page. 
 * @return {String[][]} A two dimensional array. Returns an array of pages,
 * with a page being an array of strings, ordered from first page to last page.
 */
function splitIntoPages(book, pageSize) {
    if (pageSize < 1) {
        alert("We're sorry - there was an issue loading this page. Redirecting to dashboard.");
        location.replace('/');
        throw new Error('Page size cannot be less than 1.');
    }
    let pages = [];
    for (let i = 0; i < book.length; i += pageSize) {
        pages.push(book.slice(i, i + pageSize));
    }
    return pages;
}

/**
 * Remove any line numbers from a list of strings such as a page.
 * @param {String[]} textList The list of strings such as a page
 * or book which should have the line numbers removed. 
 * @return {String[]} The list of strings without any line numbers.
 */
function removeNumbers(textList) {
    return textList.map((line) => {
        if (hasNumLabel(line)) {
            return getNumAndText(line)[1];
        }
        return line;
    });
}

/**
 * Check if a given line has a line number label.
 * @param {String} line The line which should be checked.
 * @return {Boolean} true if has a label, false if not.
 */
function hasNumLabel(line) {
    return line.includes("𓀴");
}

/**
 * Take a line with a line number and split it into two values:
 * the line number, and the text content of the line, in that order.
 * @param {String} line The line which should be split into a line
 * number and text content. 
 * @return {String[]} An array containing two values - firstly,
 * the line number, and secondly, the text content of the line.
 */
function getNumAndText(line) {
    return line.split("𓀴");
}
