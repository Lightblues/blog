#!/usr/bin/env python3
"""
Set up CNAME records pointing subdomains to GitHub Pages.

This script will:
1. List existing records for the target subdomains
2. Create or update CNAME records as needed

Target configuration:
  blog.easonsi.site  → CNAME → lightblues.github.io
  notes.easonsi.site → CNAME → lightblues.github.io
"""

import sys
from tencentcloud.dnspod.v20210323 import models
from config import DOMAIN, GITHUB_PAGES_RECORDS, get_client


def get_existing_records(client, subdomain: str) -> list:
    """Get existing records for a subdomain."""
    req = models.DescribeRecordListRequest()
    req.Domain = DOMAIN
    req.Subdomain = subdomain
    req.Limit = 100

    try:
        resp = client.DescribeRecordList(req)
        return resp.RecordList or []
    except Exception as e:
        if "EmptyList" in str(e) or "ResourceNotFound" in str(e):
            return []
        raise


def create_cname_record(client, subdomain: str, value: str):
    """Create a new CNAME record."""
    req = models.CreateRecordRequest()
    req.Domain = DOMAIN
    req.SubDomain = subdomain
    req.RecordType = "CNAME"
    req.RecordLine = "默认"
    req.Value = value
    req.TTL = 600

    resp = client.CreateRecord(req)
    print(f"  ✓ Created CNAME record: {subdomain}.{DOMAIN} → {value} (ID: {resp.RecordId})")


def modify_record(client, record_id: int, subdomain: str, value: str):
    """Modify an existing record to CNAME."""
    req = models.ModifyRecordRequest()
    req.Domain = DOMAIN
    req.RecordId = record_id
    req.SubDomain = subdomain
    req.RecordType = "CNAME"
    req.RecordLine = "默认"
    req.Value = value
    req.TTL = 600

    client.ModifyRecord(req)
    print(f"  ✓ Updated record {record_id}: {subdomain}.{DOMAIN} → {value}")


def setup_subdomain(client, subdomain: str, target: str, dry_run: bool = False):
    """Set up a single subdomain CNAME record."""
    print(f"\n[{subdomain}.{DOMAIN}] → {target}")

    existing = get_existing_records(client, subdomain)

    if not existing:
        print(f"  No existing records. Will create CNAME.")
        if not dry_run:
            create_cname_record(client, subdomain, target)
        return

    # Check if already correctly configured
    for r in existing:
        print(f"  Existing: {r.Type} → {r.Value} (ID: {r.RecordId}, Line: {r.Line})")

    # Find if there's already a matching CNAME
    cname_records = [r for r in existing if r.Type == "CNAME" and r.Value.rstrip(".") == target.rstrip(".")]
    if cname_records:
        print(f"  ✓ Already configured correctly. No changes needed.")
        return

    # If there's exactly one record, update it
    if len(existing) == 1:
        r = existing[0]
        print(f"  Will update record {r.RecordId} from {r.Type}:{r.Value} to CNAME:{target}")
        if not dry_run:
            modify_record(client, r.RecordId, subdomain, target)
        return

    # Multiple records - warn and skip
    print(f"  ⚠ Multiple existing records found. Please resolve manually:")
    for r in existing:
        print(f"    ID={r.RecordId} Type={r.Type} Value={r.Value}")
    print(f"  Skipping automatic modification.")


def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY RUN MODE (no changes will be made) ===")

    print(f"Setting up GitHub Pages DNS for {DOMAIN}")
    print(f"Target: GitHub Pages ({list(GITHUB_PAGES_RECORDS.values())[0]})")

    client = get_client()

    for subdomain, target in GITHUB_PAGES_RECORDS.items():
        setup_subdomain(client, subdomain, target, dry_run=dry_run)

    print("\n" + "=" * 60)
    print("Done!")
    if not dry_run:
        print("\nNext steps:")
        print("1. Go to each GitHub repo → Settings → Pages → Custom domain")
        print(f"   - blog repo: set custom domain to 'blog.{DOMAIN}'")
        print(f"   - wiki repo: set custom domain to 'notes.{DOMAIN}'")
        print("2. Enable 'Enforce HTTPS'")
        print("3. Wait a few minutes for DNS propagation and certificate issuance")


if __name__ == "__main__":
    main()
