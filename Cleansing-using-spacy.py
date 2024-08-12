import os
import csv
import spacy
from spellchecker import SpellChecker
from datetime import datetime

# Load SpaCy's English language model
nlp = spacy.load('en_core_web_sm')
spell = SpellChecker()

# Function to clean the transcript using SpaCy
def transcript_cleansing_spacy(transcription):
    # Process the text with SpaCy
    doc = nlp(transcription)
    
    cleaned_tokens = []
    
    for token in doc:
        # Correct spelling errors
        if token.text.lower() in spell:
            cleaned_tokens.append(token.text)
        else:
            # Suggest the correct spelling or fallback to the original token text
            corrected_text = spell.correction(token.text.lower())
            if corrected_text is None:
                cleaned_tokens.append(token.text)  # Use original token if correction is None
            else:
                cleaned_tokens.append(corrected_text)
    
    # Join the cleaned tokens into a single string
    cleaned_transcript = " ".join(cleaned_tokens)
    
    # Capitalize the first letter of each sentence
    cleaned_transcript = cleaned_transcript.capitalize()
    
    return cleaned_transcript

# Function to find the most recent transcript file for the given video ID
def find_transcript_file(video_id, raw_folder):
    # List all files in the raw folder
    files = os.listdir(raw_folder)
    
    # Filter files that match the video ID
    matching_files = [f for f in files if f.startswith(video_id) and f.endswith('_transcript.csv')]
    
    if not matching_files:
        return None
    
    # Sort files by creation time (assuming timestamp is in the filename)
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
    cleaned_transcript = transcript_cleansing_spacy(transcript_text)
    print("\nCleaned Transcript:\n", cleaned_transcript)

    # Get the current UTC timestamp
    utc_timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # Define the output file path with UTC timestamp and video ID
    output_file = os.path.join(output_folder, f"{video_id}_{utc_timestamp}_cleaned_transcript.csv")
    
    # Save the cleaned transcript to a new CSV file with space between original and cleaned transcripts
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Original Transcript", "Cleaned Transcript"])
        writer.writerow([transcript_text, ""])  # Write original transcript and empty column for spacing
        writer.writerow(["", ""])  # Add an empty row for spacing
        writer.writerow(["", cleaned_transcript])  # Write cleaned transcript in the second column
    
    print(f"\nCleaned transcript saved to {output_file}")

# Example usage
video_id = "7nB2v1Aq3cg"
raw_folder = "./output/raw"  # Folder containing the raw transcripts
output_folder = "./output/spacy"  # Folder where cleaned transcripts will be saved
process_transcript_from_csv(video_id, raw_folder, output_folder)
