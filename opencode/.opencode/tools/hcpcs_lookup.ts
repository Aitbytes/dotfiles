import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description:
    "Look up HCPCS Level II codes and Medicare Physician Fee Schedule (PFS) data. Searches CMS PFS dataset and FDA device classification. No API key required. Useful for finding reimbursement codes for medical devices, prosthetics, and procedures.",
  args: {
    code: tool.schema
      .string()
      .optional()
      .describe("Specific HCPCS or CPT code to look up (e.g. 'L8500', '31611', 'A4623')"),
    search: tool.schema
      .string()
      .optional()
      .describe("Keyword search in code descriptions (e.g. 'laryngectomy', 'voice prosthesis', 'trachea')"),
    source: tool.schema
      .enum(["cms", "fda", "both"])
      .optional()
      .describe("Data source: cms (PFS), fda (device classification), or both (default: both)"),
    limit: tool.schema.number().optional().describe("Max results to return (default: 20)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format: md or json (default: md)"),
    output: tool.schema.string().optional().describe("Output file path (default: stdout)"),
  },
  async execute(args, context) {
    const script = `${context.worktree}/opencode/.opencode/tools/hcpcs_lookup.py`

    const cmdArgs: string[] = []

    if (args.code) cmdArgs.push("--code", args.code)
    if (args.search) cmdArgs.push("--search", args.search)
    if (args.source) cmdArgs.push("--source", args.source)
    if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
    if (args.format) cmdArgs.push("--format", args.format)
    if (args.output) cmdArgs.push("--output", args.output)

    try {
      const result = await $`uv run --with requests python3 ${script} ${cmdArgs}`.text()
      return result
    } catch (e) {
      return `Error running HCPCS lookup: ${e.message}`
    }
  },
})
