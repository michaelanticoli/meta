# Quick Start: Push to Local Machine

This is a quick reference guide for pushing your repository to a local machine.

## TL;DR

```bash
# 1. Run the setup script
./setup-local-remote.sh

# 2. Push to local
git push local main

# 3. Or push to all remotes at once
./push-all.sh main
```

## Manual Setup

### Create bare repository on local machine:
```bash
mkdir -p ~/git-repositories
git init --bare ~/git-repositories/meta.git
```

### Add local remote:
```bash
git remote add local ~/git-repositories/meta.git
```

### Push to local:
```bash
git push local main
```

## SSH Setup (Different Machine)

```bash
# On remote machine:
mkdir -p ~/git-repositories
git init --bare ~/git-repositories/meta.git

# On your working machine:
git remote add local ssh://user@hostname/home/user/git-repositories/meta.git
git push local main
```

## Common Commands

```bash
# List all remotes
git remote -v

# Push current branch to local
git push local $(git branch --show-current)

# Push all branches to local
git push local --all

# Fetch from local
git fetch local

# Remove local remote
git remote remove local
```

## Full Documentation

For complete instructions, troubleshooting, and advanced configurations, see [PUSH_TO_LOCAL.md](../PUSH_TO_LOCAL.md)
