---
name: blog-writer
description: Write, edit, and publish posts to the Hugo blog deployed on Dokploy. Use when the user asks to create a new blog post, fix a typo, update content, or publish an article to their blog at hugo-blog.aitbytes.dev.
---

# Blog Writer Skill

Write and publish content to the Hugo blog at **https://hugo-blog.aitbytes.dev**.

## Architecture overview

The blog uses a **two-repo, runtime-content** design:

```
Aitbytes/blog-engine-hugo             Aitbytes/blog-content
  (theme, layouts, Dockerfile)          (markdown posts only)
         │                                       │
         └─────────────┬─────────────────────────┘
                       ▼
            Dokploy Application
            "Hugo Blog App" (idle, redeploy on demand)
            ┌──────────────────────────────────┐
            │ entrypoint.sh on start:           │
            │  1. git clone/pull blog-content   │
            │  2. hugo --minify → static HTML   │
            │  3. nginx serves with auth_basic  │
            │     on /private/* if password set │
            └──────────────────────────────────┘
                    ▲
                    │  application.redeploy
                    │  (no Docker image rebuild!)
```

**Key insight**: Content lives in a completely separate repo. Publishing a post triggers a `redeploy` — the container restarts, pulls the latest content, rebuilds Hugo (milliseconds), and serves. **The Docker image is never rebuilt for content changes.**

## Repo structure

### Content repo (`Aitbytes/blog-content`)

```
posts/                    ← Public blog posts
  my-post.md
private/                  ← Password-protected posts (auth_basic)
  draft-notes.md
about.md                  ← About page (optional)
images/                   ← Post images (optional)
```

**Private posts** live in `private/` instead of `posts/`. They are:
- Hidden from homepage, tag pages, RSS, and sitemap (via Hugo `build.list = "never"` cascade)
- Served at `/private/<slug>/` behind Nginx `auth_basic`
- Protected by the password stored in Dokploy env var `BLOG_PRIVATE_PASSWORD`

If `BLOG_PRIVATE_PASSWORD` is unset, private posts are openly accessible — useful in dev.

### Engine repo (`Aitbytes/blog-engine-hugo`)

```
hugo.toml                 ← Site config (title, baseURL, theme, cascade for private)
themes/PaperMod/           ← Theme (git submodule)
layouts/                  ← Custom layout overrides (optional)
static/                   ← Static assets (CSS, JS, images)
Dockerfile                ← Container build
entrypoint.sh             ← Runtime: pull content → build → nginx + auth_basic
```

## How to write a public post

### 1. Clone the content repo

```bash
git clone https://github.com/Aitbytes/blog-content.git
cd blog-content
```

### 2. Create a markdown file in `posts/`

```bash
# Name convention: YYYY-MM-DD-slug.md
touch posts/2026-06-10-my-new-post.md
```

### 3. Write the post with Hugo front matter

```markdown
---
title: "Your Post Title"
date: 2026-06-10T14:30:00Z
draft: false
tags: ["tag1", "tag2"]
categories: ["category-name"]
---

## First Section

Write your content here. Standard markdown works.

### Subsection

- Bullet points
- **bold**, *italic*, `code`

![image alt](/images/photo.jpg)

> Blockquotes look great in PaperMod.

## Second Section

More content...

```

**Front matter rules:**
- `title`: Required. The post title.
- `date`: Required. ISO 8601 format with timezone (`YYYY-MM-DDTHH:MM:SSZ`).
- `draft`: Set to `true` to hide from published site. Set to `false` to publish.
- `tags`: Optional. Array of lowercase tags for categorization.
- `categories`: Optional. Array of categories (affects URL path).
- `series`: Optional. Array for post series.
- `cover`: Optional. Cover image path.

**Markdown tips:**
- Use `##` (H2) for main sections — H1 is reserved for the post title.
- Code blocks with triple backticks and language hint: ` ```python `.
- Images go in `images/` directory, referenced as `/images/photo.jpg`.
- Shortcodes: PaperMod supports `{{< figure src="..." >}}` for images.

**⚠️ Critical: date vs. build time.** Hugo skips posts with dates in the future by default. The container builds at the moment of redeploy. If your post date is later than the redeploy time, the post will be silently omitted from the output. Always set the date to a time before your planned push/redeploy. The entrypoint now passes `--buildFuture` as a safety net, but prefer to set dates in the past.

### 4. Commit and push

```bash
git add posts/2026-06-10-my-new-post.md
git commit -m "New post: Your Post Title"
git push origin main
```

### 5. Deploy

Trigger a redeploy in Dokploy. **Reference the dokploy skill** for authentication and API details. The key command:

```
POST /api/application.redeploy
Body: {"applicationId": "U4n8Ur8dyraoWX8lxhLrJ"}
```

After redeploy, the container:
1. `git pull` from `Aitbytes/blog-content`
2. `hugo --minify` rebuilds the site (~50ms)
3. Hugo builds the site (with `--buildFuture` to include posts dated today)
3. Nginx serves the updated HTML

**No Docker rebuild. No downtime (sub-second restart).**

## How to write a private post

Same flow as public, but place the file in `private/`:

```bash
touch private/2026-06-10-draft-notes.md
```

Write the post with identical front matter format. The `date`, `title`, `tags` etc. all work the same.

Private posts are **invisible on the public site** (hidden from homepage, tags, RSS, sitemap) and require the blog password at `/private/<slug>/`. The password is managed via Dokploy env var `BLOG_PRIVATE_PASSWORD`.

**Verify the private post is gated after deploy:**
```bash
# Should return 401 (no password)
curl -s -o /dev/null -w "%{http_code}\n" https://hugo-blog.aitbytes.dev/private/your-slug/

# Should return 200 (correct password)
curl -s -o /dev/null -w "%{http_code}\n" -u blog:YOUR_PASSWORD https://hugo-blog.aitbytes.dev/private/your-slug/
```

## How to edit an existing post

1. Clone or pull the content repo:
   ```bash
   cd blog-content && git pull origin main
   ```

2. Edit the `.md` file directly — fix typos, add sections, update dates.

3. Commit, push, redeploy. Same flow as creating a new post.

## How to manage the private password

**Set or change password:**
1. Update `BLOG_PRIVATE_PASSWORD` in Dokploy env vars. **Reference the dokploy skill** for the `application.saveEnvironment` endpoint.
2. Redeploy:
   ```
   POST /api/application.redeploy
   Body: {"applicationId": "U4n8Ur8dyraoWX8lxhLrJ"}
   ```
3. Verify with the curl command shown above.

**Remove private access** (make everything public): delete the `BLOG_PRIVATE_PASSWORD` env var from Dokploy and redeploy. The `/private/` section becomes openly accessible.

**How it works**: On container start, `entrypoint.sh` reads `BLOG_PRIVATE_PASSWORD`, generates an `.htpasswd` file with SHA-512 hash, and injects an `auth_basic` block into the Nginx config for the `/private` location. Hugo's `cascade.build.list = "never"` keeps private posts out of all public views.

## How to change site config

Site config changes require an **engine repo** update and a full **Docker image rebuild**:

1. Edit `hugo.toml` in `Aitbytes/blog-engine-hugo`
2. Commit and push — Dokploy's auto-deploy will trigger a build
3. This DOES rebuild the Docker image (unlike content changes)

## How to add images

1. Place images in `images/` in the content repo:
   ```bash
   mkdir -p images
   cp ~/Pictures/photo.jpg images/
   git add images/photo.jpg
   ```

2. Reference in posts with absolute paths:
   ```markdown
   ![Photo description](/images/photo.jpg)
   ```

3. Commit, push, redeploy.

## Reference: Dokploy IDs

| Resource | ID |
|---|---|
| Dokploy URL | `https://aitbytes.dev` |
| Blog project | `BxShGC_krVXqQruoKoYHG` |
| Production environment | `PVVdayq0gSG67i8dKRlQ3` |
| Hugo Blog App | `U4n8Ur8dyraoWX8lxhLrJ` (`hugo-blog-app-45lpdq`) |
| Site URL | `https://hugo-blog.aitbytes.dev` |

## Reference: GitHub repos

| Repo | URL |
|---|---|
| Engine (app code) | `https://github.com/Aitbytes/blog-engine-hugo` |
| Content (posts) | `https://github.com/Aitbytes/blog-content` |

## Reference: Hugo version & theme

| Component | Detail |
|---|---|
| Hugo version | `v0.163.0` extended (downloaded at Docker build time) |
| Theme | PaperMod (git submodule, pinned in engine repo) |
| Hugo config | `/app/hugo.toml` — valid TOML, NOT YAML syntax |
| Private posts cascade | `build.list = "never"` on `/private/**` |

## Reference: Env vars (Dokploy)

| Var | Purpose |
|---|---|
| `CONTENT_REPO` | GitHub path to content repo (`Aitbytes/blog-content`) |
| `CONTENT_REPO_TOKEN` | GitHub PAT for cloning private content repo |
| `BLOG_PRIVATE_PASSWORD` | Password for `/private/` section (unset = open) |

## Dokploy integration

For all Dokploy operations, load the **dokploy skill** first. The blog-writer skill only needs the redeploy endpoint for content changes.

**Quick redeploy (content update only):**
```bash
export VAULT_SKIP_VERIFY=true && source ~/scripts/vault-env dokploy
curl -s -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  "$DOKPLOY_URL/api/application.redeploy" \
  -d '{"applicationId": "U4n8Ur8dyraoWX8lxhLrJ"}'
```

**Check deployment status:**
```bash
curl -s -H "x-api-key: $DOKPLOY_API_KEY" \
  "$DOKPLOY_URL/api/application.one?applicationId=U4n8Ur8dyraoWX8lxhLrJ" \
  | jq '{applicationStatus, appName}'
```

**Update env vars (e.g. change private password):**
```bash
curl -s -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  "$DOKPLOY_URL/api/application.saveEnvironment" \
  -d "{\"applicationId\": \"U4n8Ur8dyraoWX8lxhLrJ\", \"env\": \"CONTENT_REPO=Aitbytes/blog-content\\nCONTENT_REPO_TOKEN=<token>\\nBLOG_PRIVATE_PASSWORD=<new-password>\"}"
```

## Troubleshooting

**Post not appearing on site:**
- Check `draft: false` in front matter
- Verify the file is in `posts/` directory (not `private/`)
- Ensure date format is valid ISO 8601 with timezone
- Push to `main` branch of `Aitbytes/blog-content`
- Did you redeploy? Content changes require a redeploy.

**Private post not password-protected:**
- Verify `BLOG_PRIVATE_PASSWORD` is set in Dokploy env vars
- Redeploy after setting the password
- Check with: `curl -I https://hugo-blog.aitbytes.dev/private/any-slug/` should return HTTP 401

**Hugo build errors on redeploy:**
- Check container logs via Dokploy API
- Common issues: invalid TOML in front matter, missing required fields
- SSH into host: `ssh adminuser@aitbytes.dev "sudo docker ps -a --filter name=hugo-blog"`

**Docker image rebuild needed?**
- Content changes (public or private): **NO** — just redeploy
- Config/theme changes (hugo.toml, layouts, etc.): **YES** — push to engine repo triggers auto-deploy
- Dockerfile or entrypoint.sh changes: **YES** — same as above
- Password changes: **NO** — env var is injected at container start, just redeploy
