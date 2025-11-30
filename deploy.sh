#!/bin/bash
# Harbor Agent Deployment Workflow
# This script builds, deploys to Cloudflare Pages, and optionally commits/pushes to GitHub

set -e

echo "🚀 Harbor Agent Deployment Workflow"
echo ""

# Step 1: Build
echo "📦 Step 1: Building the site..."
npm run build
echo "✅ Build complete"
echo ""

# Step 2: Deploy to Cloudflare Pages
echo "☁️  Step 2: Deploying to Cloudflare Pages..."
wrangler pages deploy dist --project-name=harbor-agent
echo "✅ Deployment complete"
echo ""

# Step 3: Git operations (if there are changes)
if [ -n "$(git status --porcelain)" ]; then
  echo "📝 Step 3: Git operations..."
  echo "   Current changes:"
  git status --short
  echo ""
  
  if [ "$1" == "--commit" ] || [ "$1" == "-c" ]; then
    COMMIT_MSG="${2:-Update site deployment}"
    echo "   Committing changes: $COMMIT_MSG"
    git add .
    git commit -m "$COMMIT_MSG"
    echo "✅ Changes committed"
    echo ""
    
    if [ "$3" == "--push" ] || [ "$3" == "-p" ]; then
      echo "   Pushing to GitHub..."
      git push origin main
      echo "✅ Changes pushed to GitHub"
    else
      echo "   💡 To push to GitHub, run: git push origin main"
    fi
  else
    echo "   💡 To commit changes, run: ./deploy.sh --commit 'Your message' --push"
    echo "   Or manually: git add . && git commit -m 'message' && git push origin main"
  fi
else
  echo "📝 Step 3: No uncommitted changes"
fi

echo ""
echo "✨ Deployment workflow complete!"
echo "🌐 Site should be live at: https://harboragent.dev"

