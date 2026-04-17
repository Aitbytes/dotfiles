import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

const STRUCTURED_ERROR_RE = /^[A-Z_]+: .+ \(provider=.+, stage=.+\)$/s

export default tool({
  description:
    "Search the FDA 510(k) medical device clearance database via the openFDA API. Returns device names, applicants, decision dates, product codes, and regulatory details. No API key required for basic use. Optionally set OPENFDA_API_KEY env var for higher rate limits.",
  args: {
    query: tool.schema
      .string()
      .optional()
      .describe("Free-text search across all 510(k) fields (e.g. 'laryngectomy', 'voice prosthesis')"),
    k_number: tool.schema
      .string()
      .optional()
      .describe("Specific 510(k) number to look up (e.g. 'K201234')"),
    applicant: tool.schema.string().optional().describe("Filter by applicant/company name"),
    device_name: tool.schema.string().optional().describe("Filter by device name"),
    decision: tool.schema
      .string()
      .optional()
      .describe("Filter by decision code: SESE (Substantially Equivalent), NSUB (Not Substantially Equivalent), etc."),
    date_from: tool.schema.string().optional().describe("Decision date from, format YYYYMMDD"),
    date_to: tool.schema.string().optional().describe("Decision date to, format YYYYMMDD"),
    limit: tool.schema.number().optional().describe("Max results to return (default: 10, max: 100)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format: md or json (default: md)"),
    output: tool.schema.string().optional().describe("Output file path (default: stdout)"),
  },
  async execute(args, context) {
    const script = `${import.meta.dir}/fda_510k.py`

    const cmdArgs: string[] = []

    if (args.query) cmdArgs.push("--query", args.query)
    if (args.k_number) cmdArgs.push("--k-number", args.k_number)
    if (args.applicant) cmdArgs.push("--applicant", args.applicant)
    if (args.device_name) cmdArgs.push("--device-name", args.device_name)
    if (args.decision) cmdArgs.push("--decision", args.decision)
    if (args.date_from) cmdArgs.push("--date-from", args.date_from)
    if (args.date_to) cmdArgs.push("--date-to", args.date_to)
    if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
    if (args.format) cmdArgs.push("--format", args.format)
    if (args.output) cmdArgs.push("--output", args.output)

    try {
      return await $`uv run --with requests python3 ${script} ${cmdArgs}`.text()
    } catch (e: any) {
      if (STRUCTURED_ERROR_RE.test(e.message)) throw new Error(e.message)
      throw new Error(`Error running fda_510k: ${e.message}`)
    }
  },
})
