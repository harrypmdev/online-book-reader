/**
 * @jest-environment jsdom
 */

const bookmarkDone = require('../reader/reader.js');

/*Mocking for test, establishes 'bookmark' button element.*/
beforeEach(() => {
    document.body.innerHTML = '<button id="bookmark"></button>'
  });

/*Test that bookmarkDone function updates bookmark functionality
correctly.
*/
describe('test bookmarkDone function', () => {
    test('expect book', () => {
        bookmarkDone();
        let bookmark = document.querySelector('#bookmark');
        expect(bookmark.getAttribute('data-clicked')).toEqual('true');
        expect(bookmark.getAttribute('disabled')).toEqual('');
        expect(bookmark.classList.contains('btn-success')).toEqual(true);
        expect(bookmark.classList.contains('btn-warning')).toEqual(false);
    });
});