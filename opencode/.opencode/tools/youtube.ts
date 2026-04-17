import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

const SCRIPT = `${import.meta.dir}/youtube.py`

function runYoutube(action: string, args: string[]): Promise<string> {
  return $`uv run --with requests --with youtube-transcript-api python3 ${SCRIPT} ${action} ${args}`.text()
}

export default tool({
  description:
    "YouTube tool with four actions: (1) 'search' — search YouTube for videos by query, returns ranked results with titles, channels, caption availability, and URLs; (2) 'resolve' — resolve a video ID or URL to full metadata; (3) 'transcript' — extract transcript from a video, automatically falling back between providers (youtube-transcript-api → yt-dlp); (4) 'channel' — list recent videos from a YouTube channel URL. Returns provenance and confidence level.",
  args: {
    action: tool.schema.enum(["search", "resolve", "transcript", "channel"]).describe("Action to perform: 'search' for video discovery, 'resolve' for video metadata, 'transcript' for transcript extraction, 'channel' for listing channel videos"),
    query: tool.schema.string().optional().describe("Search query (required for action='search')"),
    video_id_or_url: tool.schema.string().optional().describe("YouTube video ID or URL (required for action='resolve' or 'transcript')"),
    channel_url: tool.schema.string().optional().describe("YouTube channel URL (required for action='channel')"),
    limit: tool.schema.number().optional().describe("Max search results (default: 10, action='search' only)"),
    attempts: tool.schema.number().optional().describe("Query variant attempts (default: 4, action='search' only)"),
    languages: tool.schema.array(tool.schema.string()).optional().describe("Preferred languages in priority order (default: ['en'], action='transcript' only)"),
    no_fallback: tool.schema.boolean().optional().describe("Skip yt-dlp fallback if primary transcript source fails (default: false, action='transcript' only)"),
    timeout: tool.schema.number().optional().describe("Request timeout in seconds (default: 20)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format (default: md)"),
  },
  async execute(args, context) {
    const action = args.action
    const cmdArgs: string[] = []

    if (action === "search") {
      if (!args.query) return "Error: 'query' is required for action='search'"
      cmdArgs.push("--query", args.query)
      if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
      if (args.attempts !== undefined) cmdArgs.push("--attempts", String(args.attempts))
    } else if (action === "resolve") {
      if (!args.video_id_or_url) return "Error: 'video_id_or_url' is required for action='resolve'"
      cmdArgs.push(args.video_id_or_url)
    } else if (action === "transcript") {
      if (!args.video_id_or_url) return "Error: 'video_id_or_url' is required for action='transcript'"
      cmdArgs.push(args.video_id_or_url)
      if (args.languages && args.languages.length > 0) cmdArgs.push("--languages", ...args.languages)
      if (args.no_fallback) cmdArgs.push("--no-fallback")
    } else if (action === "channel") {
      if (!args.channel_url) return "Error: 'channel_url' is required for action='channel'"
      cmdArgs.push(args.channel_url)
      if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
    }

    if (args.timeout !== undefined) cmdArgs.push("--timeout", String(args.timeout))
    if (args.format) cmdArgs.push("--format", args.format)

    try {
      return await runYoutube(action, cmdArgs)
    } catch (e: any) {
      return `Error running YouTube ${action}: ${e.message}`
    }
  },
})