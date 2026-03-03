#!/usr/bin/env python3
"""
Publish normalized UI payload to the web API bulk endpoint.
Usage: python3 publish_to_api.py --url https://app.example.com/api/resources/bulk --token SECRET
"""
import argparse
import json
import time
import requests


def post_with_retries(url, data, headers, retries=5, backoff=1.0):
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=30)
            if resp.status_code in (200, 201):
                return resp
            else:
                print(f"Attempt {attempt}: status {resp.status_code} - {resp.text}")
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
        time.sleep(backoff * (2 ** (attempt - 1)))
    raise RuntimeError("All attempts failed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='Bulk API URL')
    parser.add_argument('--token', required=False, help='API token for X-Api-Token header')
    parser.add_argument('--file', default='Scripts/ui_payload.json', help='Path to ui_payload.json')
    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as f:
        payload = json.load(f)

    headers = {'Content-Type': 'application/json'}
    if args.token:
        headers['X-Api-Token'] = args.token

    resp = post_with_retries(args.url, payload, headers)
    print('Success:', resp.status_code, resp.text)


if __name__ == '__main__':
    main()
