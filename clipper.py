from moviepy import VideoFileClip

def create_clip(input_path, start_sec, end_sec, output_path):
    with VideoFileClip(input_path) as video:
        clip = video.subclipped(start_sec, end_sec)
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

def extract_audio(video_path, audio_output_path):
    with VideoFileClip(video_path) as video:
        audio = video.audio
        audio.write_audiofile(audio_output_path)
