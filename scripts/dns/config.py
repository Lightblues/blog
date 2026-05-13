"""
Tencent Cloud DNSPod client configuration.

Env vars required:
  TENCENTCLOUD_SECRET_ID_MAIN
  TENCENTCLOUD_SECRET_KEY_MAIN
"""

import os
import sys
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client

# Domain managed by this script
DOMAIN = "easonsi.site"

# GitHub Pages target
GITHUB_PAGES_CNAME = "lightblues.github.io"

# Subdomain → CNAME value mapping for GitHub Pages setup
GITHUB_PAGES_RECORDS = {
    "blog": GITHUB_PAGES_CNAME,
    "notes": GITHUB_PAGES_CNAME,
}


def get_client() -> dnspod_client.DnspodClient:
    """Create an authenticated DnspodClient from environment variables."""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID_MAIN")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY_MAIN")

    if not secret_id or not secret_key:
        print("Error: TENCENTCLOUD_SECRET_ID_MAIN and TENCENTCLOUD_SECRET_KEY_MAIN must be set.")
        sys.exit(1)

    cred = credential.Credential(secret_id, secret_key)

    http_profile = HttpProfile()
    http_profile.endpoint = "dnspod.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return dnspod_client.DnspodClient(cred, "", client_profile)


def print_json(obj):
    """Pretty-print a tencentcloud response object."""
    data = json.loads(obj.to_json_string())
    print(json.dumps(data, indent=2, ensure_ascii=False))
