import { process } from './nlp.js';

test('is apple fruit or company', () => {
  expect(process("apple")).toEqual(200);
});
