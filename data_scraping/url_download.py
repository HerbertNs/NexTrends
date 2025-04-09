from pytube import YouTube
import requests
import os

def download_thumbnail(url, output_folder):
    try:
        yt = YouTube(url)
        video_id = yt.video_id
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            os.makedirs(output_folder, exist_ok=True)
            filename = os.path.join(output_folder, f"{video_id}_thumbnail.jpg")
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Successfully downloaded thumbnail as {filename}")
            return filename
        else:
            print(f"Error: Could not download thumbnail (HTTP {response.status_code})")
            return None
            
    except Exception as e:
        print(f"Error processing URL: {str(e)}")
        return None

def process_compiled_links():
    compiled_links_folder = "NexTrends\\data_scraping\\compiled_links"
    thumbnails_folder = "NexTrends\\data_scraping\\compiled_thumbnails"
    
    for filename in os.listdir(compiled_links_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(compiled_links_folder, filename)
            with open(file_path, 'r') as f:
                urls = f.read().splitlines()
                
            print(f"\nProcessing {len(urls)} URLs from {filename}")
            for url in urls:
                if url.strip():
                    download_thumbnail(url.strip(), thumbnails_folder)

if __name__ == "__main__":
    process_compiled_links()