from openai import OpenAI
api_key = ''#add api key here

client = OpenAI(api_key=api_key)
from youtube_transcript_api import YouTubeTranscriptApi

# Your OpenAI API key

# Function to clean the transcript using OpenAI
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

# Function to extract and clean the transcript
def process_youtube_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    for transcript in transcript_list:
        transcript_fulltxt = transcript.translate('en').fetch()
        transcript_text = " ".join([item['text'] for item in transcript_fulltxt])
        print(transcript_text)
        cleaned_transcript = transcript_cleansing(transcript_text)
        print(cleaned_transcript)

# Example usage
video_id = "7nB2v1Aq3cg&t"
process_youtube_transcript(video_id)