# Gowtham Deals – AI Manager
### End-to-End Autonomous Multi-Agent Pipeline for YouTube Shorts & Instagram Reels

An autonomous AI agent orchestration system that discovers viral e-commerce deals, verifies genuine price cuts across platforms, calculates profit potential, generates 9:16 vertical short videos (1080x1920) with AI voiceover and captions, and publishes them with auto-pinned affiliate links.

---

## 🏗️ Architecture Overview

```
                      ┌─────────────────────────────────┐
                      │   Gowtham Deals - AI Manager    │
                      │  (Master Workflow Orchestrator) │
                      └────────────────┬────────────────┘
                                       │
        ┌──────────────────────────────┴──────────────────────────────┐
        │                                                             │
 ┌──────▼──────────────┐                               ┌──────────────▼──────┐
 │  Deal Hunter Agent  │                               │  Price Comparison   │
 │ (Amazon & Flipkart) │                               │ (Keepa & Cross-API) │
 └──────┬──────────────┘                               └──────────────┬──────┘
        │                                                             │
 ┌──────▼──────────────┐                               ┌──────────────▼──────┐
 │   Affiliate Agent   │                               │ Deal Scoring Agent  │
 │ (Tracking & Links)  │                               │  (0-100 Viral Rank) │
 └──────┬──────────────┘                               └──────────────┬──────┘
        │                                                             │
 ┌──────▼──────────────┐                               ┌──────────────▼──────┐
 │ Video Creator Agent │                               │  Social Media Agent │
 │  (FFmpeg & Speech)  │                               │ (YouTube & Reels)   │
 └──────┬──────────────┘                               └──────────────┬──────┘
        │                                                             │
        └──────────────────────────────┬──────────────────────────────┘
                                       │
                      ┌────────────────▼────────────────┐
                      │    Central Admin Dashboard      │
                      │  (Metrics, Studio & Analytics)  │
                      └────────────────┬────────────────┘
                                       │
                      ┌────────────────┴────────────────┐
                      │                                 │
           ┌──────────▼──────────┐           ┌──────────▼──────────┐
           │   Instagram Reels   │           │   YouTube Shorts    │
           └─────────────────────┘           └─────────────────────┘
```

---

## 🤖 The 6 Specialized Agents & Roles

1. **AI Manager (Director / Master Orchestrator):**
   - Coordinates cron cycles (e.g., every 4 hours).
   - Passes data seamlessly between agents.
   - Maintains system health, state persistence, and audit logs.

2. **Deal Hunter Agent (Trend & Flash Sale Spotter):**
   - Scrapes and tracks Amazon India, Flipkart, Myntra, and Croma.
   - Monitors price drops, lightning deals, and clearance sales.
   - Allows manual product addition or automated e-commerce webhooks.

3. **Price Comparison Agent (Fact Checker & Historical Auditor):**
   - Cross-checks prices between competing platforms (e.g. Amazon vs. Flipkart vs. Reliance Digital).
   - Audits 90-day price history via Keepa / PriceHistory APIs.
   - Detects and rejects fake discounts (e.g. inflated MRP tricks).

4. **Deal Scoring Agent (Quality & Viral Filter):**
   - Evaluates each deal on a 100-point scale across 5 criteria:
     - Discount Depth (30 pts)
     - Historical Low Benchmark (25 pts)
     - Absolute Savings in ₹ (20 pts)
     - Brand Demand & Clout (15 pts)
     - Commission Margin (10 pts)
   - Only deals scoring ≥ 85 are auto-queued for video generation.

5. **Affiliate Agent (Monetization Engine):**
   - Formats Amazon Associate links with `tag=gowthamdeals-21`.
   - Generates branded shortlinks (`https://gdeals.in/...`).
   - Injects platform UTM tags (`utm_source=youtube_shorts`).
   - Verifies link health (HTTP 200 and in-stock verification).

6. **Video Creator Agent (Automated Production Studio):**
   - Generates high-retention 3-second hook scripts, comparison breakdowns, and call-to-actions.
   - Generates synthesized voiceover narration (`espeak-ng` / ElevenLabs / OpenAI Audio).
   - Compiles genuine **1080x1920 (9:16) vertical MP4 videos** using FFmpeg and Pillow.
   - Animates discount badges, strike-through original prices, Keepa verified tags, and Gowtham Deals watermark.

7. **Social Media Agent (YouTube Shorts & Instagram Reels Publisher):**
   - Uploads directly via YouTube Data API v3 and Meta Graph API.
   - Writes high-converting titles, descriptions, and 15 targeted hashtags.
   - **Automatically posts and pins the top comment** containing your affiliate link and urgency disclaimer.

---

## 🚀 Running the System

### 1. Start the Server
```bash
cd /home/user/gowtham-deals-ai
node server.js
```
The dashboard runs at `http://0.0.0.0:3000`.

### 2. Video Rendering Engine
To render a 9:16 vertical Short for any deal:
```bash
python3 video_generator.py /home/user/gowtham-deals-ai/generated_videos/video_deal-101.mp4
```

### 3. File Structure
- `server.js` - Express API backend and agent coordinator.
- `video_generator.py` - High-performance FFmpeg + Pillow 9:16 video renderer.
- `public/` - Responsive Web Dashboard matching the user's mobile diagram.
- `data/deals.json` - Active deals, pricing, scores, scripts, and links.
- `data/agents.json` - Real-time state and agent execution logs.
- `data/settings.json` - Affiliate tags, YouTube/Instagram API tokens, and cron intervals.
- `generated_videos/` - Rendered vertical MP4 videos and thumbnails.
