from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Initialize sentiment analysis pipeline once
sentiment_classifier = pipeline("sentiment-analysis")

def get_transcript(video_id):
    """
    Fetch YouTube transcript as a list of dictionaries with keys: 'text', 'start', 'duration'.
    Returns None if transcript not available.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript_list
    except Exception as e:
        print(f"Transcript not available for video {video_id}: {e}")
        return None

def get_clip_transcript(transcript_list, clip_start, clip_end):
    """
    Returns concatenated transcript text overlapping the clip time interval.
    """
    clip_texts = [
        entry['text'] for entry in transcript_list
        if entry['start'] >= clip_start and entry['start'] < clip_end
    ]
    return " ".join(clip_texts)

def is_highlight(text, min_score=0.85):
    """
    Use sentiment analysis to classify if text is a positive highlight.
    """
    if not text.strip():
        return False
    results = sentiment_classifier(text[:512])
    result = results[0]
    return result['label'] == 'POSITIVE' and result['score'] >= min_score

def filter_clips_by_transcript(clips, transcript_list):
    """
    Filter clips keeping only those whose transcript text is classified as positive highlight.
    """
    filtered = []
    for start, end in clips:
        snippet = get_clip_transcript(transcript_list, start, end)
        if is_highlight(snippet):
            filtered.append((start, end))
    return filtered
