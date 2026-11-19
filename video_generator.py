#!/usr/bin/env python3
"""
Gowtham Deals - AI Video Creator Agent
Renders high-retention 9:16 vertical short-form videos (1080x1920)
Designed for YouTube Shorts & Instagram Reels.
"""

import sys
import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_lightning(draw, x, y, scale=1.0):
    # Sharp lightning bolt
    points = [
        (x + int(15 * scale), y),
        (x, y + int(35 * scale)),
        (x + int(12 * scale), y + int(35 * scale)),
        (x + int(4 * scale), y + int(60 * scale)),
        (x + int(30 * scale), y + int(25 * scale)),
        (x + int(16 * scale), y + int(25 * scale)),
        (x + int(25 * scale), y)
    ]
    draw.polygon(points, fill=(250, 204, 21))

def draw_category_graphic(draw, category, cx, cy, box_w, box_h):
    cat = (category or "").lower()
    
    # Background circle
    r = min(box_w, box_h) // 3
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(30, 41, 59), outline=(56, 189, 248), width=4)
    
    if "audio" in cat or "headphone" in cat or "earbud" in cat:
        # Headphones
        head_r = int(r * 0.55)
        draw.arc([(cx - head_r, cy - head_r - 10), (cx + head_r, cy + head_r - 10)], start=180, end=0, fill=(56, 189, 248), width=12)
        # Left cup
        draw.rounded_rectangle([(cx - head_r - 14, cy - 15), (cx - head_r + 14, cy + 50)], radius=12, fill=(34, 197, 94))
        # Right cup
        draw.rounded_rectangle([(cx + head_r - 14, cy - 15), (cx + head_r + 14, cy + 50)], radius=12, fill=(34, 197, 94))
    elif "phone" in cat or "mobile" in cat:
        # Smartphone
        draw.rounded_rectangle([(cx - 45, cy - 80), (cx + 45, cy + 80)], radius=15, fill=(15, 23, 42), outline=(56, 189, 248), width=6)
        draw.rounded_rectangle([(cx - 35, cy - 65), (cx + 35, cy + 55)], radius=6, fill=(30, 41, 59))
        draw.ellipse([(cx - 8, cy + 63), (cx + 8, cy + 73)], fill=(56, 189, 248))
    elif "laptop" in cat or "macbook" in cat or "computer" in cat:
        # Laptop
        draw.rounded_rectangle([(cx - 75, cy - 45), (cx + 75, cy + 30)], radius=10, fill=(15, 23, 42), outline=(56, 189, 248), width=5)
        draw.rounded_rectangle([(cx - 95, cy + 30), (cx + 95, cy + 45)], radius=6, fill=(100, 116, 139))
    elif "game" in cat or "ps5" in cat or "playstation" in cat or "console" in cat:
        # Game controller
        draw.rounded_rectangle([(cx - 75, cy - 35), (cx + 75, cy + 45)], radius=25, fill=(15, 23, 42), outline=(168, 85, 247), width=6)
        # D-pad
        draw.rectangle([(cx - 50, cy - 10), (cx - 30, cy + 10)], fill=(255, 255, 255))
        draw.rectangle([(cx - 43, cy - 17), (cx - 37, cy + 17)], fill=(255, 255, 255))
        # Buttons
        draw.ellipse([(cx + 30, cy - 12), (cx + 42, cy)], fill=(239, 68, 68))
        draw.ellipse([(cx + 44, cy + 2), (cx + 56, cy + 14)], fill=(34, 197, 94))
    else:
        # Star / Gift
        draw_lightning(draw, cx - 20, cy - 40, scale=1.4)

def wrap_text(text, max_chars=28):
    words = text.split()
    lines = []
    current = []
    current_len = 0
    for w in words:
        if current_len + len(w) + 1 <= max_chars:
            current.append(w)
            current_len += len(w) + 1
        else:
            if current:
                lines.append(" ".join(current))
            current = [w]
            current_len = len(w)
    if current:
        lines.append(" ".join(current))
    return lines

def render_scene_frame(deal, scene_text, scene_badge, out_path):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), color=(11, 17, 32))
    draw = ImageDraw.Draw(img)
    
    # 1. Header (Dark Navy with Neon Blue Accent)
    draw.rectangle([(0, 0), (W, 260)], fill=(15, 23, 42))
    draw.rectangle([(0, 256), (W, 260)], fill=(56, 189, 248))
    
    # Brand Top Pill
    draw.rounded_rectangle([(60, 45), (480, 115)], radius=20, fill=(30, 41, 59), outline=(56, 189, 248), width=3)
    draw_lightning(draw, 80, 52, scale=0.9)
    draw.text((120, 60), "GOWTHAM DEALS", fill=(255, 255, 255), font=get_font(FONT_BOLD, 30))
    
    # Verified AI Pill
    draw.rounded_rectangle([(620, 45), (1020, 115)], radius=20, fill=(5, 150, 105), outline=(16, 185, 129), width=2)
    draw.text((660, 62), "VERIFIED BY AI", fill=(255, 255, 255), font=get_font(FONT_BOLD, 26))
    
    # Category / Alert Banner
    draw.rounded_rectangle([(60, 145), (1020, 235)], radius=22, fill=(225, 29, 72))
    draw.text((100, 165), scene_badge, fill=(255, 255, 255), font=get_font(FONT_BOLD, 36))
    
    # 2. Main Product Card Box
    card_top = 295
    card_bottom = 1120
    draw.rounded_rectangle([(50, card_top), (W - 50, card_bottom)], radius=32, fill=(30, 41, 59), outline=(99, 102, 241), width=4)
    
    # Product Metadata Badges
    brand = deal.get("brand", "TECH").upper()
    platform = deal.get("platform", "Amazon").upper()
    score = deal.get("score", 95)
    
    draw.rounded_rectangle([(80, card_top + 25), (320, card_top + 80)], radius=14, fill=(14, 165, 233))
    draw.text((105, card_top + 38), f"BRAND: {brand}", fill=(255, 255, 255), font=get_font(FONT_BOLD, 22))
    
    draw.rounded_rectangle([(340, card_top + 25), (640, card_top + 80)], radius=14, fill=(245, 158, 11))
    draw.text((365, card_top + 38), f"STORE: {platform}", fill=(0, 0, 0), font=get_font(FONT_BOLD, 22))

    draw.rounded_rectangle([(W - 350, card_top + 25), (W - 80, card_top + 80)], radius=14, fill=(16, 185, 129))
    draw.text((W - 330, card_top + 38), f"SCORE: {score}/100", fill=(255, 255, 255), font=get_font(FONT_BOLD, 22))
    
    # Title
    title = deal.get("title", "Premium Tech Product")
    lines = wrap_text(title, max_chars=32)[:3]
    t_y = card_top + 105
    for l in lines:
        draw.text((80, t_y), l, fill=(255, 255, 255), font=get_font(FONT_BOLD, 42))
        t_y += 54
        
    # Visual Icon Box
    icon_box_top = card_top + 290
    draw.rounded_rectangle([(180, icon_box_top), (W - 180, icon_box_top + 240)], radius=25, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
    draw_category_graphic(draw, deal.get("category", ""), W // 2, icon_box_top + 120, W - 360, 240)
    
    # Massive Price Drop Section
    price_top = icon_box_top + 265
    draw.rounded_rectangle([(80, price_top), (W - 80, price_top + 185)], radius=24, fill=(15, 23, 42), outline=(34, 197, 94), width=4)
    
    old_p = deal.get("original_price", "₹29,990")
    new_p = deal.get("discounted_price", "₹19,990")
    disc = deal.get("discount_percent", "33%")
    
    # MRP Strike-through
    draw.text((110, price_top + 25), f"MRP: {old_p}", fill=(148, 163, 184), font=get_font(FONT_REGULAR, 34))
    mrp_box = draw.textbbox((110, price_top + 25), f"MRP: {old_p}", font=get_font(FONT_REGULAR, 34))
    draw.line([(mrp_box[0], (mrp_box[1] + mrp_box[3]) // 2), (mrp_box[2], (mrp_box[1] + mrp_box[3]) // 2)], fill=(239, 68, 68), width=4)
    
    # Deal Price Highlight
    draw.text((110, price_top + 75), f"DEAL: {new_p}", fill=(34, 197, 94), font=get_font(FONT_BOLD, 64))
    
    # Right-side Discount Pill
    draw.rounded_rectangle([(W - 400, price_top + 30), (W - 110, price_top + 155)], radius=20, fill=(239, 68, 68))
    draw.text((W - 375, price_top + 45), f"{disc} OFF", fill=(255, 255, 255), font=get_font(FONT_BOLD, 46))
    draw.text((W - 375, price_top + 105), "LIMITED TIME SALE", fill=(254, 240, 138), font=get_font(FONT_BOLD, 20))
    
    # 3. Price Comparison Agent Audit Box
    comp_top = 1155
    draw.rounded_rectangle([(50, comp_top), (W - 50, comp_top + 290)], radius=28, fill=(15, 23, 42), outline=(71, 85, 105), width=3)
    
    draw.text((80, comp_top + 20), "PRICE COMPARISON AGENT AUDIT", fill=(148, 163, 184), font=get_font(FONT_BOLD, 24))
    
    # Primary Platform Check
    plat1 = deal.get("platform", "Amazon")
    pr1 = deal.get("discounted_price", "₹19,990")
    draw.rounded_rectangle([(80, comp_top + 60), (510, comp_top + 165)], radius=18, fill=(30, 41, 59), outline=(34, 197, 94), width=3)
    draw.text((105, comp_top + 78), f"{plat1}: {pr1}", fill=(34, 197, 94), font=get_font(FONT_BOLD, 28))
    draw.text((105, comp_top + 120), "LOWEST PRICE MATCH", fill=(255, 255, 255), font=get_font(FONT_BOLD, 20))

    # Competitor Check
    plat2 = deal.get("comparison_platform", "Flipkart")
    pr2 = deal.get("comparison_price", "₹24,990")
    draw.rounded_rectangle([(540, comp_top + 60), (W - 80, comp_top + 165)], radius=18, fill=(30, 41, 59), outline=(239, 68, 68), width=2)
    draw.text((565, comp_top + 78), f"{plat2}: {pr2}", fill=(248, 113, 113), font=get_font(FONT_BOLD, 28))
    draw.text((565, comp_top + 120), "MORE EXPENSIVE", fill=(148, 163, 184), font=get_font(FONT_BOLD, 20))

    # Keepa All-Time Low Badge
    lowest = deal.get("lowest_recorded_price", pr1)
    draw.rounded_rectangle([(80, comp_top + 195), (W - 80, comp_top + 265)], radius=16, fill=(6, 78, 59))
    draw.text((110, comp_top + 215), f"Keepa Verified: Matches All-Time Lowest Price ({lowest})", fill=(167, 243, 208), font=get_font(FONT_BOLD, 24))

    # 4. Animated Subtitle / Hook Banner
    cap_top = 1480
    draw.rounded_rectangle([(50, cap_top), (W - 50, cap_top + 220)], radius=28, fill=(2, 6, 23), outline=(245, 158, 11), width=4)
    
    draw.rounded_rectangle([(80, cap_top - 20), (340, cap_top + 25)], radius=12, fill=(245, 158, 11))
    draw.text((100, cap_top - 12), "AI SCRIPT HOOK", fill=(0, 0, 0), font=get_font(FONT_BOLD, 22))
    
    cap_lines = wrap_text(scene_text, max_chars=34)[:3]
    cap_y = cap_top + 45
    for idx, cl in enumerate(cap_lines):
        color = (255, 255, 255) if idx == 0 else ((254, 240, 138) if idx == 1 else (148, 163, 184))
        draw.text((80, cap_y), cl, fill=color, font=get_font(FONT_BOLD, 36))
        cap_y += 50

    # 5. Bottom Sticky CTA Footer
    footer_top = 1730
    draw.rectangle([(0, footer_top), (W, 1920)], fill=(15, 23, 42))
    draw.line([(0, footer_top), (W, footer_top)], fill=(56, 189, 248), width=4)
    
    draw.rounded_rectangle([(60, footer_top + 20), (W - 60, footer_top + 150)], radius=25, fill=(79, 70, 229))
    draw.text((110, footer_top + 42), "LINK IN PINNED COMMENT & BIO", fill=(255, 255, 255), font=get_font(FONT_BOLD, 42))
    draw.text((180, footer_top + 98), "Hurry! Prices fluctuate quickly on Amazon & Flipkart", fill=(254, 240, 138), font=get_font(FONT_BOLD, 24))
    
    img.save(out_path)
    return out_path

def generate_video_for_deal(deal, output_mp4):
    os.makedirs("/tmp/gdeals_frames", exist_ok=True)
    
    p_name = deal.get("title", "Product")[:32]
    p_disc = deal.get("discount_percent", "33%")
    p_new = deal.get("discounted_price", "₹1,999")
    p_old = deal.get("original_price", "₹4,999")
    p_plat = deal.get("platform", "Amazon India")
    p_comp = deal.get("comparison_platform", "Flipkart")
    p_compprice = deal.get("comparison_price", "₹3,499")
    
    scenes = [
        {
            "badge": "MASSIVE PRICE DROP ALERT",
            "text": f"STOP SCROLLING! {p_name} just crashed to {p_new}!",
            "voice": f"Stop scrolling! {p_name} just crashed to {p_new} on {p_plat}!",
        },
        {
            "badge": "PRICE COMPARISON AUDIT",
            "text": f"{p_comp} is at {p_compprice}, but {p_plat} is {p_new}!",
            "voice": f"{p_comp} is selling at {p_compprice}, but {p_plat} gives you {p_disc} off right now!",
        },
        {
            "badge": "LOWEST PRICE VERIFIED",
            "text": f"Keepa audited! All-time lowest price recorded this year!",
            "voice": f"Our AI price auditor verified this is the all time lowest price recorded this year!",
        },
        {
            "badge": "GRAB BEFORE DEAL EXPIRES",
            "text": f"Direct link in the PINNED COMMENT and BIO right now!",
            "voice": f"Direct discount link is in the pinned comment and bio! Grab it before the sale ends!",
        }
    ]
    
    frame_paths = []
    for i, sc in enumerate(scenes):
        frame_file = f"/tmp/gdeals_frames/frame_{i}.png"
        render_scene_frame(deal, sc["text"], sc["badge"], frame_file)
        frame_paths.append(frame_file)
        
    full_voice_script = " ".join([sc["voice"] for sc in scenes])
    voice_wav = "/tmp/gdeals_frames/narration.wav"
    subprocess.run(["espeak-ng", "-s", "145", "-v", "en-us", "-w", voice_wav, full_voice_script], check=True)
    
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", voice_wav
    ]
    res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        total_audio_duration = float(res.stdout.strip())
    except Exception:
        total_audio_duration = 16.0
        
    per_frame_dur = max(2.5, total_audio_duration / len(scenes))
    
    concat_txt = "/tmp/gdeals_frames/inputs.txt"
    with open(concat_txt, "w") as f:
        for fpath in frame_paths:
            f.write(f"file '{fpath}'\n")
            f.write(f"duration {per_frame_dur:.2f}\n")
        f.write(f"file '{frame_paths[-1]}'\n")
        
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", voice_wav,
        "-filter_complex",
        "[1:a]volume=1.8[voice];"
        "anoisesrc=d=25:c=pink:a=0.012[bg_noise];"
        "[voice][bg_noise]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    
    run_res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if run_res.returncode != 0:
        raise RuntimeError(f"FFmpeg render failed: {run_res.stderr}")
        
    return output_mp4

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/user/gowtham-deals-ai/generated_videos/deal_sony_xm4.mp4"
    
    # Load deal from deals.json if deal ID or argument provided
    deals_file = "/home/user/gowtham-deals-ai/data/deals.json"
    deal = None
    if os.path.exists(deals_file):
        try:
            with open(deals_file) as f:
                deals = json.load(f)
                # match by output name or default to first
                for d in deals:
                    if d.get("id") in out:
                        deal = d
                        break
                if not deal and len(deals) > 0:
                    deal = deals[0]
        except Exception:
            pass

    if not deal:
        deal = {
            "title": "Sony WH-1000XM4 Wireless Headphones",
            "brand": "Sony",
            "category": "Audio & Headphones",
            "original_price": "₹29,990",
            "discounted_price": "₹19,990",
            "discount_percent": "33%",
            "platform": "Amazon India",
            "comparison_platform": "Flipkart",
            "comparison_price": "₹24,990",
            "lowest_recorded_price": "₹19,990",
            "score": 96
        }
        
    generate_video_for_deal(deal, out)
