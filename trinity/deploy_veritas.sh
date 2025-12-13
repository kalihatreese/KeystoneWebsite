#!/data/data/com.termux/files/usr/bin/bash
# Deploy Keystone Veritas site to Vercel with force-clear cache

echo "🔄 Pushing changes to GitHub..."
git add .
git commit -m "Auto-deploy update" 2>/dev/null
git push origin main

echo "🚀 Deploying to Vercel with cache cleared..."
vercel --prod --force

echo "✅ Deployment complete!"
