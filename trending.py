import time
import csv
from datetime import datetime
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ───── CONFIG ─────
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
NICHES = [
    "AI technology",
    "latest gadgets",
    "smartphone reviews",
    "coding tutorials",
    "tech news",
    "gaming highlights",
    "esports tournaments",
    "crypto news",
    "investing for beginners",
    "startup tips",
    "funny skits",
    "study hacks",
    "time management",
    
]
MAX_PER_NICHE = 7
REFRESH_MINUTES = 30
CSV_FILE = "youtube_trending_by_niche.csv"
# ────────────────────

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_top_videos(query):
    resp = youtube.search().list(
        part="id",
        q=query,
        type="video",
        order="viewCount",
        maxResults=MAX_PER_NICHE
    ).execute()
    return [item["id"]["videoId"] for item in resp.get("items", [])]

def fetch_video_details(video_ids):
    if not video_ids:
        return {}
    resp = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    ).execute()
    out = {}
    for it in resp.get("items", []):
        vid = it["id"]
        out[vid] = {
            "title": it["snippet"]["title"],
            "channel": it["snippet"]["channelTitle"],
            "views": int(it["statistics"].get("viewCount", "0")),
            "duration": it["contentDetails"].get("duration", ""),
            "link": f"https://www.youtube.com/watch?v={vid}"
        }
    return out

def build_and_save():
    all_videos = []
    for niche in NICHES:
        try:
            video_ids = search_top_videos(niche)
            details = fetch_video_details(video_ids)
        except Exception as e:
            print(f"⚠️  Error fetching for niche '{niche}': {e}")
            continue

        for vid in video_ids:
            d = details.get(vid)
            if not d:
                continue
            all_videos.append({
                "niche": niche,
                "title": d["title"],
                "channel": d["channel"],
                "views": d["views"],
                "duration": d["duration"],
                "link": d["link"]
            })

    # Sort by views (highest to lowest)
    all_videos.sort(key=lambda x: x["views"], reverse=True)

    # Write to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "niche", "title", "channel", "views", "duration", "link"])
        for rank, video in enumerate(all_videos, 1):
            w.writerow([
                rank,
                video["niche"],
                video["title"],
                video["channel"],
                video["views"],
                video["duration"],
                video["link"]
            ])

    print(f"{datetime.now().isoformat()} • Wrote {len(all_videos)} ranked videos to '{CSV_FILE}'")

if __name__ == "__main__":
    while True:
        build_and_save()
        time.sleep(REFRESH_MINUTES * 60)
