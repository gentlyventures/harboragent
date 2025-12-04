# SECURITY INCIDENT: Exposed SSH Private Key

## Incident Summary
- **Date Detected**: December 4th, 2025, 16:48:50 UTC
- **Detected By**: GitGuardian
- **Secret Type**: OpenSSH Private Key
- **Repository**: gentlyventures/harboragent
- **Key File**: `.ssh/ovh-rocketchat_ed25519`

## Actions Taken

### ✅ Completed
1. **Removed from repository**: SSH key files removed from git tracking
2. **Removed from git history**: Used `git filter-branch` to remove the key from all commits
3. **Updated .gitignore**: Added comprehensive SSH key patterns to prevent future commits:
   - `.ssh/`
   - `*.pem`
   - `*.key`
   - `id_rsa*`, `id_ed25519*`, `id_ecdsa*`
   - `*.pub`

## ⚠️ CRITICAL NEXT STEPS

### 1. Force Push to Remote (REQUIRED)
The key has been removed from local history, but **you must force push to update GitHub**:

```bash
git push origin main --force
```

**WARNING**: This rewrites history. Coordinate with your team if others have cloned the repo.

### 2. Rotate the SSH Key (REQUIRED - DO IMMEDIATELY)
The exposed key is compromised and must be replaced:

#### On your local machine:
```bash
# Generate a new SSH key pair
ssh-keygen -t ed25519 -f ~/.ssh/ovh-rocketchat_ed25519_new -C "OVH Rocket.Chat"

# Copy the new public key
cat ~/.ssh/ovh-rocketchat_ed25519_new.pub
```

#### On the OVH server (40.160.4.30):
1. SSH into the server using the OLD key (while it's still active):
   ```bash
   ssh -i .ssh/ovh-rocketchat_ed25519 ubuntu@40.160.4.30
   ```

2. Add the NEW public key to `~/.ssh/authorized_keys`:
   ```bash
   # Backup current authorized_keys
   cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup
   
   # Add new public key
   echo "NEW_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
   ```

3. Test the new key:
   ```bash
   # From your local machine
   ssh -i ~/.ssh/ovh-rocketchat_ed25519_new ubuntu@40.160.4.30
   ```

4. Once confirmed working, remove the OLD key from `authorized_keys`:
   ```bash
   # On the server
   nano ~/.ssh/authorized_keys
   # Remove the line containing the old public key
   ```

5. Update your local key file:
   ```bash
   # Replace old key with new key
   mv ~/.ssh/ovh-rocketchat_ed25519 ~/.ssh/ovh-rocketchat_ed25519.old
   mv ~/.ssh/ovh-rocketchat_ed25519_new ~/.ssh/ovh-rocketchat_ed25519
   mv ~/.ssh/ovh-rocketchat_ed25519_new.pub ~/.ssh/ovh-rocketchat_ed25519.pub
   ```

6. Update the deployment script if needed:
   - The script at `deploy/deploy_to_ovh.sh` references `.ssh/ovh-rocketchat_ed25519`
   - Ensure the new key is in the same location

### 3. Verify GitGuardian Alert
After force pushing, GitGuardian should automatically re-scan. The alert should clear within 24-48 hours.

### 4. Additional Security Measures
- Review all other repositories for similar exposures
- Consider using SSH agent forwarding or deploy keys instead of committing keys
- Use environment variables or secrets managers for sensitive credentials
- Enable branch protection rules on GitHub to prevent force pushes to main

## Prevention
The `.gitignore` file has been updated to prevent future commits of:
- SSH keys (`.ssh/` directory)
- Private key files (`*.pem`, `*.key`, `id_*`)
- Public keys (`*.pub`)

**Always verify** that sensitive files are in `.gitignore` before committing.

## References
- Key was committed in: `093928a` (December 4th, 2025)
- Removed in: `d39895a` (December 4th, 2025)
- Server: 40.160.4.30 (OVH)
- User: ubuntu

