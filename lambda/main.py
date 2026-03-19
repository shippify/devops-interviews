import json
import urllib.request
import boto3
import os

BUCKET_NAME = os.environ.get("BUCKET_NAME", "")
EXTERNAL_API_URL = os.environ.get("EXTERNAL_API_URL", "https://httpbin.org/get")


def handler(event, context):
    result = {"s3_list": None, "external_api": None, "errors": []}

    # 1. Try to list ALL S3 buckets
    try:
        print('Listing S3 buckets...')
        s3 = boto3.client("s3")
        buckets_resp = s3.list_buckets()
        result["s3_list"] = {
            "buckets": [b["Name"] for b in buckets_resp.get("Buckets", [])],
        }
        print('S3 buckets listed successfully: ', result["s3_list"])

        # Also list objects from our target bucket
        if BUCKET_NAME:
            response = s3.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=5)
            result["s3_list"]["bucket_objects"] = {
                "bucket": BUCKET_NAME,
                "key_count": response.get("KeyCount", 0),
                "keys": [obj["Key"] for obj in response.get("Contents", [])],
            }
    except Exception as e:
        result["errors"].append(f"s3: {type(e).__name__}: {str(e)}")
        print('S3 listing failed: ', result["errors"])

    # 2. Try to call external API
    try:
        req = urllib.request.Request(EXTERNAL_API_URL, method="GET")
        print('Calling external API: ', EXTERNAL_API_URL)
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode()
            result["external_api"] = {"status": resp.status, "body_preview": body[:200]}
            print('External API called successfully: ', result["external_api"])
    except Exception as e:
        result["errors"].append(f"api: {type(e).__name__}: {str(e)}")
        print('External API call failed: ', result["errors"])

    return {
        "statusCode": 200,
        "body": json.dumps(result, indent=2),
    }
