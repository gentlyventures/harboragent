# Release Setup - GitHub Releases

The Genesis Mission Readiness Pack files are hosted on GitHub Releases for free, secure distribution.

## Current Release

**v1.0.0** is available at:
```
https://github.com/gentlyventures/harboragent/releases/download/v1.0.0/harbor-agent-genesis-pack-v1.0.zip
```

This is the `DOWNLOAD_ORIGIN_URL` value to use in your Worker secrets.

## Creating New Releases

### Option 1: Manual Release (Simplest)

1. Build/create your pack zip file in `dist/`
2. Go to: https://github.com/gentlyventures/harboragent/releases
3. Click "Draft a new release"
4. Tag: `v1.1.0` (or your version)
5. Title: "Harbor Agent — Genesis Mission Readiness Pack v1.1.0"
6. Upload the zip file as an asset
7. Publish release

### Option 2: GitHub Actions Workflow

1. Go to: https://github.com/gentlyventures/harboragent/actions
2. Select "Create Release" workflow
3. Click "Run workflow"
4. Enter version tag (e.g., `v1.1.0`)
5. Run

The workflow will:
- Find the matching zip file in `dist/`
- Create a GitHub release with that version tag
- Upload the zip as a release asset

### Option 3: GitHub CLI

```bash
gh release create v1.1.0 dist/harbor-agent-genesis-pack-v1.1.0.zip \
  --title "Harbor Agent — Genesis Mission Readiness Pack v1.1.0" \
  --notes "Release notes here"
```

## Updating DOWNLOAD_ORIGIN_URL

After creating a new release, update the `DOWNLOAD_ORIGIN_URL` secret:

1. In GitHub Secrets, update `DOWNLOAD_ORIGIN_URL` to:
   ```
   https://github.com/gentlyventures/harboragent/releases/download/v1.1.0/harbor-agent-genesis-pack-v1.1.0.zip
   ```

2. Or update via Wrangler (if testing locally):
   ```bash
   echo "https://github.com/gentlyventures/harboragent/releases/download/v1.1.0/harbor-agent-genesis-pack-v1.1.0.zip" | wrangler secret put DOWNLOAD_ORIGIN_URL
   ```

## URL Format

GitHub Releases URLs follow this pattern:
```
https://github.com/OWNER/REPO/releases/download/TAG/FILENAME.zip
```

For this repo:
```
https://github.com/gentlyventures/harboragent/releases/download/v1.0.0/harbor-agent-genesis-pack-v1.0.zip
```

## Benefits

- ✅ **Free** - No additional costs
- ✅ **Secure** - GitHub handles CDN and security
- ✅ **Versioned** - Each release is tagged and immutable
- ✅ **Fast** - GitHub's CDN is global and fast
- ✅ **Simple** - Uses existing GitHub infrastructure

