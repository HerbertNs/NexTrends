import googleapiclient.discovery
import csv
import sys
import os
import time
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv(API_KEY)

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

categories = {
    1: "Film_and_Animation",
    2: "Autos_and_Vehicles",
    10: "Music",
    15: "Pets_and_Animals",
    17: "Sports",
    18: "Short_Movies",
    19: "Travel_and_Events",
    20: "Gaming",
    21: "Videoblogging",
    22: "People_and_Blogs",
    23: "Comedy",
    24: "Entertainment",
    25: "News_and_Politics",
    26: "How_to_and_Style",
    27: "Education",
    28: "Science_and_Technology",
    29: "Nonprofits_and_Activism",
    30: "Movies",
    31: "Anime_and_Animation",
    32: "Action_and_Adventure",
    33: "Classics",
    34: "Comedy_Movies",
    35: "Documentary",
    36: "Drama",
    37: "Family",
    38: "Foreign",
    39: "Horror",
    40: "Sci_Fi_and_Fantasy",
    41: "Thriller",
    42: "Shorts",
    43: "Shows",
    44: "Trailers"
}

def get_videos_by_category(category_id, max_results=10):
    request = youtube.search().list(
        part="snippet",
        type="video",
        maxResults=max_results,
        videoCategoryId=category_id,
        order="date",
        publishedAfter="2025-01-01T00:00:00Z"
    )
    
    try:
        response = request.execute()
        request = youtube.videoCategories().list(part="snippet", regionCode="US")
        response = request.execute()
        print(response)
    except:
        print("\t\nNO QUOTA LEFT!")
        sys.exit()

    videos = []
    video_ids = []

    for video in response.get("items", []):
        video_id = video["id"]["videoId"]
        title = video["snippet"]["title"]
        channel = video["snippet"]["channelTitle"]
        published_date = video["snippet"]["publishedAt"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        videos.append([video_id, title, channel, published_date, video_url])
        video_ids.append(video_id)

    return videos, video_ids

def get_video_details(video_ids):
    if not video_ids:
        return {}

    request = youtube.videos().list(
        part="statistics",
        id=",".join(video_ids)
    )
    
    try:
        response = request.execute()
    except:
        print("\t\nNO QUOTA LEFT!")
        sys.exit()

    views_dict = {}
    for item in response.get("items", []):
        video_id = item["id"]
        views = item["statistics"].get("viewCount", "0")
        views_dict[video_id] = int(views)

    return views_dict

def save_to_updated_csv(category_name, videos, views_dict):
    updated_filename = f"Updated_{category_name}.csv"
    previous_filename = f"Previous_{category_name}.csv"

    if os.path.exists(updated_filename):
        if os.path.exists(previous_filename):
            os.remove(previous_filename)  
        os.rename(updated_filename, previous_filename)

   
    with open(updated_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Channel", "Published Date", "Video URL", "Views"])
        
        for video in videos:
            video_id, title, channel, published_date, video_url = video
            views = views_dict.get(video_id, 0)
            writer.writerow([title, channel, published_date, video_url, views])

    print(f"Saved {len(videos)} videos to {updated_filename}")
    

for category_id, category_name in categories.items():
    videos, video_ids = get_videos_by_category(category_id)
    views_dict = get_video_details(video_ids)
    save_to_updated_csv(category_name, videos, views_dict)

print(" Scrape cycle completed!")



