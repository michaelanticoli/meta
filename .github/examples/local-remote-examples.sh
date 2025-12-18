#!/bin/bash

# local-remote-examples.sh
# Example commands for setting up and using local git remotes
# This file is for reference only - copy and modify commands as needed

# ==============================================================================
# EXAMPLE 1: Simple Same-Machine Setup
# ==============================================================================

# Create a bare repository in your home directory
mkdir -p ~/git-repositories
git init --bare ~/git-repositories/meta.git

# Add it as a remote
git remote add local ~/git-repositories/meta.git

# Push your main branch
git push local main

# ==============================================================================
# EXAMPLE 2: SSH to Another Machine
# ==============================================================================

# On the remote machine, create the bare repository:
# ssh user@192.168.1.100
# mkdir -p ~/git-repositories
# git init --bare ~/git-repositories/meta.git
# exit

# On your local machine, add the SSH remote
git remote add local ssh://user@192.168.1.100/home/user/git-repositories/meta.git

# Push to the remote machine
git push local main
