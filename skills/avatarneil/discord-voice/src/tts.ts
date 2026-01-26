/**
 * Text-to-Speech providers
 */

import type { DiscordVoiceConfig } from "./config.js";

export interface TTSResult {
  audioBuffer: Buffer;
  format: "pcm" | "opus" | "mp3";
  sampleRate: number;
}

export interface TTSProvider {
  synthesize(text: string): Promise<TTSResult>;
}

/**
 * OpenAI TTS Provider
 */
export class OpenAITTS implements TTSProvider {
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

  async synthesize(text: string): Promise<TTSResult> {
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

    const arrayBuffer = await response.arrayBuffer();
    return {
      audioBuffer: Buffer.from(arrayBuffer),
      format: "opus",
      sampleRate: 48000, // Opus from OpenAI is typically 48kHz
    };
  }
}

/**
 * ElevenLabs TTS Provider
 */
export class ElevenLabsTTS implements TTSProvider {
  private apiKey: string;
  private voiceId: string;
  private modelId: string;

  constructor(config: DiscordVoiceConfig) {
    this.apiKey = config.elevenlabs?.apiKey || process.env.ELEVENLABS_API_KEY || "";
    this.voiceId = config.elevenlabs?.voiceId || config.ttsVoice || "21m00Tcm4TlvDq8ikWAM"; // Default: Rachel
    this.modelId = config.elevenlabs?.modelId || "eleven_multilingual_v2";

    if (!this.apiKey) {
      throw new Error("ElevenLabs API key required for ElevenLabs TTS");
    }
  }

  async synthesize(text: string): Promise<TTSResult> {
    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${this.voiceId}`,
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
        }),
      }
    );

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`ElevenLabs TTS error: ${response.status} ${error}`);
    }

    const arrayBuffer = await response.arrayBuffer();
    return {
      audioBuffer: Buffer.from(arrayBuffer),
      format: "mp3",
      sampleRate: 44100,
    };
  }
}

/**
 * Create TTS provider based on config
 */
export function createTTSProvider(config: DiscordVoiceConfig): TTSProvider {
  switch (config.ttsProvider) {
    case "elevenlabs":
      return new ElevenLabsTTS(config);
    case "openai":
    default:
      return new OpenAITTS(config);
  }
}
