import os
import csv
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from datetime import datetime

def get_video_metadata(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()

    if response['items']:
        video_data = response['items'][0]
        snippet = video_data['snippet']
        statistics = video_data['statistics']
        
        video_metadata = {
            'video_id': video_id,
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'channel_name': snippet.get('channelTitle', ''),
            'upload_date': snippet.get('publishedAt', ''),
            'views': statistics.get('viewCount', ''),
            'likes': statistics.get('likeCount', ''),
            'dislikes': statistics.get('dislikeCount', ''),
            'tags': ', '.join(snippet.get('tags', []))
        }
        return video_metadata
    else:
        raise ValueError("Video not found")

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript_data = []
    
    for transcript in transcript_list:
        full_transcript = transcript.translate('en').fetch()
        for entry in full_transcript:
            transcript_data.append({
                'transcript_text': entry['text'],
                'timestamp': entry['start'],
                'language': transcript.language
            })
    return transcript_data

def save_to_csv(video_metadata, transcript_data, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Get the current UTC timestamp
    utc_timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # Define the output file path with UTC timestamp and video ID
    output_file = os.path.join(output_folder, f"{video_metadata['video_id']}_{utc_timestamp}_transcript.csv")
    #output_file = "./output/transcript.csv"

    
    # Define the headers for the CSV
    headers = ['video_id', 'title', 'description', 'channel_name', 'upload_date', 'views', 
               'likes', 'dislikes', 'tags', 'transcript_text', 'timestamp', 'language']
    
    # Write the metadata and transcript to the CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        
        for transcript_entry in transcript_data:
            row = {
                **video_metadata,
                **transcript_entry
            }
            writer.writerow(row)
    
    print(f"Transcript and metadata saved to {output_file}")

# Example usage
video_id = "7nB2v1Aq3cg"  # Remove the "&t" part if it's included in the URL
api_key = "AIzaSyDI1lTwrd8IuGCfuaeGqSVN1U51coaJkig"  # Replace with your YouTube Data API key
output_folder = "./output/raw"

# Fetch video metadata
video_metadata = get_video_metadata(video_id, api_key)

# Fetch transcript data
transcript_data = get_transcript(video_id)

# Save to CSV with UTC timestamp
save_to_csv(video_metadata, transcript_data, output_folder)