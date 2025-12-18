#!/bin/bash

# setup-local-remote.sh - Interactive script to set up a local git remote
# This script helps you configure a local machine as a git remote for this repository

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions for colored output
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Welcome message
print_header "Local Git Remote Setup"

echo "This script will help you set up a local machine as a git remote."
echo "You can then push your repository changes to your local machine."
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not a git repository!"
    exit 1
fi

print_success "Git repository detected"
echo ""

# Check if local remote already exists
if git remote get-url local > /dev/null 2>&1; then
    print_warning "A 'local' remote already exists:"
    git remote get-url local
    echo ""
    read -p "Do you want to reconfigure it? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove local
        print_status "Removed existing 'local' remote"
    else
        print_status "Keeping existing configuration"
        exit 0
    fi
fi

# Ask for setup type
echo "How do you want to set up your local remote?"
echo ""
echo "1) Same machine (path-based)"
echo "2) Different machine via SSH"
echo "3) Windows file path"
echo "4) Custom URL"
echo ""
read -p "Choose an option (1-4): " -n 1 -r SETUP_TYPE
echo ""
echo ""

case $SETUP_TYPE in
    1)
        print_header "Same Machine Setup"
        echo "Enter the path where you want to create the bare repository."
        echo "Example: /home/username/git-repositories/meta.git"
        echo ""
        read -p "Path: " LOCAL_PATH
        
        # Expand ~ to home directory
        LOCAL_PATH="${LOCAL_PATH/#\~/$HOME}"
        
        # Ask if we should create the bare repository
        if [ ! -d "$LOCAL_PATH" ]; then
            read -p "Directory doesn't exist. Create bare repository at this location? (Y/n): " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                mkdir -p "$(dirname "$LOCAL_PATH")"
                git init --bare "$LOCAL_PATH"
                print_success "Created bare repository at $LOCAL_PATH"
            fi
        fi
        
        REMOTE_URL="$LOCAL_PATH"
        ;;
    2)
        print_header "SSH Setup"
        echo "Enter your SSH connection details:"
        echo ""
        read -p "Username: " SSH_USER
        read -p "Host/IP: " SSH_HOST
        read -p "Repository path on remote: " SSH_PATH
        
        REMOTE_URL="ssh://${SSH_USER}@${SSH_HOST}/${SSH_PATH}"
        
        print_warning "Make sure the bare repository exists on the remote machine!"
        echo "You can create it by running on the remote machine:"
        echo "  mkdir -p \"$(dirname "$SSH_PATH")\""
        echo "  git init --bare \"$SSH_PATH\""
        ;;
    3)
        print_header "Windows Path Setup"
        echo "Enter the Windows path (e.g., C:/git-repositories/meta.git):"
        echo ""
        read -p "Path: " WIN_PATH
        
        REMOTE_URL="file:///$WIN_PATH"
        
        print_warning "Make sure the bare repository exists at this location!"
        echo "You can create it by running in Git Bash:"
        echo "  mkdir -p \"$(dirname "$WIN_PATH")\""
        echo "  git init --bare \"$WIN_PATH\""
        ;;
    4)
        print_header "Custom URL Setup"
        echo "Enter the complete git URL:"
        echo ""
        read -p "URL: " REMOTE_URL
        ;;
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

echo ""
print_status "Adding local remote with URL: $REMOTE_URL"

# Add the remote
if git remote add local "$REMOTE_URL"; then
    print_success "Successfully added 'local' remote!"
    echo ""
    
    # Verify the configuration
    print_status "Current remotes:"
    git remote -v | grep -E "(origin|local)"
    echo ""
    
    # Ask if user wants to push now
    read -p "Do you want to push the current branch to local now? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        CURRENT_BRANCH=$(git branch --show-current)
        print_status "Pushing $CURRENT_BRANCH to local..."
        
        if git push local "$CURRENT_BRANCH"; then
            print_success "Successfully pushed to local remote!"
        else
            print_error "Failed to push to local remote"
            print_warning "You may need to create the bare repository first"
        fi
    fi
    
    echo ""
    print_success "Setup complete!"
    echo ""
    echo "Next steps:"
    echo "  • Push to local: git push local <branch>"
    echo "  • Push to all remotes: ./push-all.sh <branch>"
    echo "  • Read full documentation: PUSH_TO_LOCAL.md"
    echo ""
else
    print_error "Failed to add remote"
    exit 1
fi
