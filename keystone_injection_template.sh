# ================================
# Keystone Suite Key Loader & Deployment Template
# ================================

# 1. Centralized Key Loader (JS)
cat << 'JS_EOF' > keyloader.js
module.exports = () => ({
    CLOUDFLARE_API_TOKEN: process.env.CLOUDFLARE_API_TOKEN,
    CLOUDFLARE_ACCOUNT_ID: process.env.CLOUDFLARE_ACCOUNT_ID,
    CLOUDFLARE_ZONE_ID: process.env.CLOUDFLARE_ZONE_ID,
    OTHER_KEY: process.env.OTHER_KEY
});
JS_EOF

# 2. Example Usage
cat << 'JS_EOF' > example_usage.js
const keys = require('./keyloader')();
console.log(keys.CLOUDFLARE_API_TOKEN);
JS_EOF

# 3. One-Liner Injection Template for any script
cat << 'BASH_EOF' > inject_template.sh
cat << 'SCRIPT_EOF' > filename.js
const keys = require('./keyloader')();
// Your full script here using keys
SCRIPT_EOF
BASH_EOF

# 4. Single Deployment Script (bash)
cat << 'DEPLOY_EOF' > deploy_all.sh
#!/bin/bash
# Install dependencies
npm install

# Build frontend
npm run build

# Create D1 database
wrangler d1 create mydb

# Apply migrations
wrangler d1 execute mydb "CREATE TABLE IF NOT EXISTS example(id INTEGER PRIMARY KEY, data TEXT);"

# Deploy site
wrangler deploy --env production
DEPLOY_EOF

echo "Keystone Suite injection template generated successfully."
