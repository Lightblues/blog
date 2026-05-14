# Blog

Hexo-based personal tech blog. Deployed to GitHub Pages via `blog.easonsi.site`.

## Quick Reference

- Theme: Butterfly
- Node: 22+
- Deploy target: `Lightblues/blog` repo → gh-pages branch → GitHub Pages
- Custom domain: `blog.easonsi.site` (CNAME → `lightblues.github.io`)
- Images: `cdn.jsdelivr.net/gh/lightblues/assets@main/blog/...`

## Common Commands

```bash
npm install          # install deps
npx hexo generate   # build
npx hexo server     # local preview (localhost:4000)
npx hexo new "title" # new post
npx hexo clean      # clear cache
```

## DNS Management

```bash
cd scripts/dns

# Requires env vars:
#   TENCENTCLOUD_SECRET_ID_MAIN
#   TENCENTCLOUD_SECRET_KEY_MAIN
# Python: ~/.venvs/base/bin/python (has tencentcloud-sdk-python-dnspod)

python list_records.py              # list all DNS records
python setup_github_pages.py --dry-run  # preview CNAME setup
python setup_github_pages.py        # apply CNAME records
python purge_jsdelivr.py            # warm jsdelivr CDN cache after pushing new images
```

## Image Workflow

Images live in `Lightblues/assets` repo under `blog/` directory.

```bash
# Add new images
cp new-image.jpg ~/Projects/output/assets/blog/{category}/
cd ~/Projects/output/assets && git add blog/ && git commit && git push

# Warm CDN cache (optional, speeds up first access)
cd ~/Projects/output/blog/scripts/dns && python purge_jsdelivr.py
```

URL pattern: `https://cdn.jsdelivr.net/gh/lightblues/assets@main/blog/{category}/{file}`

## Coding Style

- Blog posts in `source/_posts/` as Markdown
- Images referenced via jsdelivr CDN (assets repo)
- Config files: `_config.yml` (Hexo), `_config.butterfly.yml` (theme)

## Related Projects

- Wiki/Notes: `~/Projects/output/wiki` → `notes.easonsi.site`
- Assets: `~/Projects/output/assets` → jsdelivr CDN
- DNS scripts: `scripts/dns/`

## Specs & Decisions

- Architecture spec: `.ea/spec/spec.md`
- Decision log: `.ea/spec/decisions.md`
