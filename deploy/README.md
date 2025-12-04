# Harbor Ops API Deployment Guide

This directory contains deployment configuration for running the Harbor Ops API on an OVH VM.

## Overview

The Harbor Ops API is a FastAPI backend that provides REST endpoints for:
- Pack lifecycle management (CRUD)
- CRM data updates
- Research pipeline execution
- Revenue/sales data access

## Files

- `Dockerfile.harbor_ops` - Docker image definition for the API
- `docker-compose.harbor_ops.yml` - Docker Compose configuration
- `harbor_ops.env.example` - Environment variables template
- `deploy_to_ovh.sh` - Automated deployment script

## Local Development

### Start the API locally

```bash
# From project root
python -m orchestrator api
```

The API will start on `http://127.0.0.1:8000` with auto-reload enabled.

### Start the frontend

```bash
# From project root
pnpm dev
```

Visit `http://localhost:8081/admin` to access the admin dashboard.

**Note:** The frontend defaults to `http://127.0.0.1:8000` for the API in development. No environment variable needed.

## OVH Production Deployment

### Prerequisites

1. **OVH VM** (already configured):
   - Hostname: `harboragent`
   - IP: `40.160.4.30`
   - OS: Ubuntu 25.04
   - SSH user: `ubuntu`
   - SSH key: `.ssh/ovh-rocketchat_ed25519` (in repo root)

2. **Cloudflare DNS** configuration (manual step):
   - Add A record: `api.harboragent.dev` → `40.160.4.30`
   - Enable Cloudflare proxy (orange cloud) for TLS termination
   - TTL: Auto

3. **Local machine** requirements:
   - SSH key at `.ssh/ovh-rocketchat_ed25519` (relative to repo root)
   - `rsync` installed
   - This repository cloned

### Production Deploy Steps

#### Step 1: Configure Cloudflare DNS

In Cloudflare DNS for `harboragent.dev`, add:

- **Type:** A
- **Name:** api
- **Target:** 40.160.4.30
- **Proxy:** ON (orange cloud)
- **TTL:** Auto

#### Step 2: Deploy to OVH

From your local machine, in the repo root:

```bash
cd deploy
chmod +x deploy_to_ovh.sh
./deploy_to_ovh.sh
```

The script will:
- Install Docker and docker-compose plugin (if not already installed)
- Create `/opt/harbor-ops` directory
- Sync necessary files (orchestrator/, pack-crm/, revenue/, deploy/)
- Set up environment file template
- Build and start the Docker container

**Note:** The script uses hardcoded OVH server details:
- Host: `40.160.4.30`
- User: `ubuntu`
- SSH Key: `.ssh/ovh-rocketchat_ed25519`

#### Step 3: Configure Environment Variables

SSH into the OVH server:

```bash
ssh -i .ssh/ovh-rocketchat_ed25519 ubuntu@40.160.4.30
```

Edit the environment file:

```bash
cd /opt/harbor-ops/deploy
nano harbor_ops.env
```

Set required values:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
HARBOR_ENV=production
```

Restart the container:

```bash
docker compose -f docker-compose.harbor_ops.yml restart
```

#### Step 4: Configure Cloudflare Pages Frontend

In Cloudflare Pages project for `harboragent.dev`:

1. Go to Settings → Environment Variables
2. Add environment variable:
   - **Name:** `VITE_HARBOR_OPS_API_URL`
   - **Value:** `https://api.harboragent.dev`
   - **Environment:** Production (and Preview if desired)
3. Save and redeploy the frontend

#### Step 5: Verify Deployment

1. **Verify API is accessible:**
   ```bash
   # From server
   curl http://localhost:8000/health
   
   # From local machine (after DNS propagates)
   curl https://api.harboragent.dev/health
   ```

2. **Check API docs:**
   - Visit: https://api.harboragent.dev/docs

3. **Test Admin UI:**
   - Visit: https://harboragent.dev/admin
   - Should be able to:
     - List packs
     - Create a new idea
     - Run the research pipeline for a pack

### Redeploying After Code Changes

Simply run the deployment script again:

```bash
cd deploy
./deploy_to_ovh.sh
```

The script is idempotent and will:
- Sync latest code changes
- Rebuild the Docker image
- Restart the container

### Manual Container Management

SSH into the server:

```bash
ssh -i .ssh/ovh-rocketchat_ed25519 ubuntu@40.160.4.30
```

Then use standard docker compose commands:

```bash
cd /opt/harbor-ops/deploy

# View logs
docker compose -f docker-compose.harbor_ops.yml logs -f

# Restart container
docker compose -f docker-compose.harbor_ops.yml restart

# Stop container
docker compose -f docker-compose.harbor_ops.yml down

# Start container
docker compose -f docker-compose.harbor_ops.yml up -d

# Rebuild and restart
docker compose -f docker-compose.harbor_ops.yml up -d --build
```

## Data Persistence

The following directories are mounted as volumes to persist data outside the container:

- `pack-crm/data/` - Pack lifecycle data (packs.json)
- `pack-crm/research/` - Research reports
- `orchestrator/data/runs/` - Research run state JSON files
- `revenue/data/` - Revenue and leads data

These directories are located at:
- `/opt/harbor-ops/pack-crm/data/`
- `/opt/harbor-ops/pack-crm/research/`
- `/opt/harbor-ops/orchestrator/data/runs/`
- `/opt/harbor-ops/revenue/data/`

**Important:** These directories persist even if you rebuild or recreate the container.

## Network Configuration

### CORS Settings

The API is configured to allow requests from:
- `http://localhost:8081` (local dev)
- `http://127.0.0.1:8081` (local dev)
- `https://harboragent.dev` (production frontend)
- `https://api.harboragent.dev` (if needed)

CORS configuration is in `orchestrator/api.py`.

### TLS/HTTPS

The container serves HTTP on port 8000. Cloudflare handles TLS termination:
- Cloudflare proxy (orange cloud) terminates TLS
- Requests to `https://api.harboragent.dev` are proxied to `http://<OVH_IP>:8000`
- No SSL certificates needed in the container

## Weekly Pack Updates (Cron Job)

The Harbor Ops API includes an endpoint to check for updates to published packs (regulation changes, market trends, etc.). Set up a weekly cron job to automatically check all published packs.

### Setup Cron Job on OVH Server

SSH into the server and add a cron job:

```bash
ssh -i .ssh/ovh-rocketchat_ed25519 ubuntu@40.160.4.30
crontab -e
```

Add this line to run weekly checks every Monday at 9 AM UTC:

```cron
0 9 * * 1 curl -X POST https://api.harboragent.dev/api/packs/genesis-mission/check-updates -H "Content-Type: application/json" > /tmp/pack-updates.log 2>&1
```

Or use a script to check all published packs:

```bash
# Create script
cat > /opt/harbor-ops/scripts/weekly-updates.sh << 'EOF'
#!/bin/bash
API_URL="https://api.harboragent.dev"
for pack in genesis-mission tax-assist; do
  curl -X POST "${API_URL}/api/packs/${pack}/check-updates" \
    -H "Content-Type: application/json" \
    >> /tmp/pack-updates.log 2>&1
  echo "" >> /tmp/pack-updates.log
done
EOF

chmod +x /opt/harbor-ops/scripts/weekly-updates.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "0 9 * * 1 /opt/harbor-ops/scripts/weekly-updates.sh") | crontab -
```

**Note:** The update check endpoint is currently a placeholder. Implement actual checks for:
- Regulation/standard changes (monitor official sources)
- Market trends (news APIs, industry reports)
- User feedback aggregation
- Competitive landscape shifts

## Troubleshooting

### Container won't start

1. SSH into the server:
   ```bash
   ssh -i .ssh/ovh-rocketchat_ed25519 ubuntu@40.160.4.30
   ```

2. Check logs:
   ```bash
   cd /opt/harbor-ops/deploy
   docker compose -f docker-compose.harbor_ops.yml logs
   ```

3. Verify environment file exists:
   ```bash
   ls -la /opt/harbor-ops/deploy/harbor_ops.env
   ```

4. Check if port 8000 is already in use:
   ```bash
   sudo netstat -tlnp | grep 8000
   ```

### API returns 500 errors

1. Check container logs for Python errors
2. Verify `OPENAI_API_KEY` is set correctly in `harbor_ops.env`
3. Ensure data directories exist and are writable:
   ```bash
   ls -la /opt/harbor-ops/pack-crm/data/
   ```

### Frontend can't connect to API

1. Verify API is accessible from the server:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check Cloudflare DNS:
   - Ensure `api.harboragent.dev` A record points to OVH VM IP
   - Ensure proxy (orange cloud) is enabled

3. Verify frontend environment variable:
   - In Cloudflare Pages, check `VITE_HARBOR_OPS_API_URL` is set to `https://api.harboragent.dev`

4. Check CORS settings in `orchestrator/api.py` - ensure `https://harboragent.dev` is in `allow_origins`

### Docker installation fails

The deployment script is configured for Ubuntu 25.04. If Docker installation fails:
1. Manually install Docker on the server
2. Run the deployment script again (it will skip Docker installation if already present)

## Security Notes

- **Never commit `harbor_ops.env`** - it contains secrets
- The `harbor_ops.env.example` file is safe to commit (no real values)
- SSH key `.ssh/ovh-rocketchat_ed25519` should be kept secure and never committed
- Consider setting up a firewall on the OVH VM (only allow SSH and port 8000 from Cloudflare IPs)
- The API serves HTTP on port 8000; Cloudflare handles TLS termination

## See Also

- `orchestrator/README.md` - API documentation and usage
- `pack-crm/README.md` - Pack CRM module documentation

