import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

const STRUCTURED_ERROR_RE = /^[A-Z_]+: .+ \(provider=.+, stage=.+\)$/s

export default tool({
  description:
    "Search patents by keyword, assignee, inventor, or patent number via Google Patents (no API key required). Returns patent numbers, titles, assignees, inventors, priority/filing/grant dates, and direct URLs. Covers US, EP, WO, and 100+ patent offices worldwide.",
  args: {
    query: tool.schema
      .string()
      .optional()
      .describe("Keyword search query (e.g. 'voice prosthesis laryngectomy', 'electrolarynx')"),
    patent_number: tool.schema
      .string()
      .optional()
      .describe("Specific patent number to look up (e.g. 'US10123456B2', 'EP1234567A1')"),
    assignee: tool.schema.string().optional().describe("Filter by assignee/company name (e.g. 'Atos Medical')"),
    inventor: tool.schema.string().optional().describe("Inventor name"),
    country: tool.schema
      .string()
      .optional()
      .describe("Country code filter: US, EP, WO, DE, etc. (default: all countries)"),
    date_from: tool.schema.string().optional().describe("Filter by priority year from (e.g. '2015')"),
    date_to: tool.schema.string().optional().describe("Filter by priority year to (e.g. '2024')"),
    limit: tool.schema.number().optional().describe("Max results to return (default: 10)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format: md or json (default: md)"),
    output: tool.schema.string().optional().describe("Output file path (default: stdout)"),
  },
  async execute(args, context) {
    const script = `${import.meta.dir}/patent_search.py`

    const cmdArgs: string[] = []

    if (args.query) cmdArgs.push("--query", args.query)
    if (args.patent_number) cmdArgs.push("--patent-number", args.patent_number)
    if (args.assignee) cmdArgs.push("--assignee", args.assignee)
    if (args.inventor) cmdArgs.push("--inventor", args.inventor)
    if (args.country) cmdArgs.push("--country", args.country)
    if (args.date_from) cmdArgs.push("--date-from", args.date_from)
    if (args.date_to) cmdArgs.push("--date-to", args.date_to)
    if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
    if (args.format) cmdArgs.push("--format", args.format)
    if (args.output) cmdArgs.push("--output", args.output)

    try {
      return await $`uv run --with requests --with beautifulsoup4 --with lxml python3 ${script} ${cmdArgs}`.text()
    } catch (e: any) {
      if (STRUCTURED_ERROR_RE.test(e.message)) throw new Error(e.message)
      throw new Error(`Error running patent_search: ${e.message}`)
    }
  },
})
