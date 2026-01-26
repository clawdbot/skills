/**
 * Discord Voice Plugin for Clawdbot
 * 
 * Enables real-time voice conversations in Discord voice channels.
 * 
 * Features:
 * - Join/leave voice channels via slash commands (/voice join, /voice leave)
 * - Listen to user speech with VAD (Voice Activity Detection)
 * - Speech-to-text via Whisper API or Deepgram
 * - Routes transcribed text through Clawdbot agent
 * - Text-to-speech via OpenAI or ElevenLabs
 * - Plays audio responses back to the voice channel
 */

import crypto from "node:crypto";
import { Type } from "@sinclair/typebox";
import { Client, GatewayIntentBits, type VoiceBasedChannel, type GuildMember } from "discord.js";

import { parseConfig, type DiscordVoiceConfig } from "./src/config.js";
import { VoiceConnectionManager } from "./src/voice-connection.js";
import { loadCoreAgentDeps, type CoreConfig } from "./src/core-bridge.js";

interface PluginApi {
  pluginConfig: unknown;
  config: unknown;
  logger: {
    info(msg: string): void;
    warn(msg: string): void;
    error(msg: string): void;
    debug?(msg: string): void;
  };
  runtime: {
    discord?: {
      getClient(accountId?: string): Client | null;
    };
    agent?: {
      chat(params: {
        sessionKey: string;
        message: string;
        channel?: string;
        senderId?: string;
      }): Promise<{ text: string }>;
    };
  };
  registerGatewayMethod(
    name: string,
    handler: (ctx: { params: unknown; respond: (ok: boolean, payload?: unknown) => void }) => void | Promise<void>
  ): void;
  registerTool(tool: {
    name: string;
    label: string;
    description: string;
    parameters: unknown;
    execute: (toolCallId: string, params: unknown) => Promise<{
      content: Array<{ type: string; text: string }>;
      details?: unknown;
    }>;
  }): void;
  registerService(service: {
    id: string;
    start: () => Promise<void> | void;
    stop: () => Promise<void> | void;
  }): void;
  registerCli(
    register: (ctx: { program: unknown }) => void,
    opts?: { commands: string[] }
  ): void;
}

const VoiceToolSchema = Type.Union([
  Type.Object({
    action: Type.Literal("join"),
    channelId: Type.String({ description: "Voice channel ID to join" }),
    guildId: Type.Optional(Type.String({ description: "Guild ID (optional if in guild context)" })),
  }),
  Type.Object({
    action: Type.Literal("leave"),
    guildId: Type.Optional(Type.String({ description: "Guild ID to leave voice in (optional)" })),
  }),
  Type.Object({
    action: Type.Literal("speak"),
    text: Type.String({ description: "Text to speak in the voice channel" }),
    guildId: Type.Optional(Type.String({ description: "Guild ID (optional)" })),
  }),
  Type.Object({
    action: Type.Literal("status"),
  }),
]);

const discordVoicePlugin = {
  id: "discord-voice",
  name: "Discord Voice",
  description: "Real-time voice conversations in Discord voice channels",

  configSchema: {
    parse(value: unknown): DiscordVoiceConfig {
      return parseConfig(value);
    },
  },

  register(api: PluginApi) {
    const cfg = parseConfig(api.pluginConfig);
    let voiceManager: VoiceConnectionManager | null = null;
    let discordClient: Client | null = null;
    let clientReady = false;

    if (!cfg.enabled) {
      api.logger.info("[discord-voice] Plugin disabled");
      return;
    }

    // Get Discord token from main config
    const mainConfig = api.config as { discord?: { token?: string }, channels?: { discord?: { token?: string } } };
    const discordToken = mainConfig?.channels?.discord?.token || mainConfig?.discord?.token;
    
    if (!discordToken) {
      api.logger.error("[discord-voice] No Discord token found in config. Plugin requires discord.token to be configured.");
      return;
    }

    // Create our own Discord client with voice intents
    discordClient = new Client({
      intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildVoiceStates,
        GatewayIntentBits.GuildMessages,
      ],
    });

    discordClient.once("ready", async () => {
      clientReady = true;
      api.logger.info(`[discord-voice] Discord client ready as ${discordClient?.user?.tag}`);
      
      // Set bot user ID on voice manager for echo filtering
      if (discordClient?.user?.id && voiceManager) {
        voiceManager.setBotUserId(discordClient.user.id);
      }
      
      // Auto-join channel if configured
      if (cfg.autoJoinChannel) {
        try {
          api.logger.info(`[discord-voice] Auto-joining channel ${cfg.autoJoinChannel}`);
          // Wait a moment for everything to initialize
          await new Promise(resolve => setTimeout(resolve, 2000));
          
          const channel = await discordClient!.channels.fetch(cfg.autoJoinChannel);
          if (channel && channel.isVoiceBased()) {
            const vm = ensureVoiceManager();
            await vm.join(channel as VoiceBasedChannel);
            api.logger.info(`[discord-voice] Auto-joined voice channel: ${channel.name}`);
          } else {
            api.logger.warn(`[discord-voice] Auto-join channel ${cfg.autoJoinChannel} is not a voice channel`);
          }
        } catch (error) {
          api.logger.error(`[discord-voice] Failed to auto-join: ${error instanceof Error ? error.message : String(error)}`);
        }
      }
    });

    discordClient.login(discordToken).catch((err) => {
      api.logger.error(`[discord-voice] Failed to login: ${err instanceof Error ? err.message : String(err)}`);
    });

    /**
     * Handle transcribed speech - route to agent and get response
     */
    async function handleTranscript(
      userId: string,
      guildId: string,
      channelId: string,
      text: string
    ): Promise<string> {
      api.logger.info(`[discord-voice] Processing transcript from ${userId}: "${text}"`);

      try {
        const deps = await loadCoreAgentDeps();
        if (!deps) {
          api.logger.error("[discord-voice] Could not load core dependencies");
          return "I'm having trouble connecting to my brain right now.";
        }

        const coreConfig = api.config as CoreConfig;
        const agentId = "main";
        
        // Build session key based on guild
        const sessionKey = `discord:voice:${guildId}`;
        
        // Resolve paths
        const storePath = deps.resolveStorePath(coreConfig.session?.store, { agentId });
        const agentDir = deps.resolveAgentDir(coreConfig, agentId);
        const workspaceDir = deps.resolveAgentWorkspaceDir(coreConfig, agentId);

        // Ensure workspace exists
        await deps.ensureAgentWorkspace({ dir: workspaceDir });

        // Load or create session entry
        const sessionStore = deps.loadSessionStore(storePath);
        const now = Date.now();
        type SessionEntry = { sessionId: string; updatedAt: number };
        let sessionEntry = sessionStore[sessionKey] as SessionEntry | undefined;

        if (!sessionEntry) {
          sessionEntry = {
            sessionId: crypto.randomUUID(),
            updatedAt: now,
          };
          sessionStore[sessionKey] = sessionEntry;
          await deps.saveSessionStore(storePath, sessionStore);
        }

        const sessionId = sessionEntry.sessionId;
        const sessionFile = deps.resolveSessionFilePath(sessionId, sessionEntry, { agentId });

        // Resolve model - use voice-specific model if configured, otherwise default
        const modelRef = cfg.model || `${deps.DEFAULT_PROVIDER}/${deps.DEFAULT_MODEL}`;
        const slashIndex = modelRef.indexOf("/");
        const provider = slashIndex === -1 ? deps.DEFAULT_PROVIDER : modelRef.slice(0, slashIndex);
        const model = slashIndex === -1 ? modelRef : modelRef.slice(slashIndex + 1);

        // Resolve thinking level - use voice-specific level if configured (default to "off" for speed)
        const thinkLevel = cfg.thinkLevel || "off";

        // Resolve agent identity
        const identity = deps.resolveAgentIdentity(coreConfig, agentId);
        const agentName = identity?.name?.trim() || "assistant";

        const extraSystemPrompt = `You are ${agentName}, speaking in a Discord voice channel. Keep responses brief and conversational (1-2 sentences max). Be natural and friendly. You have access to all your normal tools and skills. The user's Discord ID is ${userId}.`;

        const timeoutMs = deps.resolveAgentTimeoutMs({ cfg: coreConfig });
        const runId = `discord-voice:${guildId}:${Date.now()}`;

        const result = await deps.runEmbeddedPiAgent({
          sessionId,
          sessionKey,
          messageProvider: "discord",
          sessionFile,
          workspaceDir,
          config: coreConfig,
          prompt: text,
          provider,
          model,
          thinkLevel,
          verboseLevel: "off",
          timeoutMs,
          runId,
          // lane: "discord-voice",  // Removed - was possibly restricting tool access
          extraSystemPrompt,
          agentDir,
        });

        // Extract text from payloads
        const texts = (result.payloads ?? [])
          .filter((p) => p.text && !p.isError)
          .map((p) => p.text?.trim())
          .filter(Boolean);

        return texts.join(" ") || "";
      } catch (error) {
        api.logger.error(`[discord-voice] Agent chat error: ${error instanceof Error ? error.message : String(error)}`);
        return "I'm sorry, I encountered an error processing your request.";
      }
    }

    /**
     * Ensure voice manager is initialized
     */
    function ensureVoiceManager(): VoiceConnectionManager {
      if (!voiceManager) {
        const botUserId = discordClient?.user?.id;
        voiceManager = new VoiceConnectionManager(cfg, api.logger, handleTranscript, botUserId);
      }
      return voiceManager;
    }

    /**
     * Get Discord client
     */
    function getDiscordClient(): Client | null {
      if (!clientReady) {
        api.logger.warn("[discord-voice] Discord client not ready yet");
        return null;
      }
      return discordClient;
    }

    // Register Gateway RPC methods
    api.registerGatewayMethod("discord-voice.join", async ({ params, respond }) => {
      try {
        const p = params as { channelId?: string; guildId?: string } | null;
        const channelId = p?.channelId;
        const guildId = p?.guildId;

        if (!channelId) {
          respond(false, { error: "channelId required" });
          return;
        }

        const client = getDiscordClient();
        if (!client) {
          respond(false, { error: "Discord client not available" });
          return;
        }

        const channel = await client.channels.fetch(channelId);
        if (!channel || !("guild" in channel) || !channel.isVoiceBased()) {
          respond(false, { error: "Invalid voice channel" });
          return;
        }

        const vm = ensureVoiceManager();
        const session = await vm.join(channel as VoiceBasedChannel);
        
        respond(true, {
          joined: true,
          guildId: session.guildId,
          channelId: session.channelId,
        });
      } catch (error) {
        respond(false, { error: error instanceof Error ? error.message : String(error) });
      }
    });

    api.registerGatewayMethod("discord-voice.leave", async ({ params, respond }) => {
      try {
        const p = params as { guildId?: string } | null;
        let guildId = p?.guildId;

        const vm = ensureVoiceManager();
        
        // If no guildId provided, leave all
        if (!guildId) {
          const sessions = vm.getAllSessions();
          if (sessions.length === 0) {
            respond(true, { left: false, reason: "Not in any voice channel" });
            return;
          }
          guildId = sessions[0].guildId;
        }

        const left = await vm.leave(guildId);
        respond(true, { left, guildId });
      } catch (error) {
        respond(false, { error: error instanceof Error ? error.message : String(error) });
      }
    });

    api.registerGatewayMethod("discord-voice.speak", async ({ params, respond }) => {
      try {
        const p = params as { text?: string; guildId?: string } | null;
        const text = p?.text;
        let guildId = p?.guildId;

        if (!text) {
          respond(false, { error: "text required" });
          return;
        }

        const vm = ensureVoiceManager();
        
        if (!guildId) {
          const sessions = vm.getAllSessions();
          if (sessions.length === 0) {
            respond(false, { error: "Not in any voice channel" });
            return;
          }
          guildId = sessions[0].guildId;
        }

        await vm.speak(guildId, text);
        respond(true, { spoken: true });
      } catch (error) {
        respond(false, { error: error instanceof Error ? error.message : String(error) });
      }
    });

    api.registerGatewayMethod("discord-voice.status", async ({ respond }) => {
      try {
        const vm = ensureVoiceManager();
        const sessions = vm.getAllSessions().map((s) => ({
          guildId: s.guildId,
          channelId: s.channelId,
          speaking: s.speaking,
          usersListening: s.userAudioStates.size,
        }));
        respond(true, { sessions });
      } catch (error) {
        respond(false, { error: error instanceof Error ? error.message : String(error) });
      }
    });

    // Register agent tool
    api.registerTool({
      name: "discord_voice",
      label: "Discord Voice",
      description: "Control Discord voice channel - join, leave, speak, or get status",
      parameters: VoiceToolSchema,
      async execute(_toolCallId, params) {
        const json = (payload: unknown) => ({
          content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
          details: payload,
        });

        try {
          const p = params as { action: string; channelId?: string; guildId?: string; text?: string };
          const vm = ensureVoiceManager();
          const client = getDiscordClient();

          switch (p.action) {
            case "join": {
              if (!p.channelId) throw new Error("channelId required");
              if (!client) throw new Error("Discord client not available");
              
              const channel = await client.channels.fetch(p.channelId);
              if (!channel || !("guild" in channel) || !channel.isVoiceBased()) {
                throw new Error("Invalid voice channel");
              }
              
              const session = await vm.join(channel as VoiceBasedChannel);
              return json({ joined: true, guildId: session.guildId, channelId: session.channelId });
            }

            case "leave": {
              let guildId = p.guildId;
              if (!guildId) {
                const sessions = vm.getAllSessions();
                if (sessions.length === 0) {
                  return json({ left: false, reason: "Not in any voice channel" });
                }
                guildId = sessions[0].guildId;
              }
              const left = await vm.leave(guildId);
              return json({ left, guildId });
            }

            case "speak": {
              if (!p.text) throw new Error("text required");
              let guildId = p.guildId;
              if (!guildId) {
                const sessions = vm.getAllSessions();
                if (sessions.length === 0) {
                  throw new Error("Not in any voice channel");
                }
                guildId = sessions[0].guildId;
              }
              await vm.speak(guildId, p.text);
              return json({ spoken: true });
            }

            case "status": {
              const sessions = vm.getAllSessions().map((s) => ({
                guildId: s.guildId,
                channelId: s.channelId,
                speaking: s.speaking,
                usersListening: s.userAudioStates.size,
              }));
              return json({ sessions });
            }

            default:
              throw new Error(`Unknown action: ${p.action}`);
          }
        } catch (error) {
          return json({ error: error instanceof Error ? error.message : String(error) });
        }
      },
    });

    // Register CLI commands
    api.registerCli(
      ({ program }) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const prog = program as any;

        const voiceCmd = prog.command("voice").description("Discord voice channel commands");

        voiceCmd
          .command("join")
          .description("Join a Discord voice channel")
          .argument("<channelId>", "Voice channel ID")
          .action(async (channelId: string) => {
            const client = getDiscordClient();
            if (!client) {
              console.error("Discord client not available");
              return;
            }

            try {
              const channel = await client.channels.fetch(channelId);
              if (!channel || !("guild" in channel) || !channel.isVoiceBased()) {
                console.error("Invalid voice channel");
                return;
              }

              const vm = ensureVoiceManager();
              const session = await vm.join(channel as VoiceBasedChannel);
              console.log(`Joined voice channel in guild ${session.guildId}`);
            } catch (error) {
              console.error(`Failed to join: ${error instanceof Error ? error.message : String(error)}`);
            }
          });

        voiceCmd
          .command("leave")
          .description("Leave the current voice channel")
          .option("-g, --guild <guildId>", "Guild ID")
          .action(async (opts: { guild?: string }) => {
            const vm = ensureVoiceManager();
            const guildId = opts.guild || vm.getAllSessions()[0]?.guildId;
            
            if (!guildId) {
              console.log("Not in any voice channel");
              return;
            }

            const left = await vm.leave(guildId);
            console.log(left ? `Left voice channel in guild ${guildId}` : "Failed to leave");
          });

        voiceCmd
          .command("status")
          .description("Show voice connection status")
          .action(() => {
            const vm = ensureVoiceManager();
            const sessions = vm.getAllSessions();

            if (sessions.length === 0) {
              console.log("Not connected to any voice channels");
              return;
            }

            for (const s of sessions) {
              console.log(`Guild: ${s.guildId}`);
              console.log(`  Channel: ${s.channelId}`);
              console.log(`  Speaking: ${s.speaking}`);
              console.log(`  Users listening: ${s.userAudioStates.size}`);
            }
          });
      },
      { commands: ["voice"] }
    );

    // Register background service
    api.registerService({
      id: "discord-voice",
      start: async () => {
        api.logger.info("[discord-voice] Service started");
      },
      stop: async () => {
        if (voiceManager) {
          await voiceManager.destroy();
          voiceManager = null;
        }
        api.logger.info("[discord-voice] Service stopped");
      },
    });
  },
};

export default discordVoicePlugin;
