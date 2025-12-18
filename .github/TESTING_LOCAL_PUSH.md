# Testing Guide: Local Push Feature

This document provides test scenarios to verify the local push functionality.

## Prerequisites for Testing

- Git installed on your system
- Basic command line knowledge
- Access to a local machine or directory for testing

## Test Scenarios

### Test 1: Documentation Accessibility

**Objective**: Verify all documentation files are accessible and readable.

**Steps**:
1. Open `PUSH_TO_LOCAL.md`
2. Open `.github/LOCAL_PUSH_QUICKSTART.md`
3. Check README.md for the "Pushing to Local Machine" section

**Expected Result**: All files should be present and contain comprehensive information.

### Test 2: Script Syntax Validation

**Objective**: Verify scripts have no syntax errors.

**Steps**:
```bash
bash -n setup-local-remote.sh
bash -n push-all.sh
```

**Expected Result**: No output (indicating no syntax errors).

### Test 3: Setup Script - Same Machine

**Objective**: Test setting up a local remote on the same machine.

**Steps**:
```bash
# Create a test directory
mkdir -p /tmp/test-local-git

# Run setup script (you'll need to interact with it)
./setup-local-remote.sh
# Choose option 1 (Same machine)
# Enter path: /tmp/test-local-git/meta.git
# Confirm creation: Y
# Push now: Y
```

**Expected Result**: 
- Bare repository created at specified path
- Local remote configured
- Initial push succeeds

**Cleanup**:
```bash
git remote remove local
rm -rf /tmp/test-local-git
```

### Test 4: Manual Local Remote Setup

**Objective**: Verify manual setup instructions work.

**Steps**:
```bash
# Create bare repository
mkdir -p /tmp/manual-test
git init --bare /tmp/manual-test/meta.git

# Add remote
git remote add local /tmp/manual-test/meta.git

# Verify
git remote -v | grep local

# Push
git push local $(git branch --show-current)
```

**Expected Result**: 
- Remote added successfully
- Push completes without errors

**Cleanup**:
```bash
git remote remove local
rm -rf /tmp/manual-test
```

### Test 5: Push All Script

**Objective**: Test the push-all script with configured remotes.

**Steps**:
```bash
# Setup local remote first
mkdir -p /tmp/push-all-test
git init --bare /tmp/push-all-test/meta.git
git remote add local /tmp/push-all-test/meta.git

# Run push-all script
./push-all.sh
```

**Expected Result**:
- Script detects current branch
- Attempts to push to origin
- Pushes to local successfully
- Shows success/failure status for each remote

**Cleanup**:
```bash
git remote remove local
rm -rf /tmp/push-all-test
```

### Test 6: Push All Script - No Local Remote

**Objective**: Verify graceful handling when local remote isn't configured.

**Steps**:
```bash
# Ensure no local remote exists
git remote remove local 2>/dev/null || true

# Run push-all script
./push-all.sh
```

**Expected Result**:
- Script continues execution
- Shows message about local remote being optional
- References documentation for setup

### Test 7: Script Executability

**Objective**: Verify scripts have execute permissions.

**Steps**:
```bash
ls -l setup-local-remote.sh push-all.sh
```

**Expected Result**: Both files should have execute permissions (rwxr-xr-x or similar).

### Test 8: Documentation Links

**Objective**: Verify all documentation links are valid.

**Steps**:
1. Open README.md
2. Click on link to PUSH_TO_LOCAL.md
3. Open PUSH_TO_LOCAL.md
4. Verify all internal links work

**Expected Result**: All links should resolve to existing files or valid URLs.

## Integration Tests

### Integration Test 1: Full Workflow

**Objective**: Test complete workflow from setup to push.

**Steps**:
```bash
# 1. Run interactive setup
./setup-local-remote.sh
# Follow prompts to set up local remote

# 2. Make a test change
echo "# Test" >> /tmp/test-file.txt

# 3. Commit change
git add /tmp/test-file.txt
git commit -m "Test commit for local push"

# 4. Push to all remotes
./push-all.sh

# 5. Verify push in local repository
cd <path-to-local-bare-repo>
git log --oneline -1

# 6. Cleanup
rm /tmp/test-file.txt
```

**Expected Result**: 
- Setup completes successfully
- Commit is pushed to local remote
- Commit appears in local repository log

### Integration Test 2: Multiple Branches

**Objective**: Test pushing multiple branches to local.

**Steps**:
```bash
# Setup local remote
mkdir -p /tmp/multi-branch-test
git init --bare /tmp/multi-branch-test/meta.git
git remote add local /tmp/multi-branch-test/meta.git

# Push all branches
git push local --all

# Verify in local repository
cd /tmp/multi-branch-test/meta.git
git branch -a
```

**Expected Result**: All branches are pushed to local remote.

**Cleanup**:
```bash
git remote remove local
rm -rf /tmp/multi-branch-test
```

## Error Handling Tests

### Error Test 1: Invalid Path

**Objective**: Test script behavior with invalid paths.

**Steps**:
```bash
./setup-local-remote.sh
# Choose option 1
# Enter an invalid path like: /invalid/path/that/doesnt/exist
# Choose not to create it
```

**Expected Result**: Script should handle gracefully.

### Error Test 2: No Git Repository

**Objective**: Test script behavior outside a git repository.

**Steps**:
```bash
cd /tmp
./path/to/setup-local-remote.sh
```

**Expected Result**: Script should detect and report that it's not in a git repository.

### Error Test 3: Duplicate Remote

**Objective**: Test handling of existing 'local' remote.

**Steps**:
```bash
# Add a local remote
git remote add local /tmp/test.git

# Run setup script
./setup-local-remote.sh
```

**Expected Result**: Script should detect existing remote and offer to reconfigure.

## Performance Tests

### Performance Test 1: Large Repository

**Objective**: Verify push performance with large repositories.

**Steps**:
1. Use a repository with significant history
2. Time the push operation: `time git push local main`

**Expected Result**: Push completes in reasonable time (dependent on repository size).

## Security Tests

### Security Test 1: SSH Key Authentication

**Objective**: Verify SSH-based remote works with key authentication.

**Steps**:
```bash
# Setup SSH-based remote (requires actual SSH server)
./setup-local-remote.sh
# Choose option 2 (SSH)
# Provide valid SSH credentials
```

**Expected Result**: Connection works without password prompt (if keys are set up).

## Documentation Tests

### Doc Test 1: Instructions Accuracy

**Objective**: Verify documentation instructions are accurate and complete.

**Steps**:
1. Follow each instruction in PUSH_TO_LOCAL.md exactly
2. Note any discrepancies or missing information

**Expected Result**: All instructions should work as written.

### Doc Test 2: Troubleshooting Section

**Objective**: Verify troubleshooting steps resolve common issues.

**Steps**:
1. Create a non-bare repository
2. Try to push to it
3. Follow troubleshooting steps to fix

**Expected Result**: Troubleshooting steps resolve the issue.

## Regression Tests

Run these tests after any modifications to ensure functionality hasn't broken:

1. Test 2: Script Syntax Validation
2. Test 4: Manual Local Remote Setup
3. Test 5: Push All Script
4. Integration Test 1: Full Workflow

## Test Results Template

```
Date: ___________
Tester: ___________

Test 1: [ ] Pass [ ] Fail
Test 2: [ ] Pass [ ] Fail
Test 3: [ ] Pass [ ] Fail
Test 4: [ ] Pass [ ] Fail
Test 5: [ ] Pass [ ] Fail
Test 6: [ ] Pass [ ] Fail
Test 7: [ ] Pass [ ] Fail
Test 8: [ ] Pass [ ] Fail

Integration Test 1: [ ] Pass [ ] Fail
Integration Test 2: [ ] Pass [ ] Fail

Error Test 1: [ ] Pass [ ] Fail
Error Test 2: [ ] Pass [ ] Fail
Error Test 3: [ ] Pass [ ] Fail

Notes:
________________________________________________________________________________
________________________________________________________________________________
________________________________________________________________________________
```

## Automated Testing Script

For quick validation, you can run this automated test:

```bash
#!/bin/bash
# automated-test.sh

echo "Running automated tests..."

# Test 1: Syntax validation
echo "Test 1: Syntax validation"
bash -n setup-local-remote.sh && bash -n push-all.sh && echo "✓ Pass" || echo "✗ Fail"

# Test 2: Files exist
echo "Test 2: File existence"
test -f PUSH_TO_LOCAL.md && test -f .github/LOCAL_PUSH_QUICKSTART.md && echo "✓ Pass" || echo "✗ Fail"

# Test 3: Scripts are executable
echo "Test 3: Script executability"
test -x setup-local-remote.sh && test -x push-all.sh && echo "✓ Pass" || echo "✗ Fail"

# Test 4: Git repository check
echo "Test 4: Git repository detection"
git rev-parse --git-dir > /dev/null 2>&1 && echo "✓ Pass" || echo "✗ Fail"

echo "Automated tests complete!"
```
