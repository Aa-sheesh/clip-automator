from yt_dlp import YoutubeDL
import os

def download_video(video_id, output_dir='videos/'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': os.path.join(output_dir, f'{video_id}.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return os.path.join(output_dir, f'{video_id}.mp4')
