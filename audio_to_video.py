import moviepy.editor as mp
import os
import logging
from pathlib import Path

def audio_to_video(audio_file, output_file, duration=None):
    try:
        # Ensure the paths are strings
        audio_file = str(audio_file)
        output_file = str(output_file)
        
        # Load audio file
        audio = mp.AudioFileClip(audio_file)
        
        # Set duration if not provided
        if duration is None:
            duration = audio.duration

        # Create a plain black background
        image = mp.ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration)

        # Set audio to the video clip
        video = image.set_audio(audio)

        # Export the video
        video.write_videofile(output_file, fps=24)
        logging.info(f"Video saved to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred while converting audio to video: {e}")
