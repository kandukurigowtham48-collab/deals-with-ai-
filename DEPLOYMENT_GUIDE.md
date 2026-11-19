# 🚀 Deployment Guide: Gowtham Deals – AI Manager

This guide walks you through deploying your automated multi-agent pipeline into 24/7 cloud production so it runs hands-free without keeping your laptop on.

---

## 📋 Recommended Hosting Options

Because the pipeline renders genuine **1080x1920 (9:16) MP4 videos** using FFmpeg and Python, you need a server with at least **1 vCPU and 1 GB to 2 GB RAM**.

| Provider | Recommended Plan | Cost | Best For |
|---|---|---|---|
| **DigitalOcean** | Basic Droplet (1 vCPU, 2GB RAM) | ~$12/mo | Easiest setup & reliable network |
| **Hetzner Cloud** | CX22 (2 vCPU, 4GB RAM) | ~€4/mo (~₹350/mo) | Best value for money |
| **AWS** | EC2 `t3.small` (or `t4g.small`) | Free Tier / ~$14/mo | Enterprise scalability |
| **Hostinger / Linode** | KVM 1 or KVM 2 | ~$5–$8/mo | Budget friendly |

---

## ⚡ Option 1: 1-Click Automated Ubuntu Deployment (Fastest)

Connect to your cloud VPS via SSH:
```bash
ssh root@YOUR_SERVER_IP
```

Clone or upload this repository to your server and run:
```bash
cd gowtham-deals-ai
chmod +x deploy.sh
./deploy.sh
```

### What `deploy.sh` Does Automatically:
1. Installs Node.js 20 LTS, Python 3, PIL, FFmpeg, and `espeak-ng`.
2. Installs PM2 process manager for 24/7 background persistence.
3. Tests the video rendering pipeline.
4. Starts the web server and configures it to auto-restart if the server ever reboots.
5. Displays your live dashboard URL (`http://YOUR_SERVER_IP:3000`).

---

## 🐳 Option 2: Docker / Docker Compose Deployment

If your server has Docker installed:
```bash
# 1. Clone repository
git clone https://github.com/your-username/gowtham-deals-ai.git
cd gowtham-deals-ai

# 2. Copy and configure .env
cp .env.example .env
nano .env

# 3. Start container in detached background mode
docker-compose up -d --build
```

Check logs anytime:
```bash
docker-compose logs -f
```

---

## 🔑 Connecting Real Production APIs

### 1. YouTube Shorts Auto-Publishing (Google Cloud Console)
1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Create a project named **"Gowtham Deals AI"**.
3. In **APIs & Services**, enable **YouTube Data API v3**.
4. Go to **Credentials** ➔ **Create Credentials** ➔ **OAuth 2.0 Client ID** (Web application or Desktop).
5. Add Authorized Redirect URI: `http://localhost:3000/oauth2callback`.
6. Download client credentials and paste `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET` into `.env`.
7. The Social Media Agent will now automatically upload Shorts and **pin the affiliate link comment**!

### 2. Instagram Reels Auto-Publishing (Meta Graph API)
1. Convert your Instagram account (`@gowthamdeals`) to an **Instagram Creator or Business Account** (free in Instagram app settings).
2. Link it to a Facebook Page (e.g. *Gowtham Deals Official*).
3. Go to [Meta for Developers](https://developers.facebook.com) ➔ Create an App ➔ Select **Business**.
4. Add the **Instagram Graph API** product.
5. In Graph API Explorer, request the following permissions:
   * `instagram_basic`
   * `instagram_content_publish`
   * `pages_show_list`
6. Generate a **Never-Expiring Long-Lived User Access Token**.
7. Copy your `META_PAGE_ACCESS_TOKEN` and `INSTAGRAM_ACCOUNT_ID` into `.env`.

### 3. Amazon Associates Tag
In `.env` or in the Admin Dashboard Settings tab:
```env
AMAZON_ASSOCIATE_TAG=gowthamdeals-21
```
All generated links will automatically carry your affiliate tracking tag and UTM parameters.

---

## ⏰ Autonomous 24/7 Cron Schedule

The system is configured by default to run on prime Indian viewing times:
* **09:00 AM** – Morning tech flash sales
* **01:00 PM** – Lunchtime browsing deals
* **06:00 PM** – Evening lightning deals
* **09:00 PM** – Night shopping discounts

To adjust the schedule, open the **Settings** tab in your Central Admin Dashboard or edit `data/settings.json`.

---

## 🛠️ Management & Monitoring Commands

```bash
# Check running status
pm2 status

# View live real-time agent logs
pm2 logs gowtham-deals-ai

# Restart the application
pm2 restart gowtham-deals-ai

# Stop the application
pm2 stop gowtham-deals-ai
```
