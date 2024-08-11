import os
import csv

def fetch_and_display_transcript(video_id, search_folder):
    # Construct the search pattern
    search_pattern = f"{video_id}_*.csv"
    
    # List all files in the directory that match the pattern
    matching_files = [f for f in os.listdir(search_folder) if f.startswith(video_id) and f.endswith('.csv')]
    
    # Check if any matching files were found
    if not matching_files:
        print(f"No file found for video ID: {video_id}")
        return
    
    # Assuming the latest file is needed if multiple files are found (sorted by creation time)
    matching_files.sort(key=lambda x: os.path.getctime(os.path.join(search_folder, x)), reverse=True)
    file_to_read = os.path.join(search_folder, matching_files[0])
    
    print(f"Reading from file: {file_to_read}\n")
    
    # Open the CSV file and read the transcript_text values
    with open(file_to_read, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            return(row['transcript_text'])

# Example usage
video_id = "7nB2v1Aq3cg"
search_folder = "./output/raw"  # Adjust the folder path as needed

transcripttext = fetch_and_display_transcript(video_id, search_folder)

print (transcripttext)