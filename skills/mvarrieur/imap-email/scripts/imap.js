#!/usr/bin/env node

/**
 * IMAP Email CLI
 * Works with any standard IMAP server (Gmail, ProtonMail Bridge, Fastmail, etc.)
 */

const imaps = require('imap-simple');
const { simpleParser } = require('mailparser');
require('dotenv').config({ path: __dirname + '/../.env' });

// Configuration from environment
const config = {
  imap: {
    user: process.env.IMAP_USER,
    password: process.env.IMAP_PASS,
    host: process.env.IMAP_HOST || '127.0.0.1',
    port: parseInt(process.env.IMAP_PORT) || 1143,
    tls: process.env.IMAP_TLS === 'true',
    authTimeout: 10000,
    tlsOptions: {
      rejectUnauthorized: process.env.IMAP_REJECT_UNAUTHORIZED !== 'false',
    },
  },
};

const DEFAULT_MAILBOX = process.env.IMAP_MAILBOX || 'INBOX';

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0];
  const options = {};
  const positional = [];

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      options[key] = value || true;
      if (value && !value.startsWith('--')) i++;
    } else {
      positional.push(arg);
    }
  }

  return { command, options, positional };
}

// Connect to IMAP server
async function connect() {
  if (!config.imap.user || !config.imap.password) {
    throw new Error('Missing IMAP_USER or IMAP_PASS environment variables');
  }

  try {
    return await imaps.connect(config);
  } catch (err) {
    console.error('IMAP connection failed:', err.message);
    console.error('Host:', config.imap.host, 'Port:', config.imap.port);
    console.error('Verify IMAP server is accessible and credentials are correct');
    throw err;
  }
}

// Check for new/unread emails
async function checkEmails(mailbox = DEFAULT_MAILBOX, limit = 10, recentTime = null) {
  const connection = await connect();

  try {
    await connection.openBox(mailbox);

    // Search for unseen messages
    const searchCriteria = ['UNSEEN'];
    
    // Add time filter if specified
    if (recentTime) {
      const sinceDate = parseRelativeTime(recentTime);
      searchCriteria.push(['SINCE', sinceDate]);
    }
    
    const fetchOptions = {
      bodies: [''], // Fetch full message for better parsing
      markSeen: false,
    };

    const messages = await connection.search(searchCriteria, fetchOptions);
    const results = [];

    for (const item of messages.slice(0, limit)) {
      const all = item.parts.find((p) => p.which === '');

      if (all) {
        // Convert buffer to string for simpleParser
        const bodyStr = typeof all.body === 'string' 
          ? all.body 
          : all.body.toString('utf8');
        
        const parsed = await simpleParser(bodyStr);
        
        // Extract text snippet (prefer text over HTML)
        const snippet = parsed.text 
          ? parsed.text.slice(0, 200) 
          : (parsed.html ? parsed.html.slice(0, 200) : '');

        results.push({
          uid: item.attributes.uid,
          from: parsed.from?.text || 'Unknown',
          subject: parsed.subject || '(no subject)',
          date: parsed.date,
          snippet: snippet.replace(/\s+/g, ' ').trim(),
          flags: item.attributes.flags,
        });
      }
    }

    return results;
  } finally {
    connection.end();
  }
}

// Fetch full email by UID
async function fetchEmail(uid, mailbox = DEFAULT_MAILBOX) {
  const connection = await connect();

  try {
    await connection.openBox(mailbox);

    const searchCriteria = [['UID', uid]];
    const fetchOptions = {
      bodies: [''],
      markSeen: false,
    };

    const messages = await connection.search(searchCriteria, fetchOptions);

    if (messages.length === 0) {
      throw new Error(`Message UID ${uid} not found`);
    }

    const item = messages[0];
    const all = item.parts.find((p) => p.which === '');
    
    // Convert buffer to string for simpleParser
    const bodyStr = typeof all.body === 'string' 
      ? all.body 
      : all.body.toString('utf8');
    
    const parsed = await simpleParser(bodyStr);

    return {
      uid: item.attributes.uid,
      from: parsed.from?.text,
      to: parsed.to?.text,
      subject: parsed.subject,
      date: parsed.date,
      text: parsed.text,
      html: parsed.html,
      attachments: parsed.attachments?.map((a) => ({
        filename: a.filename,
        contentType: a.contentType,
        size: a.size,
      })),
      flags: item.attributes.flags,
    };
  } finally {
    connection.end();
  }
}

// Parse relative time (e.g., "2h", "30m", "7d") to Date
function parseRelativeTime(timeStr) {
  const match = timeStr.match(/^(\d+)(m|h|d)$/);
  if (!match) {
    throw new Error('Invalid time format. Use: 30m, 2h, 7d');
  }

  const value = parseInt(match[1]);
  const unit = match[2];
  const now = new Date();

  switch (unit) {
    case 'm': // minutes
      return new Date(now.getTime() - value * 60 * 1000);
    case 'h': // hours
      return new Date(now.getTime() - value * 60 * 60 * 1000);
    case 'd': // days
      return new Date(now.getTime() - value * 24 * 60 * 60 * 1000);
    default:
      throw new Error('Unknown time unit');
  }
}

// Search emails with criteria
async function searchEmails(options) {
  const connection = await connect();

  try {
    const mailbox = options.mailbox || DEFAULT_MAILBOX;
    await connection.openBox(mailbox);

    const criteria = [];

    if (options.unseen) criteria.push('UNSEEN');
    if (options.seen) criteria.push('SEEN');
    if (options.from) criteria.push(['FROM', options.from]);
    if (options.subject) criteria.push(['SUBJECT', options.subject]);
    
    // Handle relative time (--recent 2h)
    if (options.recent) {
      const sinceDate = parseRelativeTime(options.recent);
      criteria.push(['SINCE', sinceDate]);
    } else {
      // Handle absolute dates
      if (options.since) criteria.push(['SINCE', options.since]);
      if (options.before) criteria.push(['BEFORE', options.before]);
    }

    // Default to all if no criteria
    if (criteria.length === 0) criteria.push('ALL');

    const fetchOptions = {
      bodies: [''], // Fetch full body for reliable parsing
      markSeen: false,
    };

    const messages = await connection.search(criteria, fetchOptions);
    const limit = parseInt(options.limit) || 20;
    const results = [];

    for (const item of messages.slice(0, limit)) {
      const all = item.parts.find((p) => p.which === '');

      if (all) {
        // Convert buffer to string for simpleParser
        const bodyStr = typeof all.body === 'string' 
          ? all.body 
          : all.body.toString('utf8');
        
        const parsed = await simpleParser(bodyStr);
        results.push({
          uid: item.attributes.uid,
          from: parsed.from?.text || 'Unknown',
          subject: parsed.subject || '(no subject)',
          date: parsed.date,
          flags: item.attributes.flags,
        });
      }
    }

    return results;
  } finally {
    connection.end();
  }
}

// Mark message(s) as read
async function markAsRead(uids, mailbox = DEFAULT_MAILBOX) {
  const connection = await connect();

  try {
    await connection.openBox(mailbox);
    await connection.addFlags(uids, '\\Seen');
    return { success: true, uids, action: 'marked as read' };
  } finally {
    connection.end();
  }
}

// Mark message(s) as unread
async function markAsUnread(uids, mailbox = DEFAULT_MAILBOX) {
  const connection = await connect();

  try {
    await connection.openBox(mailbox);
    await connection.delFlags(uids, '\\Seen');
    return { success: true, uids, action: 'marked as unread' };
  } finally {
    connection.end();
  }
}

// List all mailboxes
async function listMailboxes() {
  const connection = await connect();

  try {
    const boxes = await connection.getBoxes();
    return formatMailboxTree(boxes);
  } finally {
    connection.end();
  }
}

// Format mailbox tree recursively
function formatMailboxTree(boxes, prefix = '') {
  const result = [];
  for (const [name, info] of Object.entries(boxes)) {
    const fullName = prefix ? `${prefix}${info.delimiter}${name}` : name;
    result.push({
      name: fullName,
      delimiter: info.delimiter,
      attributes: info.attribs,
    });

    if (info.children) {
      result.push(...formatMailboxTree(info.children, fullName));
    }
  }
  return result;
}

// Main CLI handler
async function main() {
  const { command, options, positional } = parseArgs();

  try {
    let result;

    switch (command) {
      case 'check':
        result = await checkEmails(
          options.mailbox || DEFAULT_MAILBOX,
          parseInt(options.limit) || 10,
          options.recent || null
        );
        break;

      case 'fetch':
        if (!positional[0]) {
          throw new Error('UID required: node imap.js fetch <uid>');
        }
        result = await fetchEmail(positional[0], options.mailbox);
        break;

      case 'search':
        result = await searchEmails(options);
        break;

      case 'mark-read':
        if (positional.length === 0) {
          throw new Error('UID(s) required: node imap.js mark-read <uid> [uid2...]');
        }
        result = await markAsRead(positional, options.mailbox);
        break;

      case 'mark-unread':
        if (positional.length === 0) {
          throw new Error('UID(s) required: node imap.js mark-unread <uid> [uid2...]');
        }
        result = await markAsUnread(positional, options.mailbox);
        break;

      case 'list-mailboxes':
        result = await listMailboxes();
        break;

      default:
        console.error('Unknown command:', command);
        console.error('Available commands: check, fetch, search, mark-read, mark-unread, list-mailboxes');
        process.exit(1);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
