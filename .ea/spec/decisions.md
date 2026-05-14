# Architecture Decisions

Chronological log of key decisions for this project.

---

## ADR-001: Migrate DNS from self-hosted server to GitHub Pages

**Date:** 2026-05-13  
**Status:** Accepted

**Context:**  
Blog and wiki were previously served through a self-hosted server (`106.54.23.131`) with Nginx reverse proxy. The server lease expired, requiring a new hosting decision.

**Options considered:**
1. Point DNS directly to GitHub Pages (CNAME → `lightblues.github.io`)
2. Redeploy Nginx on new server (`tx04`)

**Decision:** Option 1 — GitHub Pages with CNAME records.

**Rationale:**
- Both sites are pure static (Hexo blog, MkDocs wiki) — no server-side logic needed
- CI/CD already pushes to gh-pages branch via `peaceiris/actions-gh-pages`
- Zero maintenance: no Nginx, no cert renewal, no server management
- Higher availability than single VPS
- GitHub auto-provisions Let's Encrypt certificates
- Only takes minutes to configure vs. hours for server setup

**Consequences:**
- `lightblues.github.io/blog/` now 301 redirects to `blog.easonsi.site/`
- Had to change Hexo `root: /blog/` → `root: /` and `url` accordingly
- Had to change MkDocs `site_url` similarly
- `cname` param added to deploy workflows to prevent custom domain reset on each deploy

---

## ADR-002: Migrate images from COS to GitHub + jsdelivr CDN

**Date:** 2026-05-14  
**Status:** Accepted

**Context:**  
Blog images were hosted on Tencent COS behind `cloud.easonsi.site/img/` (served via the now-expired server). 113 images, ~110MB total. Needed a new hosting solution.

**Options considered:**
1. GitHub repo (`Lightblues/assets`) + jsdelivr CDN
2. Continue with COS + new custom domain pointing to COS
3. Use relative paths within the blog repo itself

**Decision:** Option 1 — GitHub assets repo + jsdelivr.

**Rationale:**
- Wiki already uses this exact pattern (`cdn.jsdelivr.net/gh/lightblues/assets@main/wiki/...`)
- Centralizes all static assets in one repo for both blog and wiki
- Free, no billing surprises
- If jsdelivr becomes unreliable, only need to change URL prefix (images stay in GitHub permanently)
- Relative paths not viable: Butterfly theme requires absolute URLs in config (`_config.butterfly.yml` covers, favicon, etc.)
- Total size (~230MB with existing wiki assets) well within GitHub limits

**Consequences:**
- 225 URL references updated across 15 files
- `movies/movies-00001.png` was already missing from COS — accepted as lost
- jsdelivr has propagation delay for new files; `purge_jsdelivr.py` script created for warm-up
- Future image workflow: add to `assets/blog/`, push, optionally run purge script

---

## ADR-003: Use Tencent Cloud DNSPod API for DNS management

**Date:** 2026-05-13  
**Status:** Accepted

**Context:**  
Needed to manage DNS records programmatically rather than through web console.

**Decision:** Python scripts using `tencentcloud-sdk-python-dnspod` package.

**Rationale:**
- Reproducible and version-controlled DNS configuration
- Supports dry-run mode for safe previewing
- Env vars (`TENCENTCLOUD_SECRET_ID_MAIN` / `TENCENTCLOUD_SECRET_KEY_MAIN`) for multi-account support
- Scripts placed in `scripts/dns/` within blog repo for co-location

**Consequences:**
- Requires `tencentcloud-sdk-python-dnspod` installed (global base venv at `~/.venvs/base`)
- Must set env vars before running scripts
