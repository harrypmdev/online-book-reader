/* A module for functions that aid in calculating the amount of text that
can fit in a paragraph element.

Public Functions:
calculateCharacterLimit -- calculate and return the number of characters 
                           that can fit horizontally in a paragraph element.
calculateLineTotal -- calculate and return the number of lines that 
                      can fit vertically in a paragraph element.
*/

/**
 * Return the total number of characters that can fit horizontally
 * in one line of a paragraph element.
 * @param  {Element} el the element for which the number of characters
 * should be counted.
 * @return {integer} The number of characters counted.
 */
export function calculateCharacterLimit(el) {
    let originalContent = el.innerText;
    el.innerHTML = '<span class="charcount">#</span>'.repeat(150);
    let allSpans = document.getElementsByClassName('charcount');
    let prevSpan;
    let i = 0;
    for (let span of allSpans) {
        i++;
        if (typeof prevSpan != undefined && parseInt(span.offsetTop) > prevSpan) {
            el.innerText = originalContent;
            return i - 1;
        }
        prevSpan = parseInt(span.offsetTop);
    }
    return 0;
}

/**
 * Return the total number of lines that can fit vertically
 * in a paragraph element.
 * @param  {Element} el the element for which the number of lines should
 * be counted.
 * @return {integer} The number of lines counted.
 */
export function calculateLineTotal(el) {
    let originalContent = el.innerText;
    el.innerText = "";
    let i = 0;
    while (!isOverTextLimit(el)) {
      i++;
      el.innerText += `\n`;
    }
    el.innerText = originalContent;
    return i - 1;
}

/**
 * Return a boolean that indicates whether a paragraph element's 
 * text fits inside the paragraph viewport.
 * @param {Element} el The paragraph element for which this should be
 * checked.
 * @return {Boolean} false if the text fits and true if it does not.
 */
function isOverTextLimit(el) {
    return el.scrollHeight > el.offsetHeight;
}