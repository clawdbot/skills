const LZString = require('./lz-string.js');

// Re-implement SudokuPad's classic compact codec (zipClassicSudoku2)
// Source: https://sudokupad.app/puzzletools.js
const blankEncodes = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx';

function zipClassicSudoku2(puzzle = '') {
  if (puzzle.length === 0) return '';
  const isDigit = (ch) => {
    const code = ch.charCodeAt(0);
    return code >= 49 && code <= 57;
  };

  let digit = isDigit(puzzle[0]) ? puzzle[0] : '0';
  let res = '';
  let blanks = 0;

  for (let i = 1; i < puzzle.length; i++) {
    const next = isDigit(puzzle[i]) ? puzzle[i] : '0';
    if (blanks === 5 || next !== '0') {
      res += blankEncodes[Number(digit) + blanks * 10];
      digit = next;
      blanks = 0;
    } else {
      blanks++;
    }
  }

  res += blankEncodes[Number(digit) + blanks * 10];
  return res;
}

const puzzle81 = process.argv[2];
const title = process.argv[3] || 'Puzzle';
const message = process.argv[4] || `Hi, please take a look at this puzzle: "${title}"`;

if (!puzzle81 || puzzle81.length !== 81) {
  console.error('Usage: node encode_native.js <81-char 0-9/. grid> [title] [message]');
  process.exit(1);
}

// Normalize: accept '.' or '_' as empty
const normalized = puzzle81.replace(/[._]/g, '0');

const p = zipClassicSudoku2(normalized);

const wrapper = {
  p,
  n: `${title}`,
  s: '',
  m: message,
};

// SudokuPad share links should be URL-safe.
// Using compressToEncodedURIComponent avoids '+', '/', '=' so chat apps won't mangle the payload.
const compressed = LZString.compressToEncodedURIComponent(JSON.stringify(wrapper));
console.log(compressed);
