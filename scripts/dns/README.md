# DNS Management Scripts

Manage `easonsi.site` DNS records via Tencent Cloud DNSPod API.

## Setup

```bash
# Required env vars (add to your shell profile)
export TENCENTCLOUD_SECRET_ID_MAIN="your-secret-id"
export TENCENTCLOUD_SECRET_KEY_MAIN="your-secret-key"

# Python dependency (already installed globally)
uv pip install tencentcloud-sdk-python-dnspod
```

## Usage

```bash
cd scripts/dns

# List all current DNS records
python list_records.py

# Preview GitHub Pages setup (dry run)
python setup_github_pages.py --dry-run

# Apply GitHub Pages CNAME records
python setup_github_pages.py
```

## What `setup_github_pages.py` does

Creates/updates CNAME records:
- `blog.easonsi.site` → `lightblues.github.io`
- `notes.easonsi.site` → `lightblues.github.io`

After running, you also need to:
1. Set custom domain in each repo's GitHub Pages settings
2. Or add a `CNAME` file to the gh-pages branch root
