#!/bin/bash

# FocusFerry Deployment# Deploy via rsync
echo "🚀 Deploying to $DEPLOY_HOST..."
rsync -avz --delete -e "ssh -i ~/.ssh/focusferry_deploy_auto -o StrictHostKeyChecking=no" ./public/ $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATHript
# Task 0.1: Hello World Deploy

set -e  # Exit on any error

echo "🚢 FocusFerry Deployment Starting..."

# Load environment variables
if [ -f .env ]; then
    set -a  # automatically export all variables
    source .env
    set +a  # stop automatically exporting
else
    echo "❌ .env file not found. Copy .env.example to .env and fill in your credentials."
    exit 1
fi

# Check required variables
if [ -z "$DEPLOY_HOST" ] || [ -z "$DEPLOY_USER" ] || [ -z "$DEPLOY_PATH" ]; then
    echo "❌ Missing required environment variables in .env file"
    echo "Required: DEPLOY_HOST, DEPLOY_USER, DEPLOY_PATH"
    exit 1
fi

# Build the Hugo site
echo "🔨 Building Hugo site..."
hugo --minify

# Check if build was successful
if [ ! -d "public" ]; then
    echo "❌ Hugo build failed - public/ directory not found"
    exit 1
fi

# Deploy via rsync
echo "🚀 Deploying to $DEPLOY_HOST..."
rsync -avz --delete -e "ssh -i ~/.ssh/focusferry_deploy_auto -o StrictHostKeyChecking=no" ./public/ $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH

echo "✅ Deployment completed!"
echo "🌐 Site should be live at: https://hgnrs.nl"
