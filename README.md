# Story Generation, Audio, and Video Conversion

This project automates the generation of stories, their conversion to audio files, and the creation of related images and videos. The entire process is managed by a series of scripts that interact with OpenAI's API to create engaging content.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Main Script](#main-script)
  - [Supporting Scripts](#supporting-scripts)
    - [generate_story.py](#generate_storypy)
    - [text_to_audio.py](#text_to_audiopy)
    - [audio_to_video.py](#audio_to_videopy)
    - [generate_image.py](#generate_imagepy)
- [Environment Variables](#environment-variables)
- [Example Usage](#example-usage)
- [Logging](#logging)
- [License](#license)

## Overview

This program automates the process of generating stories, converting them to audio, creating related images, and finally producing videos with audio. The core functionalities are:
- Generating stories based on given topics and world details.
- Generating summaries for the stories.
- Creating images based on the story summaries.
- Converting the stories to audio files.
- Converting the audio files to videos.

## Requirements

Ensure you have the following installed and configured:
- Python 3.7 or higher
- `openai` package
- `moviepy` package
- `pydub` package
- `Pillow` package
- `requests` package
- An OpenAI API key set as an environment variable `OPENAI_API_KEY`

## Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required packages:
    ```bash
    pip install openai moviepy pydub Pillow requests
    ```

## Usage

### Main Script

The main script (`main.py`) coordinates the entire process. It is structured as follows:
- **Logging Configuration**: Sets up logging to track the process.
- **API Key Setup**: Retrieves the OpenAI API key from environment variables.
- **Story Generation**: Uses the `generate_story` function to create stories based on given topics and world details.
- **Image Generation**: Generates images based on the story summaries.
- **Audio Conversion**: Converts the story text to audio using `text_to_audio`.
- **Video Conversion**: Converts the generated audio files to video files using `audio_to_video`.

To run the main script, execute:
```
python main.py
```

### Supporting Scripts
generate_story.py Handles the story generation process, including segment generation and saving the final story to a file.

Functions:

generate_story: Generates the complete story.
generate_summary: Creates a summary of the generated story.
generate_intro: Generates an introduction for the story.
save_story_to_file: Saves the generated story to a text file.
setup_openai_client: Initializes the OpenAI client.
text_to_audio.py
Manages the conversion of text to audio files.

Functions:

text_to_audio: Converts the entire story text to an audio file.
transcribe_text_to_audio: Transcribes text segments to audio files.
stitch_audio_segments: Combines audio segments into a final audio file.
read_text_file: Reads the story text from a file.
split_text_into_segments: Splits the text into manageable segments for audio conversion.
audio_to_video.py
Converts audio files to video files with a plain black background.

Functions:

audio_to_video: Creates a video file from an audio file.
generate_image.py
Generates images based on story summaries using OpenAI's DALL-E model.

Functions:

generate_image_from_summary: Generates an image URL from the story summary.
save_image: Saves the generated image to a file.
Environment Variables
OPENAI_API_KEY: Your OpenAI API key for accessing OpenAI services.

### Example Usage
Define your story topics and world details in the main script:

```python
story_topics = ["The mysterious Island of Atlantis"]
world_details = {"The mysterious Island of Atlantis": "Atlantis is a legendary island..."}
```
Run the main script:
```
python main.py
```
The script will generate stories, create images, convert the text to audio, and finally produce video files with the audio.

Logging
The program uses Python's built-in logging module to log information, errors, and debugging messages. Check the console output for details about the process.

License
This project is licensed under the MIT License
