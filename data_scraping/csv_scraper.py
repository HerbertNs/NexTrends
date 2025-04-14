#APRIL 9TH 2025 4:57PM

import pandas as pd
import re
import os

#ou may need to adjust the file paths here.
datasheets_folder = "NexTrends\\data_scraping\\datasheets"
output_folder = "NexTrends\\data_scraping\\compiled_links"

youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+')

for file in os.listdir(datasheets_folder):
    if file.endswith('.csv') or file.endswith('.xlsx'):
        file_path = os.path.join(datasheets_folder,file)

        try:
            if file.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
        except:
            print("error encountered")
            continue
        youtube_urls = []

        for col in df.columns:
            urls = df[col].astype(str)

            matched = urls[urls.str.contains(youtube_pattern, na=False)]
            youtube_urls.extend(matched.tolist())
            
        if youtube_urls:
            txt_filename = os.path.splitext(file)[0] + "_links.txt"
            txt_path = os.path.join(output_folder,txt_filename)

            with open(txt_path, 'w') as f:
                for url in youtube_urls:
                    f.write(f"{url}\n")
                    print(f"saved {len(youtube_urls)} from {file} to {txt_filename}")
                else:
                    print(f"skipped: {file}")
