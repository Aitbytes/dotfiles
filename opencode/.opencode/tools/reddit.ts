import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description: "Scrape Reddit posts and comments for a given topic. Returns collected posts in markdown or JSON format. Requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables.",
  args: {
    niche: tool.schema.string().describe("Primary topic/keyword to search for"),
    subreddits: tool.schema.string().optional().describe("Plus-separated list of subreddits (e.g., 'programming+technology'). Defaults to niche-derived subreddits."),
    terms: tool.schema.string().optional().describe("Comma-separated additional search terms to broaden results"),
    limit: tool.schema.number().optional().describe("Max posts per search term (default: 20)"),
    max_posts: tool.schema.number().optional().describe("Hard cap on total unique posts collected (default: 50)"),
    min_score: tool.schema.number().optional().describe("Minimum post score to include (default: 10)"),
    comments: tool.schema.number().optional().describe("Number of top comments per post (default: 10)"),
    min_comment_score: tool.schema.number().optional().describe("Minimum comment score (default: 1)"),
    output: tool.schema.string().optional().describe("Output file path (default: <niche>_reddit_data.md)"),
    format: tool.schema.enum(["md", "json"]).optional().describe("Output format: md or json (default: md)"),
    sort: tool.schema.enum(["relevance", "new", "top", "comments"]).optional().describe("Reddit sort order (default: top)"),
  },
  async execute(args, context) {
    const script = `${context.worktree}/opencode/.opencode/tools/reddit_scraper.py`
    
    const cmdArgs = [`--niche`, args.niche]
    
    if (args.subreddits) cmdArgs.push(`--subreddits`, args.subreddits)
    if (args.terms) cmdArgs.push(`--terms`, args.terms)
    if (args.limit !== undefined) cmdArgs.push(`--limit`, String(args.limit))
    if (args.max_posts !== undefined) cmdArgs.push(`--max-posts`, String(args.max_posts))
    if (args.min_score !== undefined) cmdArgs.push(`--min-score`, String(args.min_score))
    if (args.comments !== undefined) cmdArgs.push(`--comments`, String(args.comments))
    if (args.min_comment_score !== undefined) cmdArgs.push(`--min-comment-score`, String(args.min_comment_score))
    if (args.output) cmdArgs.push(`--output`, args.output)
    if (args.format) cmdArgs.push(`--format`, args.format)
    if (args.sort) cmdArgs.push(`--sort`, args.sort)

    try {
      const result = await $`uv run --with praw python3 ${script} ${cmdArgs}`.text()
      return result
    } catch (e) {
      return `Error running reddit scraper: ${e.message}`
    }
  },
})
