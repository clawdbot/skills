#!/usr/bin/env node
/**
 * Readwise Reader API (v3) - Saved Articles & Documents
 * API Docs: https://readwise.io/reader_api
 */

const BASE_URL = 'https://readwise.io/api/v3';

function usage() {
  console.error(`Usage: reader.mjs <command> [options]

Commands:
  list [options]              List documents
  get <document_id>           Get document details
  save <url> [--location X]   Save URL to Reader
  search "query"              Search documents

List options:
  --location <loc>    new, later, shortlist, archive, feed (default: all)
  --category <cat>    article, email, rss, highlight, note, pdf, epub, tweet, video
  --limit N           Number of results (default: 20)

Save options:
  --location <loc>    new, later, shortlist, archive (default: new)
  --tags <tags>       Comma-separated tags

General:
  --help              Show this help

Environment:
  READWISE_TOKEN      API token from https://readwise.io/access_token
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

async function request(endpoint, options = {}) {
  const token = getToken();
  const method = options.method || 'GET';
  const url = new URL(`${BASE_URL}${endpoint}`);
  
  if (method === 'GET' && options.params) {
    Object.entries(options.params).forEach(([k, v]) => {
      if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
    });
  }
  
  const fetchOptions = {
    method,
    headers: {
      'Authorization': `Token ${token}`,
      'Accept': 'application/json',
      ...(options.body ? { 'Content-Type': 'application/json' } : {})
    }
  };
  
  if (options.body) {
    fetchOptions.body = JSON.stringify(options.body);
  }
  
  const resp = await fetch(url, fetchOptions);
  
  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    throw new Error(`Reader API error (${resp.status}): ${text}`);
  }
  
  return resp.json();
}

async function listDocuments(location, category, limit = 20) {
  const params = { page_size: limit };
  if (location) params.location = location;
  if (category) params.category = category;
  
  const data = await request('/list/', { params });
  const documents = (data.results || []).map(d => ({
    id: d.id,
    url: d.url,
    title: d.title,
    author: d.author,
    source: d.source,
    category: d.category,
    location: d.location,
    tags: d.tags,
    site_name: d.site_name,
    word_count: d.word_count,
    created_at: d.created_at,
    updated_at: d.updated_at,
    reading_progress: d.reading_progress,
    first_opened_at: d.first_opened_at,
    last_opened_at: d.last_opened_at,
    saved_at: d.saved_at,
    summary: d.summary?.substring(0, 200),
    image_url: d.image_url
  }));
  console.log(JSON.stringify({ count: data.count, documents }, null, 2));
}

async function getDocument(docId) {
  const data = await request(`/list/`, { params: { id: docId } });
  const doc = data.results?.[0];
  if (!doc) {
    console.log(JSON.stringify({ error: 'Document not found' }));
    return;
  }
  console.log(JSON.stringify({
    id: doc.id,
    url: doc.url,
    title: doc.title,
    author: doc.author,
    source: doc.source,
    category: doc.category,
    location: doc.location,
    tags: doc.tags,
    site_name: doc.site_name,
    word_count: doc.word_count,
    reading_progress: doc.reading_progress,
    summary: doc.summary,
    content: doc.content?.substring(0, 5000),
    notes: doc.notes,
    highlights: doc.highlights
  }, null, 2));
}

async function saveUrl(url, location = 'new', tags = null) {
  const body = { url };
  if (location) body.location = location;
  if (tags) body.tags = tags.split(',').map(t => t.trim());
  
  const data = await request('/save/', { method: 'POST', body });
  console.log(JSON.stringify({
    success: true,
    id: data.id,
    url: data.url,
    title: data.title
  }, null, 2));
}

async function searchDocuments(query) {
  // Reader doesn't have direct search, so fetch and filter
  const data = await request('/list/', { params: { page_size: 100 } });
  const results = (data.results || []).filter(d =>
    d.title?.toLowerCase().includes(query.toLowerCase()) ||
    d.author?.toLowerCase().includes(query.toLowerCase()) ||
    d.summary?.toLowerCase().includes(query.toLowerCase())
  );
  console.log(JSON.stringify({
    query,
    count: results.length,
    documents: results.slice(0, 20).map(d => ({
      id: d.id,
      title: d.title,
      url: d.url,
      author: d.author,
      category: d.category
    }))
  }, null, 2));
}

// CLI parsing
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '-h' || args[0] === '--help') usage();

const command = args[0];
let limit = 20;
let location = null;
let category = null;
let docId = null;
let url = null;
let query = null;
let tags = null;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === '--limit' || a === '-n') {
    limit = parseInt(args[++i] || '20', 10);
  } else if (a === '--location') {
    location = args[++i];
  } else if (a === '--category') {
    category = args[++i];
  } else if (a === '--tags') {
    tags = args[++i];
  } else if (!a.startsWith('-')) {
    if (command === 'get') docId = a;
    else if (command === 'save') url = a;
    else if (command === 'search') query = a;
  }
}

try {
  switch (command) {
    case 'list':
      await listDocuments(location, category, limit);
      break;
    case 'get':
      if (!docId) {
        console.error('Error: get requires a document_id');
        usage();
      }
      await getDocument(docId);
      break;
    case 'save':
      if (!url) {
        console.error('Error: save requires a URL');
        usage();
      }
      await saveUrl(url, location, tags);
      break;
    case 'search':
      if (!query) {
        console.error('Error: search requires a query');
        usage();
      }
      await searchDocuments(query);
      break;
    default:
      console.error(`Unknown command: ${command}`);
      usage();
  }
} catch (e) {
  console.error('Error:', e.message);
  process.exit(1);
}
