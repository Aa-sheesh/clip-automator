# Generate a README for this

Here is a comprehensive README for your YouTube Live Analyzer and Automatic Clip Creator project:

***

# YouTube Live Analyzer \& Automatic Clip Creator

This project is a Flask-based backend service that analyzes completed live streams on YouTube channels, detects highlight clips based on audio spikes and transcript sentiment, and automatically extracts highlight video clips.

***

## Features

- Fetch latest completed live stream video from a YouTube channel handle.
- Download video and extract audio.
- Detect audio spikes using librosa to identify potential highlight segments.
- Retrieve YouTube auto-generated or manual English transcripts using `youtube-transcript-api`.
- Analyze transcript snippets with Hugging Face sentiment analysis to filter for positive highlights.
- Create and save video clips for detected highlight segments.
- Exposes RESTful API endpoints for each step for modular testing and automation.

***

## Tech Stack

- Python 3.12+
- Flask Web Framework
- YouTube Data API v3 (Google API Python Client)
- youtube-transcript-api (for captions)
- moviepy (video processing)
- librosa (audio analysis)
- transformers \& torch (sentiment analysis NLP)
- python-dotenv (environment variable management)

***

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-repo/youtube-live-analyzer.git
cd youtube-live-analyzer
```


### 2. Create Virtual Environment and Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

_`requirements.txt` should include:_

```
flask
google-api-python-client
youtube-transcript-api
moviepy
librosa
transformers
torch
python-dotenv
numpy
```


### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```
YOUTUBE_API_KEY=YOUR_YOUTUBE_DATA_API_KEY
```

Make sure `.env` is in `.gitignore` to protect your keys.

### 4. Run the Flask App

```bash
python app.py
```

The API will run at `http://127.0.0.1:5000`

***

## Available API Routes

- `GET /download-video/<handle>`
Download the latest completed live stream video by YouTube handle.
- `POST /extract-audio`
Extract audio from a given video path (send JSON with `videoPath`).
- `POST /detect-spikes`
Detect audio spikes in a given audio file (send JSON with `audioPath`).
- `POST /create-clips`
Create clips from given video path and clip time intervals (send JSON with `videoPath` and `clipTimes`).
- `GET /create-smart-clips/<handle>`
Full pipeline: downloads video, extracts audio, detects spikes, fetches transcript, filters highlights by sentiment, and creates highlight clips automatically.

***

## Usage Example

1. Download latest video:
```
GET http://127.0.0.1:5000/download-video/@channelHandle
```

2. Extract audio:
```
POST http://127.0.0.1:5000/extract-audio
Content-Type: application/json
{
  "videoPath": "videos/YOUR_VIDEO_ID.mp4"
}
```

3. Detect spikes:
```
POST http://127.0.0.1:5000/detect-spikes
Content-Type: application/json
{
  "audioPath": "audio/YOUR_VIDEO_ID.wav"
}
```

4. Create clips:
```
POST http://127.0.0.1:5000/create-clips
Content-Type: application/json
{
  "videoPath": "videos/YOUR_VIDEO_ID.mp4",
  "clipTimes": [[start1, end1], [start2, end2], ...]
}
```

5. Create smart clips in one call:
```
GET http://127.0.0.1:5000/create-smart-clips/@channelHandle
```


***

## Notes

- Make sure to monitor your YouTube Data API v3 quota to avoid quotaExceeded errors.
- The sentiment analysis model is a general classifier and can be fine-tuned or replaced for domain-specific needs.
- Clip window sizes and audio spike detection parameters can be adjusted in `audio_spike_detector.py`.
- Video and clips are saved locally in `videos/`, `audio/`, and `clips/` directories respectively.

***

## Contribution and Support

Contributions and issues are welcome! Please create issues and pull requests on the GitHub repo.

For support, contact [your-email@example.com].

***

## License

MIT License
