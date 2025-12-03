#!/bin/bash
# Harbor Ops API Deployment Script for OVH
#
# Usage:
#   ./deploy_to_ovh.sh
#
# This script deploys the Harbor Ops API to the OVH server:
# - Host: 40.160.4.30
# - User: ubuntu
# - SSH Key: .ssh/ovh-rocketchat_ed25519
#
# The script:
# 1. Installs Docker and docker-compose plugin on the server (if not already installed)
# 2. Creates /opt/harbor-ops directory structure
# 3. Syncs necessary files (orchestrator/, pack-crm/, revenue/, deploy/)
# 4. Sets up environment file if missing
# 5. Builds and starts the Docker container
#
# Requirements:
# - SSH key at .ssh/ovh-rocketchat_ed25519 (relative to repo root)
# - rsync installed locally
# - Server: Ubuntu 25.04

set -euo pipefail

# Hardcoded OVH server details
HOST="40.160.4.30"
USER="ubuntu"
SSH_KEY=".ssh/ovh-rocketchat_ed25519"
SSH_TARGET="${USER}@${HOST}"
DEPLOY_DIR="/opt/harbor-ops"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SSH_KEY_PATH="${REPO_ROOT}/${SSH_KEY}"

# Verify SSH key exists
if [ ! -f "${SSH_KEY_PATH}" ]; then
    echo "❌ Error: SSH key not found at ${SSH_KEY_PATH}"
    echo "   Please ensure the key exists and try again."
    exit 1
fi

# Build SSH command with key
SSH_CMD="ssh -i ${SSH_KEY_PATH} -o StrictHostKeyChecking=no"
RSYNC_SSH="ssh -i ${SSH_KEY_PATH} -o StrictHostKeyChecking=no"

echo "=========================================="
echo "Harbor Ops API Deployment to OVH"
echo "=========================================="
echo "Target: ${SSH_TARGET}"
echo "Deploy directory: ${DEPLOY_DIR}"
echo "SSH Key: ${SSH_KEY_PATH}"
echo ""

# Step 1: Install Docker and docker-compose plugin on the server
echo "Step 1: Checking Docker installation..."
${SSH_CMD} "${SSH_TARGET}" bash <<'EOF'
    set -euo pipefail
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "Docker not found. Installing Docker..."
        
        # Update package index
        sudo apt-get update
        
        # Install prerequisites
        sudo apt-get install -y \
            ca-certificates \
            curl \
            gnupg \
            lsb-release
        
        # Add Docker's official GPG key
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        
        # Set up Docker repository
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        
        # Install Docker Engine
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        
        # Enable and start Docker service
        sudo systemctl enable docker
        sudo systemctl start docker
        
        # Add current user to docker group (if not root)
        if [ "$USER" != "root" ]; then
            sudo usermod -aG docker "$USER"
            echo "⚠️  Note: You may need to log out and back in for docker group changes to take effect."
            echo "   For now, using sudo for docker commands."
        fi
        
        echo "✅ Docker installed successfully"
    else
        echo "✅ Docker is already installed"
    fi
    
    # Check if docker compose plugin is available
    if docker compose version &> /dev/null 2>&1 || sudo docker compose version &> /dev/null 2>&1; then
        echo "✅ Docker Compose plugin is available"
    else
        echo "⚠️  Docker Compose plugin not found. Installing..."
        sudo apt-get update
        sudo apt-get install -y docker-compose-plugin
        echo "✅ Docker Compose plugin installed"
    fi
EOF

# Step 2: Create base directory structure on server
echo ""
echo "Step 2: Creating directory structure on server..."
${SSH_CMD} "${SSH_TARGET}" "sudo mkdir -p ${DEPLOY_DIR} && sudo chown -R ${USER}:${USER} ${DEPLOY_DIR}"

# Step 3: Sync necessary files to server
echo ""
echo "Step 3: Syncing files to server..."
echo "  - orchestrator/"
rsync -avz --delete \
    -e "${RSYNC_SSH}" \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.pytest_cache' \
    "${REPO_ROOT}/orchestrator/" \
    "${SSH_TARGET}:${DEPLOY_DIR}/orchestrator/"

echo "  - pack-crm/"
rsync -avz --delete \
    -e "${RSYNC_SSH}" \
    --exclude='data/' \
    --exclude='research/' \
    "${REPO_ROOT}/pack-crm/" \
    "${SSH_TARGET}:${DEPLOY_DIR}/pack-crm/"

echo "  - revenue/"
rsync -avz --delete \
    -e "${RSYNC_SSH}" \
    --exclude='data/' \
    "${REPO_ROOT}/revenue/" \
    "${SSH_TARGET}:${DEPLOY_DIR}/revenue/"

echo "  - deploy/"
rsync -avz \
    -e "${RSYNC_SSH}" \
    "${REPO_ROOT}/deploy/" \
    "${SSH_TARGET}:${DEPLOY_DIR}/deploy/"

# Step 4: Set up environment file if missing
echo ""
echo "Step 4: Checking environment file..."
${SSH_CMD} "${SSH_TARGET}" bash <<EOF
    set -euo pipefail
    cd ${DEPLOY_DIR}/deploy
    
    if [ ! -f harbor_ops.env ]; then
        echo "⚠️  harbor_ops.env not found. Creating from template..."
        cp harbor_ops.env.example harbor_ops.env
        echo ""
        echo "⚠️  ⚠️  ⚠️  IMPORTANT: You must edit harbor_ops.env with real values!"
        echo "    SSH into the server and run:"
        echo "    nano ${DEPLOY_DIR}/deploy/harbor_ops.env"
        echo "    Set OPENAI_API_KEY and any other required env vars."
        echo ""
    else
        echo "✅ harbor_ops.env already exists"
    fi
EOF

# Step 5: Build and start the container
echo ""
echo "Step 5: Building and starting Docker container..."
${SSH_CMD} "${SSH_TARGET}" bash <<EOF
    set -euo pipefail
    cd ${DEPLOY_DIR}/deploy
    
    # Ensure data directories exist
    mkdir -p ../pack-crm/data
    mkdir -p ../pack-crm/research
    mkdir -p ../orchestrator/data/runs
    mkdir -p ../revenue/data
    
    # Use sudo for docker if user is not in docker group yet
    if docker compose version &> /dev/null 2>&1; then
        DOCKER_CMD="docker"
    else
        DOCKER_CMD="sudo docker"
    fi
    
    # Build and start
    \${DOCKER_CMD} compose -f docker-compose.harbor_ops.yml up -d --build
    
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "Container status:"
    \${DOCKER_CMD} compose -f docker-compose.harbor_ops.yml ps
    
    echo ""
    echo "To view logs:"
    echo "  \${DOCKER_CMD} compose -f docker-compose.harbor_ops.yml logs -f"
    echo ""
    echo "To stop:"
    echo "  \${DOCKER_CMD} compose -f docker-compose.harbor_ops.yml down"
EOF

echo ""
echo "=========================================="
echo "Deployment Summary"
echo "=========================================="
echo "✅ Files synced to: ${SSH_TARGET}:${DEPLOY_DIR}"
echo "✅ Container should be running on port 8000"
echo ""
echo "Next steps:"
echo "1. SSH into the server:"
echo "   ssh -i ${SSH_KEY_PATH} ${SSH_TARGET}"
echo "2. Edit env file if needed:"
echo "   nano ${DEPLOY_DIR}/deploy/harbor_ops.env"
echo "   (Set OPENAI_API_KEY and other env vars)"
echo "3. Restart container if env changed:"
echo "   cd ${DEPLOY_DIR}/deploy"
echo "   docker compose -f docker-compose.harbor_ops.yml restart"
echo "4. Check logs:"
echo "   docker compose -f docker-compose.harbor_ops.yml logs -f"
echo ""
echo "To redeploy after code changes, simply run this script again:"
echo "  ./deploy_to_ovh.sh"
