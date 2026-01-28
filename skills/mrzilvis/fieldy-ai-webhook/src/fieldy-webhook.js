const fs = require("fs");
const path = require("path");

function getWorkspace(context) {
  // 1. Explicit context/env (most reliable)
  if (context?.workspace) return context.workspace;
  if (process.env.CLAWDBOT_WORKSPACE) return process.env.CLAWDBOT_WORKSPACE;

  // 2. Walk up from script location
  let current = path.dirname(path.resolve(__filename));
  while (current !== path.dirname(current)) {
    // Look for workspace markers
    if (fs.existsSync(path.join(current, ".clawdbot")) || fs.existsSync(path.join(current, "skills"))) {
      return current;
    }
    current = path.dirname(current);
  }

  // 3. Last resort: cwd (but warn about it)
  console.warn("Fieldy: Could not reliably detect workspace, using cwd");
  return process.cwd();
}

module.exports = function (inputData, context) {
  // Path logic MUST be inside the function to use 'context'
  const workspace = getWorkspace(context);
  const logDirInside = path.join(workspace, "fieldy", "transcripts");

  try {
    // --- STEP 1: PARSE INPUT ---
    const rawData = typeof inputData === "string" ? JSON.parse(inputData) : inputData;
    const data = rawData.payload || rawData;

    // Extract text safely
    const transcription = (
      data.transcription ||
      data.transcript ||
      (data.transcriptions && data.transcriptions[0] && data.transcriptions[0].text) ||
      ""
    ).trim();

    // Abort if empty
    if (!transcription) return null;

    // --- STEP 2: LOGGING TO FILE ---
    try {
      const payloadDateStr = data.date || new Date().toISOString();
      const dateObj = new Date(payloadDateStr);
      const safeDateObj = isNaN(dateObj.getTime()) ? new Date() : dateObj;

      const dateFilename = safeDateObj.toISOString().split("T")[0];
      const filePath = path.join(logDirInside, `${dateFilename}.jsonl`);

      // Ensure directory exists
      if (!fs.existsSync(logDirInside)) {
        fs.mkdirSync(logDirInside, { recursive: true });
      }

      const logEntry = JSON.stringify({
        timestamp: payloadDateStr,
        text: transcription,
        speaker: (data.transcriptions && data.transcriptions[0] && data.transcriptions[0].speaker) || "Unknown",
      });

      fs.appendFileSync(filePath, logEntry + "\n");
      console.log(`Fieldy: Logged to ${dateFilename}.jsonl at ${logDirInside}`);
    } catch (fsError) {
      console.error(`Fieldy: Failed to save log to ${logDirInside}:`, fsError);
    }

    // --- STEP 3: WAKE WORD DETECTION ---
    const wakePatterns = [
      /(?:^|\W)(?:hey|hi|hello),?\s+field[yi]e?\W+(.*)/i,
      /(?:^|\W)field[yi]e?\W+(.*)/i,
    ];

    let commandText = null;
    for (const pattern of wakePatterns) {
      const match = transcription.match(pattern);
      if (match) {
        commandText = match[1] ? match[1].trim() : transcription;
        break;
      }
    }

    // --- STEP 4: DECISION ---
    if (commandText) {
      console.log("Fieldy: Wake word detected! Triggering agent.");
      return {
        message: commandText,
        deliver: true,
        name: "FieldyVoice",
      };
    } else {
      return null;
    }
  } catch (error) {
    console.error("Fieldy handler error:", error);
    return null;
  }
};