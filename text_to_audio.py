import os
import logging
import time
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment

def read_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as text_file:
            return text_file.read()
    except UnicodeDecodeError as e:
        logging.error(f"UnicodeDecodeError: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        raise

def split_text_into_segments(input_text, max_chars=4000):
    segments = []
    current_segment = ""
    paragraphs = input_text.split("\n\n")  # Split by paragraphs
    for paragraph in paragraphs:
        if len(current_segment) + len(paragraph) + 2 <= max_chars:  # +2 for the double newline
            current_segment += paragraph + "\n\n"
        else:
            segments.append(current_segment.strip())
            current_segment = paragraph + "\n\n"
    if current_segment:
        segments.append(current_segment.strip())
    return segments

def transcribe_text_to_audio(client, text, output_path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="fable",
        input=text
    )
    with open(output_path, "wb") as audio_file:
        audio_file.write(response.read())
    logging.info(f"Segment saved to {output_path}")
    return len(text)  # Return the number of characters instead of tokens

def stitch_audio_segments(audio_paths, output_path):
    combined = AudioSegment.silent(duration=1000)  # Initial silence
    for path in audio_paths:
        segment = AudioSegment.from_mp3(path)
        combined += segment + AudioSegment.silent(duration=1000)  # Add silence between segments
    combined.export(output_path, format="mp3")
    logging.info(f"Final audio saved to {output_path}")

def text_to_audio(client, text_file_path):
    foldername = os.path.splitext(os.path.basename(text_file_path))[0]
    output_dir = Path(foldername)
    output_dir.mkdir(exist_ok=True)

    # Read the input text
    input_text = read_text_file(text_file_path)
    logging.info(f"Read input text from {text_file_path}")

    # Split the text into segments
    segments = split_text_into_segments(input_text)
    logging.info(f"Split input text into {len(segments)} segments")

    start_time = time.time()
    total_chars = 0

    # Transcribe each segment to an MP3 file
    audio_paths = []
    for i, segment in enumerate(segments):
        segment_path = output_dir / f"segment_{i+1}.mp3"
        chars_used = transcribe_text_to_audio(client, segment, segment_path)
        audio_paths.append(segment_path)
        total_chars += chars_used

    # Stitch all audio segments together
    final_output_path = output_dir / f"{foldername}.mp3"
    stitch_audio_segments(audio_paths, final_output_path)

    end_time = time.time()
    total_time = end_time - start_time
    total_cost = (total_chars / 1000) * 0.015

    logging.info(f"Process completed successfully")
    logging.info(f"Total character usage: {total_chars}")
    logging.info(f"Total cost: ${total_cost:.6f}")
    logging.info(f"Total time taken: {total_time:.2f} seconds")

    return final_output_path

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("API key not found in environment variables.")
        exit(1)
    client = OpenAI(api_key=api_key)
    text_file_path = "generated_story.txt" 
    text_to_audio(client, text_file_path)
