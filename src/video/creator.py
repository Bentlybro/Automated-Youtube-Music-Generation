from moviepy.editor import AudioFileClip, ImageClip

def create_video_with_image(audio_path, image_path, output_video_path):
    """
    Creates a video by combining an audio file with a static image
    """
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path).set_duration(audio_clip.duration).resize(height=720)
    video = image_clip.set_audio(audio_clip)
    video.write_videofile(output_video_path, fps=24, codec="libx264")
    print(f"Video saved as {output_video_path}")