# Blog Project Spec

## Overview

Personal tech blog powered by Hexo + Butterfly theme, deployed via GitHub Pages with custom domain.

- **Site**: https://blog.easonsi.site/
- **Repo**: `Lightblues/blog` (GitHub)
- **Deploy**: GitHub Actions → gh-pages branch → GitHub Pages
- **Domain registrar**: Tencent Cloud (DNSPod)

## Architecture

```
Source (main branch)
  ├── source/_posts/       # Blog posts (Markdown)
  ├── source/gallery/      # Gallery pages
  ├── _config.yml          # Hexo config
  ├── _config.butterfly.yml # Theme config
  └── scripts/dns/         # DNS management scripts

Deploy pipeline:
  git push main → GitHub Actions → hexo generate → gh-pages branch → GitHub Pages CDN

Static assets:
  Lightblues/assets repo (blog/ directory) → jsdelivr CDN
```

## Domain & DNS

| Subdomain | Type | Target | Purpose |
|-----------|------|--------|---------|
| `blog.easonsi.site` | CNAME | `lightblues.github.io` | Blog |
| `notes.easonsi.site` | CNAME | `lightblues.github.io` | Wiki/Notes (MkDocs) |
| `easonsi.site` | A | (multiple GitHub IPs) | Root domain |

- DNS managed via Tencent Cloud DNSPod API
- Management scripts: `scripts/dns/`
- Env vars: `TENCENTCLOUD_SECRET_ID_MAIN`, `TENCENTCLOUD_SECRET_KEY_MAIN`

## Image Hosting

All blog images hosted in `Lightblues/assets` repo under `blog/` directory.

**URL pattern:**
```
https://cdn.jsdelivr.net/gh/lightblues/assets@main/blog/{category}/{filename}
```

**Image categories:**
- `_meta/` — favicon, avatar, about page images
- `EVA/`, `GhostBlade-WLOP/`, `cosmos/`, `CowboyBepop/`, `SamuraiChamploo/`, `Fate/`, `Ukiyo-e/` — cover/gallery images
- `2405-kubuqi/` — photo gallery
- `movies/` — post images

**CDN management:**
- After pushing new images to assets repo, run `scripts/dns/purge_jsdelivr.py` to warm CDN cache
- jsdelivr has propagation delay for new files (minutes); purge or first-access triggers caching

## Related Repos

| Repo | Purpose | URL |
|------|---------|-----|
| `Lightblues/blog` | Blog source | https://github.com/Lightblues/blog |
| `Lightblues/wiki` | Notes/Wiki (MkDocs) | https://github.com/Lightblues/wiki |
| `Lightblues/assets` | Static assets (images) | https://github.com/Lightblues/assets |

## Deploy Workflow

`deploy.yml` key config:
- Uses `peaceiris/actions-gh-pages@v4`
- `cname: blog.easonsi.site` ensures custom domain persists across deploys
- Node.js 22, `npx hexo generate`

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/dns/config.py` | DNSPod client config & shared constants |
| `scripts/dns/list_records.py` | List all DNS records for easonsi.site |
| `scripts/dns/setup_github_pages.py` | Create/update CNAME records for GitHub Pages |
| `scripts/dns/purge_jsdelivr.py` | Purge jsdelivr CDN cache for all blog images |
