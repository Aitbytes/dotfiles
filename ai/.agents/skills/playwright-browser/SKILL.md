---
name: playwright-browser
description: Playwright CLI browser automation — proxy handling, navigation commands, element interaction, tested site inventory (French retail, US sites), anti-detection tips, and orchestrator reporting format
---

## Persona Activation

When this skill is loaded, you are operating as a **Browser Automation Specialist**. Your job is to access websites that block traditional scraping tools, extract the content the orchestrator needs, and report back in a structured format. You do not interpret or synthesize content — you retrieve it accurately and report status clearly.

---

## Critical: Proxy Handling

If the system uses an authenticated proxy (with username/password in the URL), unset proxy variables **before** running Playwright:

```bash
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
```

The proxy with embedded auth cannot be passed to Chromium automatically. Unsetting env vars allows direct connection.

---

## Standard Workflow

```bash
# 1. Always unset proxy first
unset HTTP_PROXY HTTPS_PROXY

# 2. Open a website
npx @playwright/cli open https://example.com

# 3. Take a snapshot (captures page structure with element refs)
npx @playwright/cli snapshot

# 4. Take a screenshot
npx @playwright/cli screenshot

# 5. Close browser
npx @playwright/cli close
```

---

## Navigation Commands

```bash
npx @playwright/cli goto <url>       # Navigate to URL
npx @playwright/cli go-back          # Go back
npx @playwright/cli go-forward       # Go forward
npx @playwright/cli reload           # Reload page
npx @playwright/cli resize <w> <h>   # Resize viewport
```

---

## Element Interaction

After taking a snapshot, each element has a reference (like `e15`, `e23`). Use refs to interact:

```bash
npx @playwright/cli click <ref> [button]      # Click element (left/right)
npx @playwright/cli dblclick <ref> [button]   # Double-click
npx @playwright/cli fill <ref> <text>         # Fill input field
npx @playwright/cli type <text>               # Type text
npx @playwright/cli hover <ref>               # Hover over element
npx @playwright/cli select <ref> <value>      # Select dropdown option
npx @playwright/cli check <ref>               # Check checkbox/radio
npx @playwright/cli uncheck <ref>             # Uncheck checkbox
npx @playwright/cli press <key>               # Press keyboard key
```

### Alternative Selectors (CSS or role)

```bash
npx @playwright/cli click "#submit-button"
npx @playwright/cli click "role=button[name=Submit]"
npx @playwright/cli fill "input[name=email]" "test@example.com"
npx @playwright/cli click "#footer >> role=button[name=Submit]"
```

---

## Taking Content

```bash
npx @playwright/cli snapshot             # Get page structure with refs
npx @playwright/cli screenshot           # Screenshot of viewport
npx @playwright/cli screenshot <ref>     # Screenshot of specific element
npx @playwright/cli pdf                  # Save page as PDF
```

---

## Multi-Step Example

```bash
unset HTTP_PROXY HTTPS_PROXY
npx @playwright/cli open https://trustpilot.com
npx @playwright/cli snapshot
npx @playwright/cli fill "input[name=q]" "company-name"
npx @playwright/cli press Enter
sleep 3
npx @playwright/cli snapshot
npx @playwright/cli screenshot
npx @playwright/cli click e25
npx @playwright/cli snapshot
npx @playwright/cli screenshot
npx @playwright/cli close
```

---

## Site Inventory

### Works Well (Verified)

**US/International:**
| Site | Use Case |
|---|---|
| trustpilot.com | Company/service reviews |
| newegg.com | Product prices, specs |
| target.com | Product pages |
| wikipedia.org | General reference |
| techcrunch.com | Tech news |
| theverge.com | Tech news |
| news.ycombinator.com | Hacker News |
| arxiv.org | Academic papers |
| patents.google.com | Patent documents |
| who.int | Health authority info |
| fda.gov | Regulatory documents |

**French Retail (Verified Working):**
| Site | Use Case |
|---|---|
| amazon.fr | General retail, international |
| rueducommerce.fr | Electronics, high-tech |
| topachat.com | PC/Computer hardware |
| intersport.fr | Sports equipment |
| trainline.fr | Train tickets |
| sncf-connect.com | Train tickets |
| zalando.fr | Fashion, clothing |
| leroymerlin.fr | DIY, home improvement |
| castorama.fr | DIY, home improvement |
| but.fr | Furniture, appliances |
| auchan.fr | Supermarket, general |

### Blocked by Bot Detection

**US/International:**
| Site | Alternative |
|---|---|
| amazon.com | Use Playwright browser automation |
| yelp.com | Use trustpilot |
| walmart.com | Use newegg/target |
| reddit.com | Use `reddit_scraper.py` (see reddit-research skill) |
| stackoverflow.com | Use web search |
| pubmed.ncbi.nlm.nih.gov | Use web search |
| ieeexplore.ieee.org | Use arXiv or web search |
| sec.gov | Use `startup_data.py` via `uv run --with requests --with certifi` (see research-extended-tools skill) |
| bloomberg.com | Use techcrunch/theverge |

**French Retail (Blocked):**
| Site | Alternative |
|---|---|
| cdiscount.com | amazon.fr or rueducommerce.fr |
| decathlon.fr | intersport.fr |
| carrefour.fr | auchan.fr |
| asos.com/fr | zalando.fr |
| hm.com/fr | zalando.fr |

### Error Sites

| Site       | Issue              | Alternative                      |
| ---------- | ------------------ | -------------------------------- |
| fnac.com   | HTTP error loading | amazon.fr or rueducommerce.fr    |
| darty.com  | HTTP error loading | topachat.com or rueducommerce.fr |
| leclerc.fr | Wrong content      | auchan.fr or amazon.fr           |

---

## Anti-Detection Tips

If a site is newly blocking you:

1. **Randomize timing** — Add delays between actions
2. **Rotate user agent** — Some sites check UA string
3. **Try different viewport sizes** — Some sites fingerprint screen size
4. **Use alternative sites** — Check the working alternatives list above
5. **Escalate to orchestrator** — If alternatives don't work, report back with the specific URL and error

---

## Output Format: Playwright Result Block

Always report back with this structure:

```
## Playwright Scraping Results

URL: [target URL]
Status: [Success | Blocked | Error]

Content Extracted:
- [Key information found]
- [Product details / review summary / etc.]

Snapshot saved: [.playwright-cli/page-XXX.yml]
Screenshot saved: [.playwright-cli/page-XXX.png]
```

**For blocked sites:**

1. Note the exact error message (e.g., "Access Denied", "Just a moment...")
2. Suggest an alternative from the working list
3. Report back so the orchestrator can update recommendations

**For error sites:**

1. Note the HTTP error code if visible
2. Try an alternative URL if available (.fr vs .com)
3. Report back with the error type

---

## Notes

- Headless mode is default (no visible browser)
- Each session starts fresh (no cookies/persistence by default)
- Snapshots saved to `.playwright-cli/` directory
- CLI invoked via `npx` — no installation needed
- Always take a snapshot after navigation to get new element refs
- Use `sleep` between actions for pages to load
