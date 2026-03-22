import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description:
    "Search EUDAMED, the European Database on Medical Devices (EU MDR/IVDR registry). Look up CE-marked devices, manufacturers, UDI codes, risk classifications, and regulatory status. No API key required — uses the public EUDAMED REST API.",
  args: {
    query: tool.schema
      .string()
      .optional()
      .describe("Keyword search for devices (e.g. 'voice prosthesis', 'laryngectomy', 'tracheoesophageal')"),
    manufacturer: tool.schema
      .string()
      .optional()
      .describe("Filter by manufacturer or actor name (e.g. 'Atos Medical', 'Provox')"),
    udi: tool.schema
      .string()
      .optional()
      .describe("Look up a specific UDI-DI (Unique Device Identifier)"),
    limit: tool.schema.number().optional().describe("Max results to return (default: 20)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format: md or json (default: md)"),
    output: tool.schema.string().optional().describe("Output file path (default: stdout)"),
  },
  async execute(args, context) {
    const script = `${context.worktree}/opencode/.opencode/tools/eudamed_lookup.py`

    const cmdArgs: string[] = []

    if (args.query) cmdArgs.push("--query", args.query)
    if (args.manufacturer) cmdArgs.push("--manufacturer", args.manufacturer)
    if (args.udi) cmdArgs.push("--udi", args.udi)
    if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
    if (args.format) cmdArgs.push("--format", args.format)
    if (args.output) cmdArgs.push("--output", args.output)

    try {
      const result = await $`uv run --with requests python3 ${script} ${cmdArgs}`.text()
      return result
    } catch (e) {
      return `Error running EUDAMED lookup: ${e.message}`
    }
  },
})
