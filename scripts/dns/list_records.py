#!/usr/bin/env python3
"""List all DNS records for the domain."""

from tencentcloud.dnspod.v20210323 import models
from config import DOMAIN, get_client, print_json


def main():
    client = get_client()

    req = models.DescribeRecordListRequest()
    req.Domain = DOMAIN
    req.Limit = 100

    try:
        resp = client.DescribeRecordList(req)
    except Exception as e:
        if "EmptyList" in str(e) or "ResourceNotFound" in str(e):
            print(f"No records found for {DOMAIN}")
            return
        raise

    records = resp.RecordList or []
    print(f"{'ID':<12} {'Type':<8} {'Name':<20} {'Value':<40} {'TTL':<6} {'Line'}")
    print("-" * 100)
    for r in records:
        print(f"{r.RecordId:<12} {r.Type:<8} {r.Name:<20} {r.Value:<40} {r.TTL:<6} {r.Line}")


if __name__ == "__main__":
    main()
