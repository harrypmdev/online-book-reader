import { getBookFromSession } from "./utility.js";

export function getNumberedBook() {
    let book = getBookFromSession();
    let bookText = document.querySelector('#book-text');
    let lines = parseInt(bookText.getAttribute('data-lines'));
    return splitIntoNumberedPages(book, lines);
}

function splitIntoNumberedPages(book, pageSize) {
    let numberedPages = [];
    splitIntoPages(book, pageSize).forEach((page) => {
        for (let line of page) {
            if (hasNumLabel(line)) {
                let [num, text] = getNumAndText(line);
                numberedPages.push({
                    "num": num,
                    "content": removeNumbers(page)
                });
                break;
            }
        }
    })
    return numberedPages;
}

function splitIntoPages(book, pageSize) {
    let pages = [];
    for (let i = 0; i < book.length; i += pageSize) {
        pages.push(book.slice(i, i + pageSize));
    }
    return pages;
}

function removeNumbers(text_list) {
    return text_list.map((line) => {
        if (hasNumLabel(line)) {
            return getNumAndText(line)[1];
        }
        return line;
    })
}

export function getLastLineNumber(book) {
    for (let line of book.reverse()) {
        if (hasNumLabel(line)) {
            return Number(getNumAndText(line)[0]);
        }
    }
}

function hasNumLabel(line) {
    return line.includes("𓀴");
}

function getNumAndText(line) {
    let lines = line.split("𓀴");
    return [lines[0], lines[1]];
}
