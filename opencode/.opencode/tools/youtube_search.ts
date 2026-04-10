import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description:
    "Search YouTube videos by scraping YouTube search and watch pages directly. Returns concrete video URLs, titles, channels, and caption-track hints for transcript-first research.",
  args: {
    query: tool.schema.string().describe("YouTube search query"),
    limit: tool.schema.number().optional().describe("Maximum number of results to return (default: 10)"),
    attempts: tool.schema.number().optional().describe("How many internal query variants to try (default: 4)"),
    timeout: tool.schema.number().optional().describe("Request timeout in seconds (default: 20)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format (default: md)"),
    user_agent: tool.schema.string().optional().describe("Custom user agent for YouTube requests"),
  },
  async execute(args, context) {
    const script = `${context.worktree}/opencode/.opencode/tools/youtube_search.py`
    const cmdArgs = ["--query", args.query]

    if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
    if (args.attempts !== undefined) cmdArgs.push("--attempts", String(args.attempts))
    if (args.timeout !== undefined) cmdArgs.push("--timeout", String(args.timeout))
    if (args.format) cmdArgs.push("--format", args.format)
    if (args.user_agent) cmdArgs.push("--user-agent", args.user_agent)

    try {
      return await $`python3 ${script} ${cmdArgs}`.text()
    } catch (e) {
      return `Error running YouTube search tool: ${e.message}`
    }
  },
})
