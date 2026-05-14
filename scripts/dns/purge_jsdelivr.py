#!/usr/bin/env python3
"""
Purge jsdelivr CDN cache for all blog images in assets repo.

This is useful after pushing new images — jsdelivr may return 404/403
for newly added files until they're accessed or purged.

Usage:
    python purge_jsdelivr.py          # purge all blog images
    python purge_jsdelivr.py --dry-run # show URLs without purging
"""

import os
import sys
import time
import urllib.request
import json

ASSETS_BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "blog")
JSDELIVR_PURGE_URL = "https://purge.jsdelivr.net/gh/lightblues/assets@main/blog/{}"


def get_all_image_paths():
    """Get all image file paths relative to assets/blog/."""
    paths = []
    blog_dir = os.path.abspath(ASSETS_BLOG_DIR)
    for root, dirs, files in os.walk(blog_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".ico", ".webp")):
                rel_path = os.path.relpath(os.path.join(root, f), blog_dir)
                paths.append(rel_path)
    return sorted(paths)


def purge_url(path: str) -> dict:
    """Purge a single file from jsdelivr CDN."""
    url = JSDELIVR_PURGE_URL.format(path)
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    dry_run = "--dry-run" in sys.argv
    paths = get_all_image_paths()

    if not paths:
        print(f"No images found in {os.path.abspath(ASSETS_BLOG_DIR)}")
        sys.exit(1)

    print(f"Found {len(paths)} images to purge")
    if dry_run:
        print("=== DRY RUN ===")
        for p in paths:
            print(f"  {JSDELIVR_PURGE_URL.format(p)}")
        return

    success = 0
    failed = 0
    for i, p in enumerate(paths, 1):
        result = purge_url(p)
        status = result.get("status", "unknown")
        if status == "finished":
            success += 1
            print(f"  [{i}/{len(paths)}] ✓ {p}")
        else:
            failed += 1
            print(f"  [{i}/{len(paths)}] ✗ {p} ({status})")
        # Rate limiting: jsdelivr allows ~100 purge/min
        if i % 10 == 0:
            time.sleep(1)

    print(f"\nDone: {success} succeeded, {failed} failed")


if __name__ == "__main__":
    main()
