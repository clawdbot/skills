/**
 * Streaming Speech-to-Text via Deepgram WebSocket
 * 
 * Provides real-time transcription as audio streams in,
 * significantly reducing latency compared to batch transcription.
 */

import { EventEmitter } from "node:events";
import WebSocket from "ws";
import type { DiscordVoiceConfig } from "./config.js";

export interface StreamingSTTEvents {
  transcript: (text: string, isFinal: boolean, confidence?: number) => void;
  error: (error: Error) => void;
  close: () => void;
  ready: () => void;
}

export interface StreamingSTTProvider extends EventEmitter {
  on<K extends keyof StreamingSTTEvents>(event: K, listener: StreamingSTTEvents[K]): this;
  emit<K extends keyof StreamingSTTEvents>(event: K, ...args: Parameters<StreamingSTTEvents[K]>): boolean;
  
  /** Send audio chunk to be transcribed */
  sendAudio(chunk: Buffer): void;
  
  /** Signal end of audio stream */
  finalize(): void;
  
  /** Close the connection */
  close(): void;
  
  /** Check if connection is ready */
  isReady(): boolean;
}

/**
 * Deepgram Streaming STT Provider
 * 
 * Uses WebSocket connection for real-time transcription.
 * Supports interim results for ultra-low latency feedback.
 */
export class DeepgramStreamingSTT extends EventEmitter implements StreamingSTTProvider {
  private ws: WebSocket | null = null;
  private apiKey: string;
  private model: string;
  private ready = false;
  private closed = false;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 3;
  private keepAliveInterval: ReturnType<typeof setInterval> | null = null;
  private sampleRate: number;
  private interimResults: boolean;
  private endpointing: number;
  private utteranceEndMs: number;
  
  // Buffer for audio chunks received before connection is ready
  private pendingAudioChunks: Buffer[] = [];
  private maxPendingChunks = 500; // ~5 seconds of audio at 48kHz

  constructor(config: DiscordVoiceConfig, options?: {
    sampleRate?: number;
    interimResults?: boolean;
    endpointing?: number;      // ms of silence to detect end of utterance
    utteranceEndMs?: number;   // ms to wait after utterance end before finalizing
  }) {
    super();
    this.apiKey = config.deepgram?.apiKey || process.env.DEEPGRAM_API_KEY || "";
    this.model = config.deepgram?.model || "nova-2";
    this.sampleRate = options?.sampleRate ?? 48000;
    this.interimResults = options?.interimResults ?? true;
    this.endpointing = options?.endpointing ?? 300;  // 300ms silence detection
    this.utteranceEndMs = options?.utteranceEndMs ?? 1000;

    if (!this.apiKey) {
      throw new Error("Deepgram API key required for streaming STT");
    }

    this.connect();
  }

  private connect(): void {
    if (this.closed) return;

    // Build Deepgram streaming URL with parameters
    const params = new URLSearchParams({
      model: this.model,
      encoding: "linear16",
      sample_rate: this.sampleRate.toString(),
      channels: "1",
      interim_results: this.interimResults.toString(),
      punctuate: "true",
      endpointing: this.endpointing.toString(),
      utterance_end_ms: this.utteranceEndMs.toString(),
      vad_events: "true",
      smart_format: "true",
    });

    const url = `wss://api.deepgram.com/v1/listen?${params}`;

    this.ws = new WebSocket(url, {
      headers: {
        Authorization: `Token ${this.apiKey}`,
      },
    });

    this.ws.on("open", () => {
      this.ready = true;
      this.reconnectAttempts = 0;
      
      // Flush any pending audio chunks that were buffered during connection
      if (this.pendingAudioChunks.length > 0) {
        console.log(`[streaming-stt] Connection ready, flushing ${this.pendingAudioChunks.length} buffered audio chunks`);
        for (const chunk of this.pendingAudioChunks) {
          this.ws!.send(chunk);
        }
        this.pendingAudioChunks = [];
      }
      
      this.emit("ready");
      
      // Start keep-alive pings every 10 seconds
      this.keepAliveInterval = setInterval(() => {
        if (this.ws?.readyState === WebSocket.OPEN) {
          // Send keep-alive message (empty JSON object)
          this.ws.send(JSON.stringify({ type: "KeepAlive" }));
        }
      }, 10000);
    });

    this.ws.on("message", (data: Buffer | string) => {
      try {
        const msg = JSON.parse(data.toString()) as DeepgramMessage;
        this.handleMessage(msg);
      } catch (err) {
        // Ignore parse errors for non-JSON messages
      }
    });

    this.ws.on("close", (code, reason) => {
      this.ready = false;
      this.clearKeepAlive();
      
      if (!this.closed && this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        setTimeout(() => this.connect(), 1000 * this.reconnectAttempts);
      } else {
        this.emit("close");
      }
    });

    this.ws.on("error", (err) => {
      this.emit("error", err);
    });
  }

  private handleMessage(msg: DeepgramMessage): void {
    if (msg.type === "Results" && msg.channel?.alternatives?.[0]) {
      const alt = msg.channel.alternatives[0];
      const text = alt.transcript?.trim();
      
      if (text && text.length > 0) {
        const isFinal = msg.is_final ?? false;
        this.emit("transcript", text, isFinal, alt.confidence);
      }
    } else if (msg.type === "UtteranceEnd") {
      // Utterance ended - can be used to trigger processing
      // The final transcript should have already been emitted
    } else if (msg.type === "SpeechStarted") {
      // Speech detected - could use for barge-in detection
    }
  }

  private clearKeepAlive(): void {
    if (this.keepAliveInterval) {
      clearInterval(this.keepAliveInterval);
      this.keepAliveInterval = null;
    }
  }

  sendAudio(chunk: Buffer): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(chunk);
    } else if (!this.closed) {
      // Buffer audio while connection is establishing
      this.pendingAudioChunks.push(chunk);
      // Prevent unlimited buffering
      if (this.pendingAudioChunks.length > this.maxPendingChunks) {
        this.pendingAudioChunks.shift(); // Drop oldest chunk
      }
    }
  }

  finalize(): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      // Send close stream message to get final results
      this.ws.send(JSON.stringify({ type: "CloseStream" }));
    }
  }

  close(): void {
    this.closed = true;
    this.clearKeepAlive();
    this.pendingAudioChunks = [];
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.ready = false;
  }

  isReady(): boolean {
    return this.ready && this.ws?.readyState === WebSocket.OPEN;
  }

  /**
   * Wait for the connection to be ready (or fail)
   * Returns true if ready, false if failed/closed
   */
  waitForReady(timeoutMs = 5000): Promise<boolean> {
    if (this.isReady()) return Promise.resolve(true);
    if (this.closed) return Promise.resolve(false);

    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        this.off("ready", onReady);
        this.off("close", onClose);
        resolve(false);
      }, timeoutMs);

      const onReady = () => {
        clearTimeout(timeout);
        this.off("close", onClose);
        resolve(true);
      };

      const onClose = () => {
        clearTimeout(timeout);
        this.off("ready", onReady);
        resolve(false);
      };

      this.once("ready", onReady);
      this.once("close", onClose);
    });
  }
}

// Deepgram message types
interface DeepgramMessage {
  type: "Results" | "Metadata" | "UtteranceEnd" | "SpeechStarted" | "Error";
  is_final?: boolean;
  speech_final?: boolean;
  channel?: {
    alternatives?: Array<{
      transcript?: string;
      confidence?: number;
      words?: Array<{
        word: string;
        start: number;
        end: number;
        confidence: number;
      }>;
    }>;
  };
  metadata?: {
    request_id?: string;
    model_info?: {
      name: string;
      version: string;
    };
  };
}

/**
 * Streaming STT Session Manager
 * 
 * Manages per-user streaming STT sessions with automatic
 * lifecycle handling (create on speech start, destroy on silence).
 */
export class StreamingSTTManager {
  private config: DiscordVoiceConfig;
  private sessions: Map<string, DeepgramStreamingSTT> = new Map();
  private pendingTranscripts: Map<string, string> = new Map();
  
  constructor(config: DiscordVoiceConfig) {
    this.config = config;
  }

  /**
   * Get or create a streaming session for a user
   */
  getOrCreateSession(
    userId: string,
    onTranscript: (text: string, isFinal: boolean) => void
  ): DeepgramStreamingSTT {
    let session = this.sessions.get(userId);
    
    if (!session || !session.isReady()) {
      // Clean up old session if exists
      if (session) {
        session.close();
      }

      session = new DeepgramStreamingSTT(this.config, {
        sampleRate: 48000,
        interimResults: true,
        endpointing: 300,
        utteranceEndMs: 1000,
      });

      // Track partial transcripts for this user
      this.pendingTranscripts.set(userId, "");

      session.on("transcript", (text, isFinal, confidence) => {
        if (isFinal) {
          // Accumulate final transcripts
          const pending = this.pendingTranscripts.get(userId) || "";
          const fullText = pending ? `${pending} ${text}` : text;
          this.pendingTranscripts.set(userId, fullText);
        }
        onTranscript(text, isFinal);
      });

      session.on("close", () => {
        this.sessions.delete(userId);
      });

      session.on("error", (err) => {
        console.error(`[streaming-stt] Error for user ${userId}:`, err.message);
      });

      this.sessions.set(userId, session);
    }

    return session;
  }

  /**
   * Send audio to user's session
   * Audio is buffered if connection is still establishing
   */
  sendAudio(userId: string, chunk: Buffer): void {
    const session = this.sessions.get(userId);
    if (session) {
      // sendAudio now handles buffering internally if not ready
      session.sendAudio(chunk);
    }
  }

  /**
   * Finalize and get accumulated transcript for user
   */
  finalizeSession(userId: string): string {
    const session = this.sessions.get(userId);
    if (session) {
      session.finalize();
    }
    
    const transcript = this.pendingTranscripts.get(userId) || "";
    this.pendingTranscripts.delete(userId);
    return transcript;
  }

  /**
   * Close a user's session
   */
  closeSession(userId: string): void {
    const session = this.sessions.get(userId);
    if (session) {
      session.close();
      this.sessions.delete(userId);
    }
    this.pendingTranscripts.delete(userId);
  }

  /**
   * Close all sessions
   */
  closeAll(): void {
    for (const [userId, session] of this.sessions) {
      session.close();
    }
    this.sessions.clear();
    this.pendingTranscripts.clear();
  }
}

/**
 * Create streaming STT provider based on config
 */
export function createStreamingSTTProvider(config: DiscordVoiceConfig): StreamingSTTManager | null {
  if (config.sttProvider !== "deepgram") {
    return null;  // Streaming only supported with Deepgram
  }
  
  return new StreamingSTTManager(config);
}
