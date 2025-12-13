#!/data/data/com.termux/files/usr/bin/bash
# Clear Cloudflare cache for KeystoneCreatorSuite deployment

CF_API_TOKEN="YOUR_CLOUDFLARE_API_TOKEN"
ZONE_ID="YOUR_ZONE_ID"

echo "Clearing Cloudflare cache..."
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
     -H "Authorization: Bearer $CF_API_TOKEN" \
     -H "Content-Type: application/json" \
     --data '{"purge_everything":true}'

echo "Cache purge requested. Cloudflare will clear cached content shortly."
