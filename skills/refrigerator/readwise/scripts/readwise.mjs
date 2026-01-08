#!/usr/bin/env node
/**
 * Readwise API (v2) - Highlights and Books
 * API Docs: https://readwise.io/api_deets
 */

const BASE_URL = 'https://readwise.io/api/v2';

function usage() {
  console.error(`Usage: readwise.mjs <command> [options]

Commands:
  books [--limit N]                    List books/sources
  highlights [--book-id ID] [--limit N] Get highlights
  search "query"                        Search highlights
  export [--updated-after YYYY-MM-DD]   Export all highlights

Options:
  --limit N         Number of results (default: 20)
  --book-id ID      Filter by book ID
  --updated-after   Only export highlights updated after date
  --help            Show this help

Environment:
  READWISE_TOKEN    API token from https://readwise.io/access_token
`);
  process.exit(2);
}

function getToken() {
  const token = (process.env.READWISE_TOKEN ?? '').trim();
  if (!token) {
    console.error('Error: READWISE_TOKEN environment variable not set');
    console.error('Get your token from: https://readwise.io/access_token');
    process.exit(1);
  }
  return token;
}

async function request(endpoint, params = {}) {
  const token = getToken();
  const url = new URL(`${BASE_URL}${endpoint}`);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
  });
  
  const resp = await fetch(url, {
    headers: {
      'Authorization': `Token ${token}`,
      'Accept': 'application/json'
    }
  });
  
  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    throw new Error(`Readwise API error (${resp.status}): ${text}`);
  }
  
  return resp.json();
}

async function listBooks(limit = 20) {
  const data = await request('/books/', { page_size: limit });
  const books = (data.results || []).map(b => ({
    id: b.id,
    title: b.title,
    author: b.author,
    category: b.category,
    source: b.source,
    num_highlights: b.num_highlights,
    cover_image_url: b.cover_image_url
  }));
  console.log(JSON.stringify({ count: data.count, books }, null, 2));
}

async function getHighlights(bookId, limit = 20) {
  const params = { page_size: limit };
  if (bookId) params.book_id = bookId;
  
  const data = await request('/highlights/', params);
  const highlights = (data.results || []).map(h => ({
    id: h.id,
    text: h.text,
    note: h.note,
    location: h.location,
    location_type: h.location_type,
    highlighted_at: h.highlighted_at,
    book_id: h.book_id,
    url: h.url,
    tags: h.tags
  }));
  console.log(JSON.stringify({ count: data.count, highlights }, null, 2));
}

async function searchHighlights(query) {
  // Readwise doesn't have a direct search endpoint, so we fetch and filter
  // For production, you'd want to paginate through all results
  const data = await request('/highlights/', { page_size: 100 });
  const results = (data.results || []).filter(h => 
    h.text?.toLowerCase().includes(query.toLowerCase()) ||
    h.note?.toLowerCase().includes(query.toLowerCase())
  );
  console.log(JSON.stringify({ 
    query,
    count: results.length,
    highlights: results.slice(0, 20).map(h => ({
      id: h.id,
      text: h.text,
      note: h.note,
      book_id: h.book_id
    }))
  }, null, 2));
}

async function exportHighlights(updatedAfter) {
  const params = {};
  if (updatedAfter) params.updatedAfter = updatedAfter;
  
  const data = await request('/export/', params);
  const results = (data.results || []).map(book => ({
    title: book.title,
    author: book.author,
    source: book.source,
    highlights: (book.highlights || []).map(h => ({
      text: h.text,
      note: h.note,
      location: h.location,
      highlighted_at: h.highlighted_at
    }))
  }));
  console.log(JSON.stringify({ 
    count: results.length,
    books: results 
  }, null, 2));
}

// CLI parsing
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '-h' || args[0] === '--help') usage();

const command = args[0];
let limit = 20;
let bookId = null;
let query = null;
let updatedAfter = null;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === '--limit' || a === '-n') {
    limit = parseInt(args[++i] || '20', 10);
  } else if (a === '--book-id') {
    bookId = args[++i];
  } else if (a === '--updated-after') {
    updatedAfter = args[++i];
  } else if (!a.startsWith('-')) {
    query = a;
  }
}

try {
  switch (command) {
    case 'books':
      await listBooks(limit);
      break;
    case 'highlights':
      await getHighlights(bookId, limit);
      break;
    case 'search':
      if (!query) {
        console.error('Error: search requires a query');
        usage();
      }
      await searchHighlights(query);
      break;
    case 'export':
      await exportHighlights(updatedAfter);
      break;
    default:
      console.error(`Unknown command: ${command}`);
      usage();
  }
} catch (e) {
  console.error('Error:', e.message);
  process.exit(1);
}
