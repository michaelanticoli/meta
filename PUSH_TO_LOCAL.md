# Pushing Repository to Local Machine

This guide explains how to set up your local machine to receive pushes from this repository, enabling you to maintain a local copy that stays synchronized with your GitHub repository.

## Overview

By setting up a local git remote, you can:
- Push changes directly from GitHub to your local machine
- Maintain a backup of your repository locally
- Work with both GitHub and local copies simultaneously
- Sync changes between GitHub and your local machine

## Prerequisites

- Git installed on your local machine
- SSH access to your local machine (if accessing remotely)
- Basic understanding of git remotes

## Setup Instructions

### Step 1: Create a Bare Repository on Your Local Machine

A bare repository is a Git repository that doesn't have a working directory. It's ideal for receiving pushes.

```bash
# On your local machine, create a directory for your bare repository
mkdir -p ~/git-repositories
cd ~/git-repositories

# Create the bare repository
git init --bare meta.git
```

This creates a bare repository at `~/git-repositories/meta.git` on your local machine.

### Step 2: Add Local Remote to Your Working Repository

Now, add your local machine as a remote to your working repository:

#### If working on the same machine:
```bash
# In your working repository
git remote add local ~/git-repositories/meta.git
```

#### If accessing a different machine on your network:
```bash
# In your working repository
git remote add local ssh://username@local-machine-ip/home/username/git-repositories/meta.git

# For example:
# git remote add local ssh://john@192.168.1.100/home/john/git-repositories/meta.git
```

#### If using a Windows machine with Git for Windows:
```bash
# In your working repository
git remote add local file:///C:/git-repositories/meta.git
```

### Step 3: Verify the Remote Configuration

```bash
# List all remotes
git remote -v
```

You should see both `origin` (GitHub) and `local` remotes.

### Step 4: Push to Your Local Machine

```bash
# Push the current branch to local
git push local main

# Or push all branches
git push local --all

# Push all tags
git push local --tags
```

## Working with Both Remotes

### Push to Both GitHub and Local Machine

```bash
# Push to GitHub
git push origin main

# Push to local machine
git push local main

# Or push to both at once using a script (see below)
```

### Pull from GitHub and Push to Local

```bash
# Pull latest changes from GitHub
git pull origin main

# Push to local machine
git push local main
```

### Create a Convenience Script

Create a file called `push-all.sh` to push to both remotes at once:

```bash
#!/bin/bash
# push-all.sh - Push to all remotes

echo "Pushing to origin (GitHub)..."
git push origin "$@"

echo "Pushing to local..."
git push local "$@"

echo "All done!"
```

Make it executable:
```bash
chmod +x push-all.sh
```

Usage:
```bash
./push-all.sh main
```

## Setting Up a Working Copy from Bare Repository

If you want to work directly from the bare repository on your local machine:

```bash
# Clone from the bare repository
git clone ~/git-repositories/meta.git ~/projects/meta-working

# Add GitHub as remote
cd ~/projects/meta-working
git remote add github https://github.com/michaelanticoli/meta.git

# Fetch from GitHub
git fetch github

# Set up branch tracking
git branch --set-upstream-to=github/main main
```

## Automating Syncs

### Option 1: Git Hooks

Create a post-receive hook in your bare repository to automatically update a working copy:

```bash
# In ~/git-repositories/meta.git/hooks/post-receive
#!/bin/bash
WORK_TREE=/path/to/working/directory
GIT_DIR=/path/to/bare/repository

git --work-tree=$WORK_TREE --git-dir=$GIT_DIR checkout -f main
```

Make it executable:
```bash
chmod +x ~/git-repositories/meta.git/hooks/post-receive
```

### Option 2: Scheduled Sync with Cron

Create a script to periodically sync from GitHub to your local machine:

```bash
#!/bin/bash
# sync-from-github.sh

cd ~/git-repositories/meta.git
git fetch https://github.com/YOUR-USERNAME/YOUR-REPO.git main:main
```

Add to crontab to run every hour:
```bash
crontab -e
# Add: 0 * * * * /path/to/sync-from-github.sh
```

## Troubleshooting

### Permission Denied (SSH)

If you get permission denied errors when using SSH:
1. Ensure SSH keys are set up: `ssh-keygen -t ed25519`
2. Copy public key to local machine: `ssh-copy-id username@local-machine-ip`
3. Test connection: `ssh username@local-machine-ip`

### Cannot Push to Non-Bare Repository

If you accidentally created a non-bare repository:
```bash
git config --bool core.bare true
cd ..
mv .git meta.git
```

### Remote Already Exists

If you see "remote local already exists":
```bash
# Remove the existing remote
git remote remove local

# Add it again with correct configuration
git remote add local <path>
```

## Advanced Configuration

### Setting Up Multiple Local Remotes

You can set up multiple local remotes for different purposes:

```bash
git remote add local-backup ~/backups/meta.git
git remote add local-dev ~/development/meta.git
git remote add local-production ~/production/meta.git
```

### Push to All Remotes Automatically

Configure a special remote that pushes to multiple locations:

```bash
git remote add all-remotes ~/git-repositories/meta.git
git remote set-url --add --push all-remotes ~/git-repositories/meta.git
git remote set-url --add --push all-remotes https://github.com/michaelanticoli/meta.git

# Now pushing to all-remotes pushes to both
git push all-remotes main
```

## Security Considerations

- **Bare repositories**: Safer for receiving pushes as they don't have working files that could be overwritten
- **SSH keys**: Use SSH keys instead of passwords for authentication
- **Network security**: If exposing your local machine to the network, use SSH with key-based authentication
- **Backups**: Consider encrypting sensitive data before pushing to local storage

## Additional Resources

- [Git Remote Documentation](https://git-scm.com/docs/git-remote)
- [Git Push Documentation](https://git-scm.com/docs/git-push)
- [Pro Git Book - Working with Remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)

## Support

For issues specific to this repository, please open an issue on GitHub.
