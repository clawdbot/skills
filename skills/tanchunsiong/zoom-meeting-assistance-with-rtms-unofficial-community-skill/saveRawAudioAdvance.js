import fs from 'fs';
import path from 'path';
import { getRecordingsPath } from './tool.js';

// Cache for open write streams
const writeStreams = new Map();

export function saveRawAudio(chunk, streamId, user_id, timestamp) {

    const recordingsDir = getRecordingsPath(streamId);

    // Build path: recordings/YYYY/MM/DD/{streamId}/{userId}.raw
    // Use "mixedaudio" for user_id 0 (mixed audio stream)
    const fileName = (user_id === 0 || user_id === '0') ? 'mixedaudio' : user_id;
    const filePath = path.join(recordingsDir, `${fileName}.raw`);

    // If the folder doesn't exist yet, create it
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    // Check if a stream already exists for this file
    let stream = writeStreams.get(filePath);
    if (!stream) {
        stream = fs.createWriteStream(filePath, { flags: 'a' }); // append mode
        writeStreams.set(filePath, stream);
    }

    stream.write(chunk);
}

// (Optional) Close all streams when needed
export function closeAllStreams() {
    for (const stream of writeStreams.values()) {
        stream.end();
    }
    writeStreams.clear();
}
