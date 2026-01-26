/**
 * Discord Voice Connection Manager
 * Handles joining, leaving, listening, and speaking in voice channels
 * 
 * Features:
 * - Barge-in: Stops speaking when user starts talking
 * - Auto-reconnect heartbeat: Keeps connection alive
 * - Streaming STT: Real-time transcription with Deepgram
 */

import {
  joinVoiceChannel,
  createAudioPlayer,
  createAudioResource,
  AudioPlayerStatus,
  VoiceConnectionStatus,
  entersState,
  getVoiceConnection,
  EndBehaviorType,
  StreamType,
  type VoiceConnection,
  type AudioPlayer,
  type AudioReceiveStream,
} from "@discordjs/voice";
import type {
  VoiceChannel,
  StageChannel,
  GuildMember,
  VoiceBasedChannel,
} from "discord.js";
import { Readable, PassThrough } from "stream";
import { pipeline } from "stream/promises";
import * as prism from "prism-media";

import type { DiscordVoiceConfig } from "./config.js";
import { getVadThreshold } from "./config.js";

/**
 * Get RMS threshold based on VAD sensitivity
 * Higher = less sensitive (filters more noise)
 */
function getRmsThreshold(sensitivity: "low" | "medium" | "high"): number {
  switch (sensitivity) {
    case "low":
      return 400;   // More sensitive - picks up quieter speech
    case "high":
      return 1200;  // Less sensitive - requires louder speech, filters more noise
    case "medium":
    default:
      return 800;   // Balanced default
  }
}
import { createSTTProvider, type STTProvider } from "./stt.js";
import { createTTSProvider, type TTSProvider } from "./tts.js";
import { StreamingSTTManager, createStreamingSTTProvider } from "./streaming-stt.js";
import { createStreamingTTSProvider, type StreamingTTSProvider } from "./streaming-tts.js";

interface Logger {
  info(msg: string): void;
  warn(msg: string): void;
  error(msg: string): void;
  debug?(msg: string): void;
}

interface UserAudioState {
  chunks: Buffer[];
  lastActivityMs: number;
  isRecording: boolean;
  silenceTimer?: ReturnType<typeof setTimeout>;
  opusStream?: AudioReceiveStream;
  decoder?: prism.opus.Decoder;
}

export interface VoiceSession {
  guildId: string;
  channelId: string;
  channelName?: string;
  connection: VoiceConnection;
  player: AudioPlayer;
  userAudioStates: Map<string, UserAudioState>;
  speaking: boolean;
  processing: boolean;           // Lock to prevent concurrent processing
  lastSpokeAt?: number;          // Timestamp when bot finished speaking (for cooldown)
  startedSpeakingAt?: number;    // Timestamp when bot started speaking (for echo suppression)
  thinkingPlayer?: AudioPlayer;  // Separate player for thinking sound
  heartbeatInterval?: ReturnType<typeof setInterval>;
  lastHeartbeat?: number;
  reconnecting?: boolean;
}

export class VoiceConnectionManager {
  private sessions: Map<string, VoiceSession> = new Map();
  private config: DiscordVoiceConfig;
  private sttProvider: STTProvider | null = null;
  private streamingSTT: StreamingSTTManager | null = null;
  private ttsProvider: TTSProvider | null = null;
  private streamingTTS: StreamingTTSProvider | null = null;
  private logger: Logger;
  private onTranscript: (userId: string, guildId: string, channelId: string, text: string) => Promise<string>;
  private botUserId: string | null = null;

  // Heartbeat configuration (can be overridden via config.heartbeatIntervalMs)
  private readonly DEFAULT_HEARTBEAT_INTERVAL_MS = 30_000;  // 30 seconds
  private readonly HEARTBEAT_TIMEOUT_MS = 60_000;   // 60 seconds before reconnect
  private readonly MAX_RECONNECT_ATTEMPTS = 3;
  
  private get HEARTBEAT_INTERVAL_MS(): number {
    return this.config.heartbeatIntervalMs ?? this.DEFAULT_HEARTBEAT_INTERVAL_MS;
  }

  constructor(
    config: DiscordVoiceConfig,
    logger: Logger,
    onTranscript: (userId: string, guildId: string, channelId: string, text: string) => Promise<string>,
    botUserId?: string
  ) {
    this.config = config;
    this.logger = logger;
    this.onTranscript = onTranscript;
    this.botUserId = botUserId || null;
  }
  
  /**
   * Set the bot's user ID (for filtering out echo)
   */
  setBotUserId(userId: string): void {
    this.botUserId = userId;
    this.logger.info(`[discord-voice] Bot user ID set to ${userId}`);
  }

  /**
   * Initialize providers lazily
   */
  private ensureProviders(): void {
    if (!this.sttProvider) {
      this.sttProvider = createSTTProvider(this.config);
    }
    if (!this.ttsProvider) {
      this.ttsProvider = createTTSProvider(this.config);
    }
    // Initialize streaming TTS (always, for lower latency)
    if (!this.streamingTTS) {
      this.streamingTTS = createStreamingTTSProvider(this.config);
    }
    // Initialize streaming STT if using Deepgram with streaming enabled
    if (!this.streamingSTT && this.config.sttProvider === "deepgram" && this.config.streamingSTT) {
      this.streamingSTT = createStreamingSTTProvider(this.config);
    }
  }

  /**
   * Join a voice channel
   */
  async join(channel: VoiceBasedChannel): Promise<VoiceSession> {
    const existingSession = this.sessions.get(channel.guildId);
    if (existingSession) {
      if (existingSession.channelId === channel.id) {
        return existingSession;
      }
      // Leave current channel first
      await this.leave(channel.guildId);
    }

    this.ensureProviders();

    const connection = joinVoiceChannel({
      channelId: channel.id,
      guildId: channel.guildId,
      adapterCreator: channel.guild.voiceAdapterCreator,
      selfDeaf: false, // We need to hear users
      selfMute: false,
    });

    const player = createAudioPlayer();
    connection.subscribe(player);

    const session: VoiceSession = {
      guildId: channel.guildId,
      channelId: channel.id,
      channelName: channel.name,
      connection,
      player,
      userAudioStates: new Map(),
      speaking: false,
      processing: false,
      lastHeartbeat: Date.now(),
    };

    this.sessions.set(channel.guildId, session);

    // Wait for the connection to be ready
    try {
      await entersState(connection, VoiceConnectionStatus.Ready, 20_000);
      this.logger.info(`[discord-voice] Joined voice channel ${channel.name} in ${channel.guild.name}`);
    } catch (error) {
      connection.destroy();
      this.sessions.delete(channel.guildId);
      throw new Error(`Failed to join voice channel: ${error}`);
    }

    // Start listening to users
    this.startListening(session);

    // Start heartbeat for connection health monitoring
    this.startHeartbeat(session);

    // Handle connection state changes
    this.setupConnectionHandlers(session, channel);

    return session;
  }

  /**
   * Setup connection event handlers for auto-reconnect
   */
  private setupConnectionHandlers(session: VoiceSession, channel: VoiceBasedChannel): void {
    const connection = session.connection;

    connection.on(VoiceConnectionStatus.Disconnected, async () => {
      if (session.reconnecting) return;
      
      this.logger.warn(`[discord-voice] Disconnected from voice channel in ${channel.guild.name}`);
      
      try {
        // Try to reconnect within 5 seconds
        await Promise.race([
          entersState(connection, VoiceConnectionStatus.Signalling, 5_000),
          entersState(connection, VoiceConnectionStatus.Connecting, 5_000),
        ]);
        this.logger.info(`[discord-voice] Reconnecting to voice channel...`);
      } catch {
        // Connection is not recovering, attempt manual reconnect
        await this.attemptReconnect(session, channel);
      }
    });

    connection.on(VoiceConnectionStatus.Ready, () => {
      session.lastHeartbeat = Date.now();
      session.reconnecting = false;
      this.logger.info(`[discord-voice] Connection ready for ${channel.name}`);
    });

    connection.on("error", (error) => {
      this.logger.error(`[discord-voice] Connection error: ${error.message}`);
    });
  }

  /**
   * Attempt to reconnect to voice channel
   */
  private async attemptReconnect(session: VoiceSession, channel: VoiceBasedChannel, attempt = 1): Promise<void> {
    if (attempt > this.MAX_RECONNECT_ATTEMPTS) {
      this.logger.error(`[discord-voice] Max reconnection attempts reached, giving up`);
      await this.leave(session.guildId);
      return;
    }

    session.reconnecting = true;
    this.logger.info(`[discord-voice] Reconnection attempt ${attempt}/${this.MAX_RECONNECT_ATTEMPTS}`);

    try {
      // Destroy old connection
      session.connection.destroy();

      // Wait before reconnecting (exponential backoff)
      await new Promise(resolve => setTimeout(resolve, 1000 * attempt));

      // Create new connection
      const newConnection = joinVoiceChannel({
        channelId: channel.id,
        guildId: channel.guildId,
        adapterCreator: channel.guild.voiceAdapterCreator,
        selfDeaf: false,
        selfMute: false,
      });

      const newPlayer = createAudioPlayer();
      newConnection.subscribe(newPlayer);

      // Update session
      session.connection = newConnection;
      session.player = newPlayer;

      // Wait for ready
      await entersState(newConnection, VoiceConnectionStatus.Ready, 20_000);
      
      session.reconnecting = false;
      session.lastHeartbeat = Date.now();
      
      // Restart listening
      this.startListening(session);
      
      // Setup handlers for new connection
      this.setupConnectionHandlers(session, channel);
      
      this.logger.info(`[discord-voice] Reconnected successfully`);
    } catch (error) {
      this.logger.error(`[discord-voice] Reconnection failed: ${error instanceof Error ? error.message : String(error)}`);
      await this.attemptReconnect(session, channel, attempt + 1);
    }
  }

  /**
   * Start heartbeat monitoring for session
   */
  private startHeartbeat(session: VoiceSession): void {
    // Clear any existing heartbeat
    if (session.heartbeatInterval) {
      clearInterval(session.heartbeatInterval);
    }

    session.heartbeatInterval = setInterval(() => {
      const now = Date.now();
      const connectionState = session.connection.state.status;
      
      // Update heartbeat if connection is healthy
      if (connectionState === VoiceConnectionStatus.Ready) {
        session.lastHeartbeat = now;
        this.logger.debug?.(`[discord-voice] Heartbeat OK for guild ${session.guildId}`);
      } else if (session.lastHeartbeat && (now - session.lastHeartbeat > this.HEARTBEAT_TIMEOUT_MS)) {
        // Connection has been unhealthy for too long
        this.logger.warn(`[discord-voice] Heartbeat timeout, connection state: ${connectionState}`);
        
        // Don't attempt reconnect if already doing so
        if (!session.reconnecting) {
          // Trigger reconnection by destroying and rejoining
          this.logger.info(`[discord-voice] Triggering reconnection due to heartbeat timeout`);
          session.connection.destroy();
        }
      }
    }, this.HEARTBEAT_INTERVAL_MS);
  }

  /**
   * Leave a voice channel
   */
  async leave(guildId: string): Promise<boolean> {
    const session = this.sessions.get(guildId);
    if (!session) {
      return false;
    }

    // Clear heartbeat
    if (session.heartbeatInterval) {
      clearInterval(session.heartbeatInterval);
    }

    // Clear all user timers and streams
    for (const state of session.userAudioStates.values()) {
      if (state.silenceTimer) {
        clearTimeout(state.silenceTimer);
      }
      if (state.opusStream) {
        state.opusStream.destroy();
      }
      if (state.decoder) {
        state.decoder.destroy();
      }
    }

    // Close streaming STT sessions
    if (this.streamingSTT) {
      for (const userId of session.userAudioStates.keys()) {
        this.streamingSTT.closeSession(userId);
      }
    }

    session.connection.destroy();
    this.sessions.delete(guildId);
    this.logger.info(`[discord-voice] Left voice channel in guild ${guildId}`);
    return true;
  }

  /**
   * Start listening to voice in the channel
   */
  private startListening(session: VoiceSession): void {
    const receiver = session.connection.receiver;

    receiver.speaking.on("start", (userId: string) => {
      // ═══════════════════════════════════════════════════════════════
      // ECHO FILTER: Ignore speech events from the bot itself
      // This is the primary defense against echo-triggered barge-in
      // ═══════════════════════════════════════════════════════════════
      if (this.botUserId && userId === this.botUserId) {
        this.logger.debug?.(`[discord-voice] Ignoring speech from bot itself (echo filter)`);
        return;
      }
      
      if (!this.isUserAllowed(userId)) {
        return;
      }

      // Ignore audio during cooldown period (prevents residual echo)
      const SPEAK_COOLDOWN_MS = 500;
      if (session.lastSpokeAt && (Date.now() - session.lastSpokeAt) < SPEAK_COOLDOWN_MS) {
        this.logger.debug?.(`[discord-voice] Ignoring speech during cooldown (likely residual echo)`);
        return;
      }

      this.logger.debug?.(`[discord-voice] User ${userId} started speaking`);
      
      // ═══════════════════════════════════════════════════════════════
      // BARGE-IN: If we're speaking and a REAL user starts talking, stop
      // Now that we filter out bot's own userId, we can safely do barge-in
      // ═══════════════════════════════════════════════════════════════
      if (session.speaking) {
        if (this.config.bargeIn) {
          this.logger.info(`[discord-voice] Barge-in detected from user ${userId}! Stopping speech.`);
          this.stopSpeaking(session);
          session.lastSpokeAt = Date.now();
        }
        // Clear streaming transcripts and wait for next speech event
        if (this.streamingSTT) {
          this.streamingSTT.closeSession(userId);
        }
        return;
      }
      
      if (session.processing) {
        // While processing a request, don't start new recordings
        if (this.streamingSTT) {
          this.streamingSTT.closeSession(userId);
        }
        this.logger.debug?.(`[discord-voice] Ignoring speech while processing`);
        return;
      }

      let state = session.userAudioStates.get(userId);
      if (!state) {
        state = {
          chunks: [],
          lastActivityMs: Date.now(),
          isRecording: false,
        };
        session.userAudioStates.set(userId, state);
      }

      // Clear any existing silence timer
      if (state.silenceTimer) {
        clearTimeout(state.silenceTimer);
        state.silenceTimer = undefined;
      }

      if (!state.isRecording) {
        state.isRecording = true;
        state.chunks = [];
        this.startRecording(session, userId);
      }

      state.lastActivityMs = Date.now();
    });

    receiver.speaking.on("end", (userId: string) => {
      if (!this.isUserAllowed(userId)) {
        return;
      }

      this.logger.debug?.(`[discord-voice] User ${userId} stopped speaking`);
      
      const state = session.userAudioStates.get(userId);
      if (!state || !state.isRecording) {
        return;
      }

      state.lastActivityMs = Date.now();

      // Set silence timer to process the recording
      state.silenceTimer = setTimeout(async () => {
        if (state.isRecording && state.chunks.length > 0) {
          state.isRecording = false;
          
          // Clean up streams
          if (state.opusStream) {
            state.opusStream.destroy();
            state.opusStream = undefined;
          }
          if (state.decoder) {
            state.decoder.destroy();
            state.decoder = undefined;
          }
          
          await this.processRecording(session, userId, state.chunks);
          state.chunks = [];
        }
      }, this.config.silenceThresholdMs);
    });
  }

  /**
   * Stop any current speech output (for barge-in)
   */
  private stopSpeaking(session: VoiceSession): void {
    // Stop main player
    if (session.player.state.status !== AudioPlayerStatus.Idle) {
      session.player.stop(true);
    }
    
    // Stop thinking player if active
    if (session.thinkingPlayer && session.thinkingPlayer.state.status !== AudioPlayerStatus.Idle) {
      session.thinkingPlayer.stop(true);
      session.thinkingPlayer.removeAllListeners();
      session.thinkingPlayer = undefined;
    }

    session.speaking = false;
  }

  /**
   * Start recording audio from a user
   */
  private startRecording(session: VoiceSession, userId: string): void {
    const state = session.userAudioStates.get(userId);
    if (!state) return;

    const opusStream = session.connection.receiver.subscribe(userId, {
      end: {
        behavior: EndBehaviorType.AfterSilence,
        duration: this.config.silenceThresholdMs,
      },
    });

    state.opusStream = opusStream;

    // Decode Opus to PCM
    const decoder = new prism.opus.Decoder({
      rate: 48000,
      channels: 1,
      frameSize: 960,
    });

    state.decoder = decoder;
    opusStream.pipe(decoder);

    // If streaming STT is available and enabled, use it
    const useStreaming = this.streamingSTT && this.config.sttProvider === "deepgram" && this.config.streamingSTT;
    
    if (useStreaming && this.streamingSTT) {
      // Create streaming session for this user
      const streamingSession = this.streamingSTT.getOrCreateSession(userId, (text, isFinal) => {
        if (isFinal) {
          this.logger.debug?.(`[discord-voice] Streaming transcript (final): "${text}"`);
        } else {
          this.logger.debug?.(`[discord-voice] Streaming transcript (interim): "${text}"`);
        }
      });

      decoder.on("data", (chunk: Buffer) => {
        if (state.isRecording) {
          // Send to streaming STT
          this.streamingSTT?.sendAudio(userId, chunk);
          
          // Also buffer for fallback/debugging
          state.chunks.push(chunk);
          state.lastActivityMs = Date.now();

          // Check max recording length
          const totalSize = state.chunks.reduce((sum, c) => sum + c.length, 0);
          const durationMs = (totalSize / 2) / 48; // 16-bit samples at 48kHz
          if (durationMs >= this.config.maxRecordingMs) {
            this.logger.debug?.(`[discord-voice] Max recording length reached for user ${userId}`);
            state.isRecording = false;
            this.processRecording(session, userId, state.chunks);
            state.chunks = [];
          }
        }
      });
    } else {
      // Batch mode - just buffer audio
      decoder.on("data", (chunk: Buffer) => {
        if (state.isRecording) {
          state.chunks.push(chunk);
          state.lastActivityMs = Date.now();

          // Check max recording length
          const totalSize = state.chunks.reduce((sum, c) => sum + c.length, 0);
          const durationMs = (totalSize / 2) / 48; // 16-bit samples at 48kHz
          if (durationMs >= this.config.maxRecordingMs) {
            this.logger.debug?.(`[discord-voice] Max recording length reached for user ${userId}`);
            state.isRecording = false;
            this.processRecording(session, userId, state.chunks);
            state.chunks = [];
          }
        }
      });
    }

    decoder.on("end", () => {
      this.logger.debug?.(`[discord-voice] Decoder stream ended for user ${userId}`);
    });

    decoder.on("error", (error: Error) => {
      this.logger.error(`[discord-voice] Decoder error for user ${userId}: ${error.message}`);
    });
  }

  /**
   * Process recorded audio through STT and get response
   */
  private async processRecording(session: VoiceSession, userId: string, chunks: Buffer[]): Promise<void> {
    if (!this.sttProvider || !this.ttsProvider) {
      return;
    }

    // Skip if already speaking (prevents overlapping responses)
    if (session.speaking) {
      this.logger.debug?.(`[discord-voice] Skipping processing - already speaking`);
      return;
    }

    // Skip if already processing another request (prevents duplicate responses)
    if (session.processing) {
      this.logger.debug?.(`[discord-voice] Skipping processing - already processing another request`);
      return;
    }

    // Cooldown after speaking to prevent echo/accidental triggers (500ms)
    const SPEAK_COOLDOWN_MS = 500;
    if (session.lastSpokeAt && (Date.now() - session.lastSpokeAt) < SPEAK_COOLDOWN_MS) {
      this.logger.debug?.(`[discord-voice] Skipping processing - in cooldown period after speaking`);
      return;
    }

    const audioBuffer = Buffer.concat(chunks);
    
    // Skip very short recordings (likely noise) - check BEFORE setting processing lock
    const durationMs = (audioBuffer.length / 2) / 48; // 16-bit samples at 48kHz
    if (durationMs < this.config.minAudioMs) {
      this.logger.debug?.(`[discord-voice] Skipping short recording (${Math.round(durationMs)}ms < ${this.config.minAudioMs}ms) for user ${userId}`);
      return;
    }

    // Calculate RMS amplitude to filter out quiet sounds (keystrokes, background noise)
    const rms = this.calculateRMS(audioBuffer);
    const minRMS = getRmsThreshold(this.config.vadSensitivity);
    if (rms < minRMS) {
      this.logger.debug?.(`[discord-voice] Skipping quiet audio (RMS ${Math.round(rms)} < ${minRMS}) for user ${userId}`);
      return;
    }

    // Set processing lock AFTER passing all filters
    session.processing = true;

    this.logger.info(`[discord-voice] Processing ${Math.round(durationMs)}ms of audio (RMS: ${Math.round(rms)}) from user ${userId}`);

    try {
      let transcribedText: string;

      // Check if we have streaming transcript available
      if (this.streamingSTT && this.config.sttProvider === "deepgram" && this.config.streamingSTT) {
        // Get accumulated transcript from streaming session
        transcribedText = this.streamingSTT.finalizeSession(userId);
        
        // Fallback to batch if streaming didn't capture anything
        if (!transcribedText || transcribedText.trim().length === 0) {
          this.logger.debug?.(`[discord-voice] Streaming empty, falling back to batch STT`);
          const sttResult = await this.sttProvider.transcribe(audioBuffer, 48000);
          transcribedText = sttResult.text;
        }
      } else {
        // Batch transcription
        const sttResult = await this.sttProvider.transcribe(audioBuffer, 48000);
        transcribedText = sttResult.text;
      }
      
      if (!transcribedText || transcribedText.trim().length === 0) {
        this.logger.debug?.(`[discord-voice] Empty transcription for user ${userId}`);
        session.processing = false;
        return;
      }

      this.logger.info(`[discord-voice] Transcribed: "${transcribedText}"`);

      // Play looping thinking sound while processing
      const stopThinking = await this.startThinkingLoop(session);

      let response: string;
      try {
        // Get response from agent
        response = await this.onTranscript(userId, session.guildId, session.channelId, transcribedText);
      } finally {
        // Always stop thinking sound, even on error
        stopThinking();
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      
      if (!response || response.trim().length === 0) {
        session.processing = false;
        return;
      }

      // Ensure main player is subscribed before speaking
      session.connection.subscribe(session.player);
      
      // Synthesize and play response
      await this.speak(session.guildId, response);
    } catch (error) {
      this.logger.error(`[discord-voice] Error processing audio: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      session.processing = false;
    }
  }

  /**
   * Speak text in the voice channel
   */
  async speak(guildId: string, text: string): Promise<void> {
    const session = this.sessions.get(guildId);
    if (!session) {
      throw new Error("Not connected to voice channel");
    }

    this.ensureProviders();

    if (!this.streamingTTS && !this.ttsProvider) {
      throw new Error("TTS provider not initialized");
    }

    session.speaking = true;
    session.startedSpeakingAt = Date.now();

    try {
      this.logger.info(`[discord-voice] Speaking: "${text.substring(0, 50)}${text.length > 50 ? "..." : ""}"`);
      
      let resource;

      // Try streaming TTS first (lower latency)
      if (this.streamingTTS) {
        try {
          const streamResult = await this.streamingTTS.synthesizeStream(text);
          
          // Create audio resource from stream
          if (streamResult.format === "opus") {
            resource = createAudioResource(streamResult.stream, {
              inputType: StreamType.OggOpus,
            });
          } else {
            // For mp3, the audio player will transcode
            resource = createAudioResource(streamResult.stream);
          }
          
          this.logger.debug?.(`[discord-voice] Using streaming TTS`);
        } catch (streamError) {
          this.logger.warn(`[discord-voice] Streaming TTS failed, falling back to buffered: ${streamError instanceof Error ? streamError.message : String(streamError)}`);
          // Fall through to buffered TTS
        }
      }

      // Fallback to buffered TTS
      if (!resource && this.ttsProvider) {
        const ttsResult = await this.ttsProvider.synthesize(text);
        
        if (ttsResult.format === "opus") {
          resource = createAudioResource(Readable.from(ttsResult.audioBuffer), {
            inputType: StreamType.OggOpus,
          });
        } else {
          resource = createAudioResource(Readable.from(ttsResult.audioBuffer));
        }
        
        this.logger.debug?.(`[discord-voice] Using buffered TTS`);
      }

      if (!resource) {
        throw new Error("Failed to create audio resource");
      }

      session.player.play(resource);

      // Wait for playback to finish
      await new Promise<void>((resolve) => {
        const onIdle = () => {
          session.speaking = false;
          session.lastSpokeAt = Date.now(); // Set cooldown timestamp
          session.player.off(AudioPlayerStatus.Idle, onIdle);
          session.player.off("error", onError);
          resolve();
        };
        
        const onError = (error: Error) => {
          this.logger.error(`[discord-voice] Playback error: ${error.message}`);
          session.speaking = false;
          session.lastSpokeAt = Date.now(); // Set cooldown timestamp
          session.player.off(AudioPlayerStatus.Idle, onIdle);
          session.player.off("error", onError);
          resolve();
        };

        session.player.on(AudioPlayerStatus.Idle, onIdle);
        session.player.on("error", onError);
      });
    } catch (error) {
      session.speaking = false;
      session.lastSpokeAt = Date.now(); // Set cooldown timestamp
      throw error;
    }
  }

  /**
   * Start looping thinking sound, returns stop function
   */
  private async startThinkingLoop(session: VoiceSession): Promise<() => void> {
    let stopped = false;
    
    try {
      const fs = await import("node:fs");
      const path = await import("node:path");
      const { fileURLToPath } = await import("node:url");
      
      const __dirname = path.dirname(fileURLToPath(import.meta.url));
      const thinkingPath = path.join(__dirname, "..", "assets", "thinking.mp3");
      
      if (!fs.existsSync(thinkingPath)) {
        return () => {};
      }

      const audioData = fs.readFileSync(thinkingPath);
      
      // Create separate player for thinking sound
      const thinkingPlayer = createAudioPlayer();
      session.thinkingPlayer = thinkingPlayer;
      session.connection.subscribe(thinkingPlayer);

      const playLoop = () => {
        if (stopped || !thinkingPlayer) return;
        const resource = createAudioResource(Readable.from(Buffer.from(audioData)), {
          inlineVolume: true,
        });
        resource.volume?.setVolume(0.7);
        thinkingPlayer.play(resource);
      };

      thinkingPlayer.on(AudioPlayerStatus.Idle, playLoop);
      playLoop(); // Start first play

      return () => {
        stopped = true;
        if (thinkingPlayer) {
          thinkingPlayer.removeAllListeners();
          thinkingPlayer.stop(true);
        }
        session.thinkingPlayer = undefined;
        // Re-subscribe main player immediately
        session.connection.subscribe(session.player);
      };
    } catch (error) {
      this.logger.debug?.(`[discord-voice] Error starting thinking loop: ${error instanceof Error ? error.message : String(error)}`);
      return () => {
        session.thinkingPlayer = undefined;
        session.connection.subscribe(session.player);
      };
    }
  }

  /**
   * Play thinking sound once (simple version - uses main player, no loop)
   */
  private async playThinkingSoundSimple(session: VoiceSession): Promise<void> {
    try {
      const fs = await import("node:fs");
      const path = await import("node:path");
      const { fileURLToPath } = await import("node:url");
      
      const __dirname = path.dirname(fileURLToPath(import.meta.url));
      const thinkingPath = path.join(__dirname, "..", "assets", "thinking.mp3");
      
      if (!fs.existsSync(thinkingPath)) {
        return;
      }

      const audioBuffer = fs.readFileSync(thinkingPath);
      const resource = createAudioResource(Readable.from(audioBuffer), {
        inlineVolume: true,
      });
      resource.volume?.setVolume(0.5);
      
      session.player.play(resource);
      
      // Don't wait for it to finish - let it play while processing
      // The response TTS will interrupt it naturally
    } catch (error) {
      this.logger.debug?.(`[discord-voice] Error playing thinking sound: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Calculate RMS (Root Mean Square) amplitude of audio buffer
   * Used to filter out quiet sounds like keystrokes and background noise
   */
  private calculateRMS(audioBuffer: Buffer): number {
    // Audio is 16-bit signed PCM
    const samples = audioBuffer.length / 2;
    if (samples === 0) return 0;

    let sumSquares = 0;
    for (let i = 0; i < audioBuffer.length; i += 2) {
      const sample = audioBuffer.readInt16LE(i);
      sumSquares += sample * sample;
    }

    return Math.sqrt(sumSquares / samples);
  }

  /**
   * Check if a user is allowed to use voice
   */
  private isUserAllowed(userId: string): boolean {
    if (this.config.allowedUsers.length === 0) {
      return true;
    }
    return this.config.allowedUsers.includes(userId);
  }

  /**
   * Get session for a guild
   */
  getSession(guildId: string): VoiceSession | undefined {
    return this.sessions.get(guildId);
  }

  /**
   * Get all active sessions
   */
  getAllSessions(): VoiceSession[] {
    return Array.from(this.sessions.values());
  }

  /**
   * Destroy all connections
   */
  async destroy(): Promise<void> {
    // Close streaming STT
    if (this.streamingSTT) {
      this.streamingSTT.closeAll();
    }

    const guildIds = Array.from(this.sessions.keys());
    for (const guildId of guildIds) {
      await this.leave(guildId);
    }
  }
}
