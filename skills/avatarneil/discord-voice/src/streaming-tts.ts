/**
 * Streaming Text-to-Speech providers
 * 
 * Streams audio chunks as they arrive from the TTS API,
 * reducing time-to-first-audio significantly.
 */

import { Readable, PassThrough } from "node:stream";
import type { DiscordVoiceConfig } from "./config.js";

export interface StreamingTTSResult {
  stream: Readable;
  format: "pcm" | "opus" | "mp3";
  sampleRate: number;
}

export interface StreamingTTSProvider {
  /** 
   * Synthesize text to audio stream
   * Returns a readable stream that emits audio chunks as they arrive
   */
  synthesizeStream(text: string): Promise<StreamingTTSResult>;
  
  /**
   * Check if streaming is supported
   */
  supportsStreaming(): boolean;
}

/**
 * OpenAI Streaming TTS Provider
 * 
 * OpenAI TTS supports streaming responses - we can start playing
 * audio before the full response is received.
 */
export class OpenAIStreamingTTS implements StreamingTTSProvider {
  private apiKey: string;
  private model: string;
  private voice: string;

  constructor(config: DiscordVoiceConfig) {
    this.apiKey = config.openai?.apiKey || process.env.OPENAI_API_KEY || "";
    this.model = config.openai?.ttsModel || "tts-1";
    this.voice = config.ttsVoice || "nova";

    if (!this.apiKey) {
      throw new Error("OpenAI API key required for OpenAI TTS");
    }
  }

  supportsStreaming(): boolean {
    return true;
  }

  async synthesizeStream(text: string): Promise<StreamingTTSResult> {
    const response = await fetch("https://api.openai.com/v1/audio/speech", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: this.model,
        input: text,
        voice: this.voice,
        response_format: "opus", // Best for Discord voice
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`OpenAI TTS error: ${response.status} ${error}`);
    }

    if (!response.body) {
      throw new Error("OpenAI TTS returned no body");
    }

    // Convert web ReadableStream to Node.js Readable
    const nodeStream = Readable.fromWeb(response.body as any);

    return {
      stream: nodeStream,
      format: "opus",
      sampleRate: 48000,
    };
  }
}

/**
 * ElevenLabs Streaming TTS Provider
 * 
 * ElevenLabs supports streaming via their streaming endpoint.
 * Audio chunks are returned as they're generated.
 */
export class ElevenLabsStreamingTTS implements StreamingTTSProvider {
  private apiKey: string;
  private voiceId: string;
  private modelId: string;

  constructor(config: DiscordVoiceConfig) {
    this.apiKey = config.elevenlabs?.apiKey || process.env.ELEVENLABS_API_KEY || "";
    this.voiceId = config.elevenlabs?.voiceId || config.ttsVoice || "21m00Tcm4TlvDq8ikWAM";
    this.modelId = config.elevenlabs?.modelId || "eleven_turbo_v2_5"; // Turbo model is faster

    if (!this.apiKey) {
      throw new Error("ElevenLabs API key required for ElevenLabs TTS");
    }
  }

  supportsStreaming(): boolean {
    return true;
  }

  async synthesizeStream(text: string): Promise<StreamingTTSResult> {
    // Use the streaming endpoint
    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${this.voiceId}/stream`,
      {
        method: "POST",
        headers: {
          "xi-api-key": this.apiKey,
          "Content-Type": "application/json",
          Accept: "audio/mpeg",
        },
        body: JSON.stringify({
          text,
          model_id: this.modelId,
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75,
          },
          optimize_streaming_latency: 3, // 0-4, higher = lower latency but quality tradeoff
        }),
      }
    );

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`ElevenLabs TTS error: ${response.status} ${error}`);
    }

    if (!response.body) {
      throw new Error("ElevenLabs TTS returned no body");
    }

    // Convert web ReadableStream to Node.js Readable
    const nodeStream = Readable.fromWeb(response.body as any);

    return {
      stream: nodeStream,
      format: "mp3",
      sampleRate: 44100,
    };
  }
}

/**
 * Create streaming TTS provider based on config
 */
export function createStreamingTTSProvider(config: DiscordVoiceConfig): StreamingTTSProvider {
  switch (config.ttsProvider) {
    case "elevenlabs":
      return new ElevenLabsStreamingTTS(config);
    case "openai":
    default:
      return new OpenAIStreamingTTS(config);
  }
}

/**
 * Utility to buffer a stream with timeout
 * Useful when we need to wait for minimum data before starting playback
 */
export function bufferStreamWithMinimum(
  source: Readable,
  minBytes: number,
  timeoutMs: number
): Promise<{ buffer: Buffer; remaining: Readable }> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    let totalBytes = 0;
    let resolved = false;

    const timeout = setTimeout(() => {
      if (!resolved && totalBytes > 0) {
        resolved = true;
        // Return what we have
        const buffer = Buffer.concat(chunks);
        resolve({ buffer, remaining: source });
      }
    }, timeoutMs);

    source.on("data", (chunk: Buffer) => {
      if (resolved) return;
      
      chunks.push(chunk);
      totalBytes += chunk.length;

      if (totalBytes >= minBytes) {
        resolved = true;
        clearTimeout(timeout);
        const buffer = Buffer.concat(chunks);
        resolve({ buffer, remaining: source });
      }
    });

    source.on("end", () => {
      if (!resolved) {
        resolved = true;
        clearTimeout(timeout);
        const buffer = Buffer.concat(chunks);
        resolve({ buffer, remaining: source });
      }
    });

    source.on("error", (err) => {
      if (!resolved) {
        resolved = true;
        clearTimeout(timeout);
        reject(err);
      }
    });
  });
}
