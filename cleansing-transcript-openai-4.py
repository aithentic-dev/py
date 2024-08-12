import os
from openai import OpenAI
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi

api_key = ''  # Add your API key here
client = OpenAI(api_key=api_key)

# Function to clean the transcript using OpenAI (gpt-4)
def transcript_cleansing(transcription):
    response = client.chat.completions.create(
        model="gpt-4",
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

# Function to extract, clean, and save the transcript
def process_youtube_transcript(video_id, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Fetch and translate the transcript
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    for transcript in transcript_list:
        transcript_fulltxt = transcript.translate('en').fetch()
        transcript_text = " ".join([item['text'] for item in transcript_fulltxt])
        print("Original Transcript:\n", transcript_text)

        # Clean the transcript
        cleaned_transcript = transcript_cleansing(transcript_text)
        print("\nCleaned Transcript:\n", cleaned_transcript)

        # Get the current UTC timestamp
        utc_timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

        # Define the output file path with UTC timestamp and video ID
        output_file = os.path.join(output_folder, f"{video_id}_{utc_timestamp}_cleaned_transcript.txt")

        # Save the cleaned transcript to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Original Transcript:\n")
            file.write(transcript_text + "\n\n")
            file.write("Cleaned Transcript:\n")
            file.write(cleaned_transcript)
        
        print(f"\nCleaned transcript saved to {output_file}")

# Example usage
video_id = "7nB2v1Aq3cg"
output_folder = "./output/openai4"  # Replace with your desired output folder path
process_youtube_transcript(video_id, output_folder)
