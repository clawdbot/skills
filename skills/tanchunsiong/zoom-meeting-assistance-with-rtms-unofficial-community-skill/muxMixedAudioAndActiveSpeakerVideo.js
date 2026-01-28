import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import { getRecordingsPath } from './tool.js';

const runFFmpegCommand = promisify(exec);

// Asynchronous function to mux the first audio and video files
export async function muxMixedAudioAndActiveSpeakerVideo(streamId) {
  const folderPath = getRecordingsPath(streamId);

  if (!fs.existsSync(folderPath)) {
    console.error(`❌ Meeting folder does not exist: ${folderPath}`);
    return;
  }

  const audioPath = path.join(folderPath, 'mixedaudio.wav');
  const videoPath = path.join(folderPath, 'activespeakervideo.mp4');

  if (!fs.existsSync(audioPath) || !fs.existsSync(videoPath)) {
    console.error('❌ Cannot find mixedaudio.wav and/or activespeakervideo.mp4 to mux.');
    return;
  }
  const outputPath = path.join(folderPath, 'final_output.mp4');

  const offsetSeconds = 0.0; // You can adjust this offset
  const command = `ffmpeg -i "${audioPath}" -i "${videoPath}" -itsoffset ${offsetSeconds} -i "${audioPath}" -map 1:v:0 -map 2:a:0 -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 64k -ar 16000 -ac 1 -shortest "${outputPath}"`;

  console.log(`🎥 Muxing activespeakervideo.mp4 + mixedaudio.wav -> final_output.mp4`);

  try {
    await runFFmpegCommand(command);
    console.log('✅ Muxing completed. Output file created:', outputPath);
  } catch (error) {
    console.error('❌ Muxing failed:', error.message);
  }
}
