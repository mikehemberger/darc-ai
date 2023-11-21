import pandas as pd
import subprocess
import time
import os
import argparse

# IMPLEMENT FILE SKIPPING IF THE FILE IS ALREADY PRESENT!!!


def darc_download_shows(file_path, search_show_name):
    # Step 1: Read DataFrame
    df = pd.read_csv(file_path)
    
    # Step 2: Search for the show name
    search_result = df["series_title"].str.contains(search_show_name, case=False, na=False)
#    search_result = df["title"].str.contains(search_show_name, case=False, na=False)
    
    # Step 3: Exception Handling
    if not any(search_result):
        raise Exception(f"No shows found with the name: {search_show_name}")
    
    # Step 4: Logging
    num_files = sum(search_result)
    print(f"{num_files} files will be downloaded.")
    
    # Estimate time (assume each download takes about 2 minutes)
    estimated_time = num_files * 2
    print(f"Estimated time for the entire process is around {estimated_time} minutes.")
    
    # Create a new folder to store the downloaded files
    folder_name = search_show_name.lower().replace(" ", "-")

    # Step 5: Download files
    download_links = df.loc[search_result, "links"]
    
    for idx, link in enumerate(download_links):
        print(f"Downloading file {idx + 1} of {num_files}...")
        
        # Use wget to download the file into the specified folder
        subprocess.run(['wget', '-P', "./data/videos/" + folder_name, link])
        
        # Add some sleep time if needed to avoid overwhelming the server (optional)
        time.sleep(240)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download shows based on a search term.')
    parser.add_argument('--file_path', type=str, required=True, help='Path to the CSV file containing the show data.')
    parser.add_argument('--search_show_name', type=str, required=True, help='Name of the show to search for.')
    
    args = parser.parse_args()
    darc_download_shows(args.file_path, args.search_show_name)

# python3 darc_download_shows.py --file_path "./data/metadata/darc-iarchive-wldoc-with-vid-durations-mp4.csv" --search_show_name "Life On Earth"
# !python3 darc_download_shows.py --file_path "./data/metadata/darc-iarchive-wldoc-with-vid-durations-mp4.csv" --search_show_name "Life On Earth"
