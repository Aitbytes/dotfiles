import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description:
    "Search for startup and funding data. Uses SEC EDGAR (free, no key) for Form D private placement filings and company search. Optionally uses Crunchbase API (requires CRUNCHBASE_API_KEY env var) for richer funding data including rounds, investors, and valuations.",
  args: {
    company: tool.schema
      .string()
      .optional()
      .describe("Company name to look up (e.g. 'Atos Medical', 'InVivo Therapeutics')"),
    query: tool.schema
      .string()
      .optional()
      .describe("Keyword search for companies or filings (e.g. 'voice prosthesis', 'laryngectomy')"),
    source: tool.schema
      .enum(["edgar", "crunchbase", "both"])
      .optional()
      .describe(
        "Data source: edgar (free SEC filings, default), crunchbase (requires CRUNCHBASE_API_KEY), or both"
      ),
    limit: tool.schema.number().optional().describe("Max results to return (default: 10)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format: md or json (default: md)"),
    output: tool.schema.string().optional().describe("Output file path (default: stdout)"),
  },
  async execute(args, context) {
    const script = `${context.worktree}/opencode/.opencode/tools/startup_data.py`

    const cmdArgs: string[] = []

    if (args.company) cmdArgs.push("--company", args.company)
    if (args.query) cmdArgs.push("--query", args.query)
    if (args.source) cmdArgs.push("--source", args.source)
    if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
    if (args.format) cmdArgs.push("--format", args.format)
    if (args.output) cmdArgs.push("--output", args.output)

    try {
      const result = await $`uv run --with requests python3 ${script} ${cmdArgs}`.text()
      return result
    } catch (e) {
      return `Error running startup data lookup: ${e.message}`
    }
  },
})
