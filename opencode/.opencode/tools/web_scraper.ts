import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description:
    "Fetch and extract content from any public URL. Supports plain text extraction, markdown conversion, link listing, and table extraction. Uses requests + BeautifulSoup under the hood. No API key required.",
  args: {
    url: tool.schema.string().describe("URL to fetch"),
    selector: tool.schema
      .string()
      .optional()
      .describe("CSS selector(s) to extract, comma-separated (e.g. 'h1,p,table'). Defaults to full body text."),
    mode: tool.schema
      .enum(["text", "html", "markdown", "links", "tables"])
      .optional()
      .describe("Output mode: text (default), html, markdown, links, or tables"),
    output: tool.schema.string().optional().describe("Output file path. If omitted, returns content directly."),
    timeout: tool.schema.number().optional().describe("Request timeout in seconds (default: 30)"),
    user_agent: tool.schema.string().optional().describe("Custom User-Agent string"),
    headers: tool.schema
      .string()
      .optional()
      .describe('Extra HTTP headers as a JSON string (e.g. \'{"Accept-Language": "en"}\')'),
    max_chars: tool.schema
      .number()
      .optional()
      .describe("Maximum characters to return (default: 50000)"),
  },
  async execute(args, context) {
    const script = `${context.worktree}/opencode/.opencode/tools/web_scraper.py`

    const cmdArgs = ["--url", args.url]

    if (args.selector) cmdArgs.push("--selector", args.selector)
    if (args.mode) cmdArgs.push("--mode", args.mode)
    if (args.output) cmdArgs.push("--output", args.output)
    if (args.timeout !== undefined) cmdArgs.push("--timeout", String(args.timeout))
    if (args.user_agent) cmdArgs.push("--user-agent", args.user_agent)
    if (args.headers) cmdArgs.push("--headers", args.headers)
    if (args.max_chars !== undefined) cmdArgs.push("--max-chars", String(args.max_chars))

    try {
      const result =
        await $`uv run --with requests --with beautifulsoup4 --with lxml python3 ${script} ${cmdArgs}`.text()
      return result
    } catch (e) {
      return `Error running web scraper: ${e.message}`
    }
  },
})
