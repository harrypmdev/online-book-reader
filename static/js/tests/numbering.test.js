/**
 * @jest-environment jsdom
 */

import { getLastLineNumber } from '../reader/numbering.js';

/*Test that getLastLineNumber function returns line number
of last line in list.
*/
describe('test getLastLineNumber function', () => {
    test('expect book', () => {
        let text = [
            '1𓀴First Line',
            '2𓀴Second Line'
        ];
        expect(getLastLineNumber(text)).toEqual(2);
    });
});