/**
 * @jest-environment jsdom
 */

import { getLastLineNumber } from '../reader/numbering.js';

describe('test getLastLineNumber function', () => {
    test('expect book', () => {
        let text = [
            '1𓀴First Line',
            '2𓀴Second Line'
        ];
        expect(getLastLineNumber(text)).toEqual(2);
    })
})