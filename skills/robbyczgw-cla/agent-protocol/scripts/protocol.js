/**
 * Agent Protocol - JavaScript/Node.js Library
 * Import this to use agent protocol from your Node.js skills.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const EVENT_DIR = path.join(require('os').homedir(), '.clawdbot', 'events', 'queue');

/**
 * Publish an event to the event bus
 * @param {Object} options - Event options
 * @param {string} options.eventType - Event type (e.g., "research.article_found")
 * @param {string} options.source - Source agent name
 * @param {Object} options.payload - Event payload
 * @param {string} [options.priority] - Priority (low, normal, high)
 * @returns {string} Event ID
 */
async function publishEvent({ eventType, source, payload, priority = 'normal' }) {
  const event = {
    event_id: generateEventId(),
    event_type: eventType,
    source_agent: source,
    timestamp: new Date().toISOString(),
    payload,
    metadata: {}
  };

  if (priority !== 'normal') {
    event.metadata.priority = priority;
  }

  // Ensure directory exists
  if (!fs.existsSync(EVENT_DIR)) {
    fs.mkdirSync(EVENT_DIR, { recursive: true });
  }

  // Write event file
  const eventFile = path.join(EVENT_DIR, `${event.event_id}.json`);
  fs.writeFileSync(eventFile, JSON.stringify(event, null, 2));

  return event.event_id;
}

/**
 * Generate unique event ID
 * @returns {string} Event ID
 */
function generateEventId() {
  const timestamp = new Date().toISOString().replace(/[-:T]/g, '').slice(0, 15);
  const random = Math.random().toString(36).slice(2, 10);
  return `evt_${timestamp}_${random}`;
}

/**
 * Subscribe to events (basic polling implementation)
 * @param {string[]} eventTypes - Event type patterns
 * @param {Function} handler - Handler function (receives event object)
 * @param {number} [pollInterval] - Poll interval in milliseconds
 */
function subscribe(eventTypes, handler, pollInterval = 5000) {
  setInterval(() => {
    const events = getPendingEvents(eventTypes);
    events.forEach(event => {
      try {
        handler(event);
        markProcessed(event.event_id);
      } catch (error) {
        console.error('Handler error:', error);
        markProcessed(event.event_id, false);
      }
    });
  }, pollInterval);
}

/**
 * Get pending events from queue
 * @param {string[]} [eventTypes] - Event type patterns to filter
 * @returns {Object[]} Array of events
 */
function getPendingEvents(eventTypes = null) {
  if (!fs.existsSync(EVENT_DIR)) {
    return [];
  }

  const events = [];
  const files = fs.readdirSync(EVENT_DIR).filter(f => f.endsWith('.json'));

  for (const file of files) {
    try {
      const eventPath = path.join(EVENT_DIR, file);
      const event = JSON.parse(fs.readFileSync(eventPath, 'utf8'));

      // Filter by event type if specified
      if (eventTypes && !matchesEventTypes(event.event_type, eventTypes)) {
        continue;
      }

      events.push(event);
    } catch (error) {
      console.error(`Error reading event ${file}:`, error);
    }
  }

  return events;
}

/**
 * Check if event type matches any pattern
 * @param {string} eventType - Event type
 * @param {string[]} patterns - Patterns (supports wildcards like "research.*")
 * @returns {boolean} True if matches
 */
function matchesEventTypes(eventType, patterns) {
  for (const pattern of patterns) {
    if (pattern.endsWith('.*')) {
      const prefix = pattern.slice(0, -2);
      if (eventType.startsWith(prefix)) {
        return true;
      }
    } else if (pattern === eventType) {
      return true;
    }
  }
  return false;
}

/**
 * Mark event as processed
 * @param {string} eventId - Event ID
 * @param {boolean} [success] - Whether processing was successful
 */
function markProcessed(eventId, success = true) {
  const sourcePath = path.join(EVENT_DIR, `${eventId}.json`);
  if (!fs.existsSync(sourcePath)) {
    return;
  }

  const destDir = path.join(
    require('os').homedir(),
    '.clawdbot',
    'events',
    success ? 'processed' : 'failed'
  );

  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }

  const destPath = path.join(destDir, `${eventId}.json`);
  fs.renameSync(sourcePath, destPath);
}

module.exports = {
  publishEvent,
  subscribe,
  getPendingEvents,
  markProcessed
};
