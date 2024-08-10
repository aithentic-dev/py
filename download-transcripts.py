video_id = "7nB2v1Aq3cg&t"
# YouTubeTranscriptApi.get_transcript(video_id)

from youtube_transcript_api import YouTubeTranscriptApi
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
for transcript in transcript_list:
    transcript_fulltxt = transcript.translate('en').fetch()

print(transcript_fulltxt)