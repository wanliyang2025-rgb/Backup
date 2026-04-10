#!/bin/bash
# Download file from Feishu using REST API

APP_ID="cli_a93b3aa665789cc2"
APP_SECRET="d4lvhry3RZcCtDfGekHbyeNTy00TXjv0"
FILE_TOKEN="$1"
OUTPUT_PATH="${2:-/home/leonwan/.openclaw/workspace/downloaded.xlsx}"

# Get tenant_access_token
TOKEN_RESPONSE=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}")

TENANT_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tenant_access_token', ''))")

if [ -z "$TENANT_TOKEN" ]; then
  echo "Failed to get token: $TOKEN_RESPONSE"
  exit 1
fi

echo "Got token: ${TENANT_TOKEN:0:20}..."

# Get download info
DOWNLOAD_RESPONSE=$(curl -s -X GET "https://open.feishu.cn/open-apis/drive/explorer/v2/file/download_info?file_token=$FILE_TOKEN" \
  -H "Authorization: Bearer $TENANT_TOKEN")

echo "Download response: $DOWNLOAD_RESPONSE"

DOWNLOAD_URL=$(echo "$DOWNLOAD_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('download_url', ''))")

if [ -z "$DOWNLOAD_URL" ]; then
  echo "Failed to get download URL"
  exit 1
fi

echo "Downloading from: $DOWNLOAD_URL"

# Download the file
curl -L -o "$OUTPUT_PATH" "$DOWNLOAD_URL"

echo "Downloaded to: $OUTPUT_PATH"
