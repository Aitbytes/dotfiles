import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description:
    "Scrape Amazon product reviews by ASIN, URL, or search query. Extracts ratings, review text, dates, and verified purchase status. Note: Amazon actively blocks scrapers — results may be partial. For patient discussions, prefer the reddit_scrape tool instead.",
  args: {
    asin: tool.schema
      .string()
      .optional()
      .describe("Amazon product ASIN (10-character code, e.g. 'B001234567')"),
    url: tool.schema
      .string()
      .optional()
      .describe("Direct Amazon product URL (ASIN will be extracted automatically)"),
    search: tool.schema
      .string()
      .optional()
      .describe("Search Amazon for a product and scrape its reviews (e.g. 'voice prosthesis laryngectomy')"),
    pages: tool.schema
      .number()
      .optional()
      .describe("Number of review pages to scrape (default: 1, max: 5)"),
    stars: tool.schema
      .string()
      .optional()
      .describe("Filter by star rating: '1', '2', '3', '4', '5', or 'all' (default: all)"),
    sort: tool.schema
      .enum(["helpful", "recent"])
      .optional()
      .describe("Sort reviews by: helpful (default) or recent"),
    limit: tool.schema.number().optional().describe("Max reviews to return (default: 20)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format: md or json (default: md)"),
    output: tool.schema.string().optional().describe("Output file path (default: stdout)"),
  },
  async execute(args, context) {
    const script = `${context.worktree}/opencode/.opencode/tools/amazon_reviews.py`

    const cmdArgs: string[] = []

    if (args.asin) cmdArgs.push("--asin", args.asin)
    if (args.url) cmdArgs.push("--url", args.url)
    if (args.search) cmdArgs.push("--search", args.search)
    if (args.pages !== undefined) cmdArgs.push("--pages", String(args.pages))
    if (args.stars) cmdArgs.push("--stars", args.stars)
    if (args.sort) cmdArgs.push("--sort", args.sort)
    if (args.limit !== undefined) cmdArgs.push("--limit", String(args.limit))
    if (args.format) cmdArgs.push("--format", args.format)
    if (args.output) cmdArgs.push("--output", args.output)

    try {
      const result =
        await $`uv run --with requests --with beautifulsoup4 --with lxml python3 ${script} ${cmdArgs}`.text()
      return result
    } catch (e) {
      return `Error running Amazon reviews scraper: ${e.message}`
    }
  },
})
