#!/bin/bash

# push-all.sh - Push to multiple git remotes
# This script pushes the current branch (or specified branch) to both origin and local remotes

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not a git repository!"
    exit 1
fi

# Get the current branch if no arguments provided
if [ $# -eq 0 ]; then
    BRANCH=$(git branch --show-current)
    if [ -z "$BRANCH" ]; then
        print_error "Could not determine current branch"
        exit 1
    fi
    print_status "No branch specified, using current branch: $BRANCH"
else
    BRANCH="$1"
    shift
fi

# Additional arguments to pass to git push
EXTRA_ARGS="$@"

# Function to push to a remote
push_to_remote() {
    local remote=$1
    local branch=$2
    
    print_status "Pushing to $remote..."
    
    if git remote get-url "$remote" > /dev/null 2>&1; then
        if git push "$remote" "$branch" $EXTRA_ARGS; then
            print_success "Successfully pushed to $remote"
            return 0
        else
            print_error "Failed to push to $remote"
            return 1
        fi
    else
        print_error "Remote '$remote' not configured"
        return 1
    fi
}

# Main execution
print_status "Starting push to all remotes for branch: $BRANCH"
echo ""

# Track overall success
OVERALL_SUCCESS=0

# Push to origin (GitHub)
if push_to_remote "origin" "$BRANCH"; then
    echo ""
else
    OVERALL_SUCCESS=1
    echo ""
fi

# Push to local (if configured)
if push_to_remote "local" "$BRANCH"; then
    echo ""
else
    # Don't fail if local remote isn't configured
    print_status "Local remote not configured (this is optional)"
    print_status "See PUSH_TO_LOCAL.md for setup instructions"
    echo ""
fi

# Summary
if [ $OVERALL_SUCCESS -eq 0 ]; then
    print_success "All configured remotes updated successfully!"
    exit 0
else
    print_error "Some remotes failed to update"
    exit 1
fi
