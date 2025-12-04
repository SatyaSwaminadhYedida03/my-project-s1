#!/bin/bash
# 🚀 Staging to Production Promotion Script
# Usage: ./scripts/promote_to_production.sh v2.1.0

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
STAGING_BRANCH="staging"
PRODUCTION_BRANCH="main"
REQUIRED_APPROVALS=1

echo "🚀 Smart Hiring System - Production Promotion Script"
echo "=================================================="
echo ""

# Check if version provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: Version required${NC}"
    echo "Usage: ./scripts/promote_to_production.sh v2.1.0"
    exit 1
fi

VERSION=$1

# Validate version format
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}❌ Error: Invalid version format${NC}"
    echo "Use semantic versioning: v2.1.0"
    exit 1
fi

echo -e "${GREEN}✓ Version format valid: $VERSION${NC}"
echo ""

# Step 1: Pre-flight checks
echo "📋 Step 1/8: Pre-flight Checks"
echo "--------------------------------"

# Check git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ git is not installed${NC}"
    exit 1
fi

# Check we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}❌ Not in a git repository${NC}"
    exit 1
fi

# Check for uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${RED}❌ Uncommitted changes detected${NC}"
    echo "Please commit or stash changes before promoting"
    exit 1
fi

echo -e "${GREEN}✓ Git repository clean${NC}"

# Fetch latest changes
echo "Fetching latest changes..."
git fetch origin

# Check staging branch exists
if ! git rev-parse --verify origin/$STAGING_BRANCH >/dev/null 2>&1; then
    echo -e "${RED}❌ Staging branch not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pre-flight checks passed${NC}"
echo ""

# Step 2: Checkout and update staging
echo "📥 Step 2/8: Updating Staging Branch"
echo "--------------------------------"
git checkout $STAGING_BRANCH
git pull origin $STAGING_BRANCH
echo -e "${GREEN}✓ Staging branch updated${NC}"
echo ""

# Step 3: Run tests
echo "🧪 Step 3/8: Running Test Suite"
echo "--------------------------------"

if command -v python3 &> /dev/null; then
    echo "Installing test dependencies..."
    pip install -q pytest pytest-flask 2>/dev/null || true
    
    echo "Running tests..."
    if [ -f "backend/tests/conftest.py" ]; then
        cd backend
        python3 -m pytest tests/ -q --tb=short 2>/dev/null || {
            echo -e "${YELLOW}⚠️  Some tests failed. Continue anyway? (y/n)${NC}"
            read -r response
            if [[ ! "$response" =~ ^[Yy]$ ]]; then
                echo -e "${RED}❌ Promotion cancelled${NC}"
                exit 1
            fi
        }
        cd ..
    else
        echo -e "${YELLOW}⚠️  No tests found, skipping...${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Python not found, skipping tests${NC}"
fi

echo -e "${GREEN}✓ Tests completed${NC}"
echo ""

# Step 4: Create release branch
echo "🌿 Step 4/8: Creating Release Branch"
echo "--------------------------------"
RELEASE_BRANCH="release/$VERSION"

if git rev-parse --verify $RELEASE_BRANCH >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Release branch already exists${NC}"
    git checkout $RELEASE_BRANCH
else
    git checkout -b $RELEASE_BRANCH
    echo -e "${GREEN}✓ Release branch created: $RELEASE_BRANCH${NC}"
fi
echo ""

# Step 5: Generate changelog
echo "📝 Step 5/8: Generating Changelog"
echo "--------------------------------"

CHANGELOG_FILE="RELEASE_NOTES_${VERSION}.md"

cat > $CHANGELOG_FILE << EOF
# Release Notes - ${VERSION}

**Release Date:** $(date +"%Y-%m-%d")
**Branch:** ${STAGING_BRANCH} → ${PRODUCTION_BRANCH}

## 🎯 Changes

EOF

# Get commits since last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
    echo "Initial release" >> $CHANGELOG_FILE
    git log --oneline --no-merges -10 >> $CHANGELOG_FILE
else
    git log --oneline --no-merges $LAST_TAG..HEAD >> $CHANGELOG_FILE
fi

cat >> $CHANGELOG_FILE << EOF

## ✅ QA Checklist

- [ ] All automated tests passed
- [ ] Manual smoke tests completed
- [ ] Security scan passed
- [ ] Performance benchmarks acceptable
- [ ] Database migrations tested
- [ ] Rollback plan documented

## 🚀 Deployment Plan

1. Merge release branch to main
2. Tag with version ${VERSION}
3. Render auto-deploys from main
4. Monitor for 1 hour
5. Run post-deployment smoke tests

## 🆘 Rollback Plan

If issues detected:
1. Use Render dashboard to rollback to previous deploy
2. OR revert merge commit in git
3. Restore database from backup if schema changed
4. Create hotfix branch for fixes

## 📞 Contacts

- On-Call: [Your contact]
- Tech Lead: [Contact]
- Database: [Contact]
EOF

echo -e "${GREEN}✓ Changelog generated: $CHANGELOG_FILE${NC}"
echo ""

# Step 6: Review changes
echo "🔍 Step 6/8: Review Changes"
echo "--------------------------------"
echo ""
echo "Changes to be promoted:"
echo ""
git log --oneline --graph $PRODUCTION_BRANCH..HEAD | head -20
echo ""
echo -e "${YELLOW}Review the changelog: $CHANGELOG_FILE${NC}"
echo ""
read -p "Continue with promotion? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Promotion cancelled${NC}"
    exit 1
fi
echo ""

# Step 7: Merge to production
echo "🔀 Step 7/8: Merging to Production"
echo "--------------------------------"

git checkout $PRODUCTION_BRANCH
git pull origin $PRODUCTION_BRANCH

# Merge with no fast-forward to preserve history
git merge --no-ff $RELEASE_BRANCH -m "Release ${VERSION}: Merge ${STAGING_BRANCH} to ${PRODUCTION_BRANCH}"

echo -e "${GREEN}✓ Merged to $PRODUCTION_BRANCH${NC}"
echo ""

# Step 8: Tag release
echo "🏷️  Step 8/8: Creating Git Tag"
echo "--------------------------------"

if git rev-parse $VERSION >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Tag $VERSION already exists${NC}"
else
    git tag -a $VERSION -m "Release ${VERSION}

$(cat $CHANGELOG_FILE)
"
    echo -e "${GREEN}✓ Tag created: $VERSION${NC}"
fi
echo ""

# Push to remote
echo "📤 Pushing to Remote"
echo "--------------------------------"
echo "This will trigger production deployment on Render..."
echo ""
read -p "Push to remote and deploy? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⚠️  Changes committed locally but not pushed${NC}"
    echo "To push manually:"
    echo "  git push origin $PRODUCTION_BRANCH"
    echo "  git push origin $VERSION"
    exit 0
fi

git push origin $PRODUCTION_BRANCH
git push origin $VERSION

echo -e "${GREEN}✓ Pushed to remote${NC}"
echo ""

# Cleanup
echo "🧹 Cleanup"
echo "--------------------------------"
read -p "Delete release branch ${RELEASE_BRANCH}? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git branch -d $RELEASE_BRANCH
    git push origin --delete $RELEASE_BRANCH 2>/dev/null || true
    echo -e "${GREEN}✓ Release branch deleted${NC}"
fi
echo ""

# Success message
echo "=================================================="
echo -e "${GREEN}🎉 SUCCESS! Production promotion complete${NC}"
echo "=================================================="
echo ""
echo "📋 Summary:"
echo "  Version: $VERSION"
echo "  Branch: $PRODUCTION_BRANCH"
echo "  Tag: $VERSION"
echo ""
echo "📊 Next Steps:"
echo "  1. Monitor Render deployment: https://dashboard.render.com"
echo "  2. Check application logs for errors"
echo "  3. Run smoke tests from QA_CHECKLIST.md"
echo "  4. Monitor error rates in Sentry"
echo "  5. Watch for 1 hour before closing incident"
echo ""
echo "🆘 If Issues Occur:"
echo "  - See ROLLBACK_GUIDE.md"
echo "  - Use: git revert HEAD"
echo "  - Or rollback in Render dashboard"
echo ""
echo "📝 Release Notes: $CHANGELOG_FILE"
echo ""
