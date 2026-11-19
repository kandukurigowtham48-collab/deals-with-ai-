#!/bin/bash
# ==============================================================================
# GOWTHAM DEALS - AI MANAGER: 1-CLICK PRODUCTION DEPLOYMENT SCRIPT
# Tested on Ubuntu 22.04 / 24.04 LTS & Debian 12
# ==============================================================================

set -e

echo "🚀 Starting Gowtham Deals AI Manager Deployment..."

# 1. Update Package Index
echo "📦 Updating system packages..."
sudo apt-get update -y

# 2. Install Core Dependencies (Node.js, Python, FFmpeg, espeak-ng)
echo "🛠️ Installing Python3, FFmpeg, audio engine and build tools..."
sudo apt-get install -y \
    curl \
    git \
    ffmpeg \
    espeak-ng \
    python3 \
    python3-pip \
    python3-pil \
    fonts-dejavu-core

# 3. Install Node.js 20 LTS (if not installed)
if ! command -v node &> /dev/null; then
    echo "📦 Installing Node.js 20 LTS..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

echo "✅ Node.js $(node -v) installed."
echo "✅ Python $(python3 --version) installed."
echo "✅ FFmpeg $(ffmpeg -version | head -n 1) installed."

# 4. Install PM2 process manager globally
echo "⚙️ Installing PM2 process manager for 24/7 background execution..."
sudo npm install -g pm2

# 5. Setup Project Directory
APP_DIR="/opt/gowtham-deals-ai"
if [ ! -d "$APP_DIR" ]; then
    echo "📁 Creating application directory at $APP_DIR..."
    sudo mkdir -p "$APP_DIR"
    sudo chown -R $USER:$USER "$APP_DIR"
    cp -r ./* "$APP_DIR/"
fi

cd "$APP_DIR"

# 6. Install NPM dependencies
echo "📦 Installing Node dependencies..."
npm install --omit=dev

# 7. Create essential folders
mkdir -p data generated_videos public

# 8. Create .env if not exists
if [ ! -f ".env" ]; then
    echo "📝 Creating initial .env configuration..."
    cp .env.example .env
fi

# 9. Test Video Generation Engine
echo "🎬 Running sanity check on FFmpeg Video Generator..."
python3 video_generator.py "$APP_DIR/generated_videos/test_render.mp4"
echo "✅ Video rendering sanity check passed!"

# 10. Start Server with PM2 (auto-restart on crash & boot)
echo "🚀 Starting AI Manager server with PM2..."
pm2 delete gowtham-deals-ai 2>/dev/null || true
pm2 start server.js --name "gowtham-deals-ai" --watch false
pm2 save

# Setup PM2 startup script
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u $USER --hp $HOME 2>/dev/null || true

# 11. Final summary
SERVER_IP=$(curl -s https://ifconfig.me || hostname -I | awk '{print $1}')

echo ""
echo "=========================================================================="
echo "🎉 GOWTHAM DEALS - AI MANAGER IS NOW DEPLOYED & RUNNING 24/7!"
echo "=========================================================================="
echo "🌐 Web Dashboard: http://${SERVER_IP}:3000"
echo "📊 PM2 Status:    pm2 status"
echo "📜 Live Logs:     pm2 logs gowtham-deals-ai"
echo "⚙️ Config File:   $APP_DIR/.env"
echo "=========================================================================="
