// Utility functions for the RTMS meeting assistant
import path from 'path';

/**
 * Sanitize filename to avoid invalid characters
 * Replaces problematic characters with underscores
 * @param {string} name - The filename or path to sanitize
 * @returns {string} - The sanitized filename
 */
export function sanitizeFileName(name) {
  return name.replace(/[<>:"\/\\|?*=\s]/g, '_');
}

/**
 * Get the recordings directory path for a stream, organized by date
 * Format: recordings/YYYY/MM/DD/streamId
 * @param {string} streamId - The stream ID (will be sanitized)
 * @param {Date} [date] - Optional date (defaults to now)
 * @returns {string} - The full path to the recordings directory
 */
export function getRecordingsPath(streamId, date = new Date()) {
  const safeStreamId = sanitizeFileName(streamId);
  const year = date.getFullYear().toString();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return path.join('recordings', year, month, day, safeStreamId);
}
