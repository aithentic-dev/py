import os
import csv
from openai import OpenAI

api_key = ''  # Replace with your actual API key
client = OpenAI(api_key=api_key)

def find_transcript_file(video_id, cleaned_folder):
    # List all files in the cleaned folder
    files = os.listdir(cleaned_folder)
    
    # Filter files that match the video ID at the beginning of the filename
    matching_files = [f for f in files if f.startswith(video_id) and f.endswith('_cleaned_transcript.txt')]
    
    if not matching_files:
        return None
    
    # Sort files by creation time (assuming the timestamp is in the filename)
    matching_files.sort(reverse=True)
    
    # Return the most recent file
    return os.path.join(cleaned_folder, matching_files[0])

def read_cleansed_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript = file.read()
    return transcript

def generate_comments(transcript, num_comments=10):
    comments = []
    
    for _ in range(num_comments):
        response = client.chat.completions.create(
            model="gpt-4",
            temperature=0.8,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a person from South India who supports the YSRCP party but is not a political activist. "
                        "Generate a short, friendly comment in general South Indian English. "
                        "Each comment should start differently and use a unique expression or style. "
                        "Feel free to incorporate relevant context from the transcript or known details, "
                        "but ensure that each comment sounds like it comes from a genuine, supportive, and everyday person."
                    )
                },
                {
                    "role": "user",
                    "content": f"Based on the following transcript, generate a brief supportive comment for the YSRCP party in general South Indian English:\n\n{transcript}"
                }
            ]
        )
        comment = response.choices[0].message.content
        comments.append(comment.strip())

    return comments

def save_comments_to_file(comments, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for i, comment in enumerate(comments, 1):
            file.write(f"Comment {i}:\n{comment}\n\n")

# Example usage
video_id = "7nB2v1Aq3cg"
cleaned_folder = "./output/openai4"  # Folder containing the cleaned transcripts
output_comments_folder = f"./output/comments/{video_id}"  # Subfolder named after the video ID
output_comments_file = os.path.join(output_comments_folder, f"{video_id}_comments.txt")

# Ensure the output directory exists
os.makedirs(output_comments_folder, exist_ok=True)

# Find the appropriate cleaned transcript file
transcript_file = find_transcript_file(video_id, cleaned_folder)

if transcript_file is None:
    print(f"No cleaned transcript file found for video ID: {video_id}")
else:
    # Read the cleansed transcript
    transcript = read_cleansed_transcript(transcript_file)

    # Generate 10 supportive comments
    comments = generate_comments(transcript, num_comments=10)

    # Save the comments to a file
    save_comments_to_file(comments, output_comments_file)

    print(f"Comments saved to {output_comments_file}")
