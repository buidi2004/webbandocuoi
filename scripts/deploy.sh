#!/bin/bash

# ============================================
# IVIE Wedding Studio - Deploy Script
# ============================================
# Quick script to commit and push changes to GitHub
# Render will automatically deploy when changes are pushed

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   IVIE Wedding Studio - Deploy Script${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git not initialized. Initializing...${NC}"
    git init
    echo -e "${GREEN}✅ Git initialized${NC}"
fi

# Check for uncommitted changes
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
    exit 0
fi

# Show status
echo -e "${BLUE}📋 Current changes:${NC}"
git status --short
echo ""

# Get commit message
if [ -z "$1" ]; then
    echo -e "${YELLOW}Enter commit message (or press Enter for default):${NC}"
    read -r COMMIT_MSG
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="Update: $(date '+%Y-%m-%d %H:%M:%S')"
    fi
else
    COMMIT_MSG="$1"
fi

echo ""
echo -e "${BLUE}📝 Commit message: ${NC}${COMMIT_MSG}"
echo ""

# Add all changes
echo -e "${BLUE}📦 Adding all changes...${NC}"
git add .

# Commit
echo -e "${BLUE}💾 Committing...${NC}"
git commit -m "$COMMIT_MSG"

# Push to origin
echo -e "${BLUE}🚀 Pushing to GitHub...${NC}"

# Check if remote exists
if git remote | grep -q "origin"; then
    git push origin main 2>/dev/null || git push origin master 2>/dev/null || {
        echo -e "${YELLOW}⚠️  Push failed. Trying to set upstream...${NC}"
        git push -u origin main 2>/dev/null || git push -u origin master
    }
else
    echo -e "${RED}❌ No remote 'origin' configured.${NC}"
    echo -e "${YELLOW}Please run:${NC}"
    echo -e "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    exit 1
fi

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${BLUE}📡 Render will automatically deploy in 2-5 minutes.${NC}"
echo ""
echo -e "Check deployment status at:"
echo -e "  ${YELLOW}https://dashboard.render.com${NC}"
echo ""
