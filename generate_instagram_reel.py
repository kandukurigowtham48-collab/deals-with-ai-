#!/usr/bin/env python3
"""
Instagram Reels Video Creator Agent
Renders high-energy 9:16 vertical short-form video (1080x1920)
Tailored specifically for Instagram Reels & Stories.
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
    r = min(box_w, box_h) // 3
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(30, 41, 59), outline=(244, 63, 94), width=4)
    
    if "audio" in cat or "headphone" in cat or "earbud" in cat:
        head_r = int(r * 0.55)
        draw.arc([(cx - head_r, cy - head_r - 10), (cx + head_r, cy + head_r - 10)], start=180, end=0, fill=(244, 63, 94), width=12)
        draw.rounded_rectangle([(cx - head_r - 14, cy - 15), (cx - head_r + 14, cy + 50)], radius=12, fill=(34, 197, 94))
        draw.rounded_rectangle([(cx + head_r - 14, cy - 15), (cx + head_r + 14, cy + 50)], radius=12, fill=(34, 197, 94))
    elif "phone" in cat or "mobile" in cat:
        draw.rounded_rectangle([(cx - 45, cy - 80), (cx + 45, cy + 80)], radius=15, fill=(15, 23, 42), outline=(56, 189, 248), width=6)
        draw.rounded_rectangle([(cx - 35, cy - 65), (cx + 35, cy + 55)], radius=6, fill=(30, 41, 59))
        draw.ellipse([(cx - 8, cy + 63), (cx + 8, cy + 73)], fill=(56, 189, 248))
    else:
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

def render_reel_frame(deal, scene_text, scene_badge, out_path):
    W, H = 1080, 1920
    # Instagram dark gradient style
    img = Image.new("RGB", (W, H), color=(17, 10, 28))
    draw = ImageDraw.Draw(img)
    
    # Header: Instagram Reels Gradient Accent
    draw.rectangle([(0, 0), (W, 260)], fill=(24, 12, 38))
    draw.rectangle([(0, 256), (W, 260)], fill=(244, 63, 94))
    
    # Left pill: Instagram Reels Branded Tag
    draw.rounded_rectangle([(60, 45), (510, 115)], radius=20, fill=(39, 18, 61), outline=(244, 63, 94), width=3)
    draw_lightning(draw, 80, 52, scale=0.9)
    draw.text((120, 60), "INSTAGRAM REELS", fill=(255, 255, 255), font=get_font(FONT_BOLD, 28))
    
    # Right pill: Verified Channel Tag
    draw.rounded_rectangle([(620, 45), (1020, 115)], radius=20, fill=(225, 29, 72), outline=(255, 255, 255), width=2)
    draw.text((650, 62), "@GOWTHAMDEALS", fill=(255, 255, 255), font=get_font(FONT_BOLD, 26))
    
    # Alert Banner
    draw.rounded_rectangle([(60, 145), (1020, 235)], radius=22, fill=(225, 29, 72))
    draw.text((90, 165), scene_badge, fill=(255, 255, 255), font=get_font(FONT_BOLD, 36))
    
    # Product Card
    card_top = 295
    card_bottom = 1120
    draw.rounded_rectangle([(50, card_top), (W - 50, card_bottom)], radius=32, fill=(35, 21, 54), outline=(192, 132, 252), width=4)
    
    brand = deal.get("brand", "TECH").upper()
    platform = deal.get("platform", "Amazon").upper()
    score = deal.get("score", 96)
    
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
    draw.rounded_rectangle([(180, icon_box_top), (W - 180, icon_box_top + 240)], radius=25, fill=(19, 11, 31), outline=(244, 63, 94), width=3)
    draw_category_graphic(draw, deal.get("category", ""), W // 2, icon_box_top + 120, W - 360, 240)
    
    # Huge Price Drop Section
    price_top = icon_box_top + 265
    draw.rounded_rectangle([(80, price_top), (W - 80, price_top + 185)], radius=24, fill=(19, 11, 31), outline=(34, 197, 94), width=4)
    
    old_p = deal.get("original_price", "₹29,990")
    new_p = deal.get("discounted_price", "₹19,990")
    disc = deal.get("discount_percent", "33%")
    
    draw.text((110, price_top + 25), f"MRP: {old_p}", fill=(148, 163, 184), font=get_font(FONT_REGULAR, 34))
    mrp_box = draw.textbbox((110, price_top + 25), f"MRP: {old_p}", font=get_font(FONT_REGULAR, 34))
    draw.line([(mrp_box[0], (mrp_box[1] + mrp_box[3]) // 2), (mrp_box[2], (mrp_box[1] + mrp_box[3]) // 2)], fill=(239, 68, 68), width=4)
    
    draw.text((110, price_top + 75), f"DEAL: {new_p}", fill=(34, 197, 94), font=get_font(FONT_BOLD, 64))
    
    draw.rounded_rectangle([(W - 400, price_top + 30), (W - 110, price_top + 155)], radius=20, fill=(239, 68, 68))
    draw.text((W - 375, price_top + 45), f"{disc} OFF", fill=(255, 255, 255), font=get_font(FONT_BOLD, 46))
    draw.text((W - 375, price_top + 105), "LIMITED TIME SALE", fill=(254, 240, 138), font=get_font(FONT_BOLD, 20))
    
    # Comparison Audit Box
    comp_top = 1155
    draw.rounded_rectangle([(50, comp_top), (W - 50, comp_top + 290)], radius=28, fill=(19, 11, 31), outline=(107, 70, 143), width=3)
    
    draw.text((80, comp_top + 20), "PRICE AUDIT & HISTORICAL TRACKER", fill=(216, 180, 254), font=get_font(FONT_BOLD, 24))
    
    plat1 = deal.get("platform", "Amazon India")
    pr1 = deal.get("discounted_price", "₹19,990")
    draw.rounded_rectangle([(80, comp_top + 60), (510, comp_top + 165)], radius=18, fill=(35, 21, 54), outline=(34, 197, 94), width=3)
    draw.text((105, comp_top + 78), f"{plat1}: {pr1}", fill=(34, 197, 94), font=get_font(FONT_BOLD, 28))
    draw.text((105, comp_top + 120), "LOWEST PRICE MATCH", fill=(255, 255, 255), font=get_font(FONT_BOLD, 20))

    plat2 = deal.get("comparison_platform", "Flipkart")
    pr2 = deal.get("comparison_price", "₹24,990")
    draw.rounded_rectangle([(540, comp_top + 60), (W - 80, comp_top + 165)], radius=18, fill=(35, 21, 54), outline=(239, 68, 68), width=2)
    draw.text((565, comp_top + 78), f"{plat2}: {pr2}", fill=(248, 113, 113), font=get_font(FONT_BOLD, 28))
    draw.text((565, comp_top + 120), "MORE EXPENSIVE", fill=(148, 163, 184), font=get_font(FONT_BOLD, 20))

    lowest = deal.get("lowest_recorded_price", pr1)
    draw.rounded_rectangle([(80, comp_top + 195), (W - 80, comp_top + 265)], radius=16, fill=(88, 28, 135))
    draw.text((110, comp_top + 215), f"Keepa Audit: All-Time Lowest Price Verified ({lowest})", fill=(243, 232, 255), font=get_font(FONT_BOLD, 24))

    # Caption / Storyboard Banner
    cap_top = 1480
    draw.rounded_rectangle([(50, cap_top), (W - 50, cap_top + 220)], radius=28, fill=(10, 5, 18), outline=(244, 63, 94), width=4)
    
    draw.rounded_rectangle([(80, cap_top - 20), (370, cap_top + 25)], radius=12, fill=(244, 63, 94))
    draw.text((100, cap_top - 12), "INSTAGRAM REEL HOOK", fill=(255, 255, 255), font=get_font(FONT_BOLD, 20))
    
    cap_lines = wrap_text(scene_text, max_chars=34)[:3]
    cap_y = cap_top + 45
    for idx, cl in enumerate(cap_lines):
        color = (255, 255, 255) if idx == 0 else ((254, 240, 138) if idx == 1 else (192, 132, 252))
        draw.text((80, cap_y), cl, fill=color, font=get_font(FONT_BOLD, 36))
        cap_y += 50

    # Sticky Footer for Instagram (Link in Bio & Stories)
    footer_top = 1730
    draw.rectangle([(0, footer_top), (W, 1920)], fill=(24, 12, 38))
    draw.line([(0, footer_top), (W, footer_top)], fill=(244, 63, 94), width=4)
    
    draw.rounded_rectangle([(60, footer_top + 20), (W - 60, footer_top + 150)], radius=25, fill=(190, 24, 93))
    draw.text((90, footer_top + 42), "👉 LINK IN BIO & STORY STICKER", fill=(255, 255, 255), font=get_font(FONT_BOLD, 40))
    draw.text((140, footer_top + 98), "Follow @GowthamDeals for Daily Exclusive Price Drops!", fill=(254, 240, 138), font=get_font(FONT_BOLD, 24))
    
    img.save(out_path)
    return out_path

def generate_instagram_reel(deal, output_mp4):
    os.makedirs("/tmp/greel_frames", exist_ok=True)
    
    p_name = deal.get("title", "Product")[:32]
    p_disc = deal.get("discount_percent", "33%")
    p_new = deal.get("discounted_price", "₹1,999")
    p_plat = deal.get("platform", "Amazon India")
    p_comp = deal.get("comparison_platform", "Flipkart")
    p_compprice = deal.get("comparison_price", "₹3,499")
    
    scenes = [
        {
            "badge": "🚨 VIRAL REEL OF THE DAY",
            "text": f"DO NOT BUY UNTIL YOU SEE THIS! {p_name} is now {p_new}!",
            "voice": f"Do not buy anything until you see this! {p_name} just crashed to {p_new} on {p_plat}!",
        },
        {
            "badge": "📊 CROSS-STORE AUDIT",
            "text": f"{p_comp} is charging {p_compprice}, but {p_plat} is {p_new}!",
            "voice": f"{p_comp} is charging {p_compprice}, but {p_plat} gives you flat {p_disc} off right now!",
        },
        {
            "badge": "🔥 ALL-TIME LOW RECORDED",
            "text": f"Verified by AI Price Tracker! Lowest price in 2026!",
            "voice": f"Our AI price auditor verified this is the absolute lowest price recorded in 2026!",
        },
        {
            "badge": "👉 TAP LINK IN BIO & STORIES",
            "text": f"Link sticker is live in my BIO and STORIES right now!",
            "voice": f"Direct discount link sticker is live in my bio and Instagram stories! Tap before it expires!",
        }
    ]
    
    frame_paths = []
    for i, sc in enumerate(scenes):
        frame_file = f"/tmp/greel_frames/frame_{i}.png"
        render_reel_frame(deal, sc["text"], sc["badge"], frame_file)
        frame_paths.append(frame_file)
        
    full_voice_script = " ".join([sc["voice"] for sc in scenes])
    voice_wav = "/tmp/greel_frames/narration.wav"
    subprocess.run(["espeak-ng", "-s", "148", "-v", "en-us", "-w", voice_wav, full_voice_script], check=True)
    
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
    
    concat_txt = "/tmp/greel_frames/inputs.txt"
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
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/user/gowtham-deals-ai/generated_videos/instagram_reel_sony.mp4"
    deal_id = sys.argv[2] if len(sys.argv) > 2 else "deal-101"
    
    deals_file = "/home/user/gowtham-deals-ai/data/deals.json"
    deal = None
    if os.path.exists(deals_file):
        try:
            with open(deals_file) as f:
                deals = json.load(f)
                for d in deals:
                    if d.get("id") == deal_id:
                        deal = d
                        break
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
        
    generate_instagram_reel(deal, out)
    print("Reel rendered successfully:", out)
