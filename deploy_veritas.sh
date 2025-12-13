#!/data/data/com.termux/files/usr/bin/bash
cd ~/KeystoneCreatorSuite

# Commit and push
git add .
git commit -m "Deploy latest Trinity + Veritas build"
git push origin main

# Deploy to Vercel
vercel --prod --force
