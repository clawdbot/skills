const LZString = require('./lz-string.js');

// Get JSON from args
const jsonStr = process.argv[2];
if (!jsonStr) {
    console.error("Usage: node encode_lz.js <json_string>");
    process.exit(1);
}

// Compress to a URL-safe payload for SudokuPad /puzzle/ links.
// This avoids '+', '/', '=' (which often break when passed through chat systems).
const compressed = LZString.compressToEncodedURIComponent(jsonStr);
console.log(compressed);
