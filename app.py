import os
from flask import Flask, jsonify
from googleapiclient.discovery import build
from video_downloader import download_video
from clipper import create_clip, extract_audio
from audio_spike_detector import detect_audio_spikes
from transcript_utils import get_transcript, filter_clips_by_transcript

from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


app = Flask(__name__)
YOUTUBE_API_KEY = 'AIzaSyDIyb9BsEqJpTG81Bii23-ClG_onRVw48s'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def get_channel_id_from_handle(handle):
    handle = handle.lstrip('@')
    response = youtube.search().list(
        part='snippet',
        q=handle,
        type='channel',
        maxResults=1
    ).execute()
    if response['items']:
        return response['items'][0]['snippet']['channelId']
    return None

@app.route('/')
def home():
    return jsonify({"message": "Youtube Live Analyzer API is running!"})

@app.route('/download-video/<handle>')
def download_latest_video(handle):
    channel_id = get_channel_id_from_handle(handle)
    if not channel_id:
        return jsonify({"message": f"Channel handle '{handle}' not found"}), 404
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        eventType='completed',
        type='video',
        maxResults=1,
        order='date'
    )
    response = request.execute()
    if not response['items']:
        return jsonify({"message": "No completed live streams found"}), 404
    video_id = response['items'][0]['id']['videoId']
    video_path = download_video(video_id)
    return jsonify({
        "message": "Video downloaded successfully",
        "videoId": video_id,
        "videoPath": video_path
    })

@app.route('/extract-audio', methods=['POST'])
def extract_audio_route():
    data = request.json
    video_path = data.get('videoPath')
    if not video_path or not os.path.exists(video_path):
        return jsonify({"message": "Invalid or missing videoPath"}), 400
    audio_dir = 'audio'
    os.makedirs(audio_dir, exist_ok=True)
    audio_path = os.path.join(audio_dir, os.path.basename(video_path).replace('.mp4', '.wav'))
    extract_audio(video_path, audio_path)
    return jsonify({"message": "Audio extracted", "audioPath": audio_path})

@app.route('/detect-spikes', methods=['POST'])
def detect_spikes_route():
    data = request.json
    audio_path = data.get('audioPath')
    if not audio_path or not os.path.exists(audio_path):
        return jsonify({"message": "Invalid or missing audioPath"}), 400
    clip_times = detect_audio_spikes(audio_path)
    if not clip_times:
        return jsonify({"message": "No audio spikes detected"}), 404
    return jsonify({"message": "Audio spikes detected", "clipTimes": clip_times})

@app.route('/create-clips', methods=['POST'])
def create_clips_route():
    data = request.json
    video_path = data.get('videoPath')
    clip_times = data.get('clipTimes')
    if not video_path or not os.path.exists(video_path):
        return jsonify({"message": "Invalid or missing videoPath"}), 400
    if not clip_times or not isinstance(clip_times, list):
        return jsonify({"message": "Invalid or missing clipTimes"}), 400

    clips_dir = 'clips'
    os.makedirs(clips_dir, exist_ok=True)
    created_clips_info = []
    for i, clip_time in enumerate(clip_times):
        try:
            start, end = clip_time
            clip_output_path = os.path.join(clips_dir, f"clip_{i}.mp4")
            create_clip(video_path, start, end, clip_output_path)
            created_clips_info.append({
                "clipIndex": i,
                "start": start,
                "end": end,
                "clipPath": clip_output_path
            })
        except Exception as e:
            return jsonify({"message": f"Error creating clip {i}: {str(e)}"}), 500

    return jsonify({"message": "Clips created successfully", "clips": created_clips_info})

@app.route('/create-smart-clips/<handle>')
def create_smart_clips(handle):
    # Get channel ID
    handle_clean = handle.lstrip('@')
    response = youtube.search().list(
        part='snippet',
        q=handle_clean,
        type='channel',
        maxResults=1
    ).execute()
    if not response['items']:
        return jsonify({"message": "Channel not found"}), 404
    channel_id = response['items'][0]['snippet']['channelId']

    # Get latest completed live stream video
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        eventType='completed',
        type='video',
        maxResults=1,
        order='date'
    )
    response = request.execute()
    if not response['items']:
        return jsonify({"message": "No completed live streams found"}), 404

    video_id = response['items'][0]['id']['videoId']
    video_path = download_video(video_id)

    # Extract audio
    os.makedirs('audio', exist_ok=True)
    audio_path = os.path.join('audio', f'{video_id}.wav')
    extract_audio(video_path, audio_path)

    # Get transcript
    transcript_list = get_transcript(video_id)
    if not transcript_list:
        return jsonify({"message": "Transcript not available for video"}), 404

    # Detect audio spikes
    clips = detect_audio_spikes(audio_path)
    if not clips:
        return jsonify({"message": "No audio spikes detected"}), 404

    # Filter clips by transcript sentiment analysis
    filtered_clips = filter_clips_by_transcript(clips, transcript_list)
    if not filtered_clips:
        return jsonify({"message": "No highlight clips detected after filtering"}), 404

    # Create clips
    os.makedirs('clips', exist_ok=True)
    created_clips_info = []
    for i, (start, end) in enumerate(filtered_clips):
        clip_path = os.path.join('clips', f'{video_id}_clip_{i}.mp4')
        create_clip(video_path, start, end, clip_path)
        created_clips_info.append({
            "clipIndex": i,
            "start": start,
            "end": end,
            "clipPath": clip_path
        })

    return jsonify({
        "message": "Smart clips created",
        "clips": created_clips_info
    })


if __name__ == '__main__':
    app.run(debug=True)
