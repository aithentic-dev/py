


import os
import csv
from openai import OpenAI
from datetime import datetime

api_key = ''  # Add your API key here
client = OpenAI(api_key=api_key)

# Function to clean the transcript using OpenAI (gpt-4)
def transcript_cleansing(transcription):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that corrects spelling and grammar mistakes in the text without changing its meaning. Ensure the transcript remains coherent and retains the original context and meaning of the conversation."
            },
            {
                "role": "user",
                "content": f"Clean the following text:\n\n{transcription}"
            }
        ]
    )
    return response.choices[0].message.content

# Function to find the most recent transcript file for the given video ID
def find_transcript_file(video_id, raw_folder):
    # List all files in the raw folder
    files = os.listdir(raw_folder)
    
    # Filter files that match the video ID and the format
    matching_files = [f for f in files if f.startswith(video_id) and f.endswith('_transcript.csv')]
    
    if not matching_files:
        return None
    
    # Sort files by creation time (assuming the timestamp is in the filename)
    matching_files.sort(reverse=True)
    
    # Return the most recent file
    return os.path.join(raw_folder, matching_files[0])

# Function to process the transcript from an existing CSV file
def process_transcript_from_csv(video_id, raw_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Find the most recent transcript file for the given video ID
    raw_file_path = find_transcript_file(video_id, raw_folder)
    
    if raw_file_path is None:
        print(f"No raw transcript file found for video ID: {video_id}")
        return
    
    # Read the raw transcript from the CSV file
    with open(raw_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        transcript_text = " ".join([row['transcript_text'] for row in reader])
    
    print("Original Transcript:\n", transcript_text)
    
    # Clean the transcript
    cleaned_transcript = transcript_cleansing(transcript_text)
    print("\nCleaned Transcript:\n", cleaned_transcript)

    # Get the current UTC timestamp
    utc_timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # Define the output file path with UTC timestamp and video ID
    output_file = os.path.join(output_folder, f"{video_id}_{utc_timestamp}_cleaned_transcript.txt")
    
    # Save the cleaned transcript to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Original Transcript:\n")
        file.write(transcript_text + "\n\n")
        file.write("Cleaned Transcript:\n")
        file.write(cleaned_transcript)
    
    print(f"\nCleaned transcript saved to {output_file}")

# Example usage
video_id = "7nB2v1Aq3cg"
raw_folder = "./output/raw"  # Folder containing the raw transcripts
output_folder = "./output/openai4-mini"  # Folder where cleaned transcripts will be saved
process_transcript_from_csv(video_id, raw_folder, output_folder)
