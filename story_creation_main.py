import logging
from openai import OpenAI
import os
from generate_story import generate_story, generate_summary  # Import the generate_story and generate_summary functions
from text_to_audio import text_to_audio
from audio_to_video import audio_to_video
from pathlib import Path
from generate_image import generate_image_from_summary, save_image  # Import the image generation and save functions

def main():
    # Set up logging configuration for script message logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Retrieve the OpenAI API key from environment variables or set API key here
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("API key not found in environment variables.")
        return

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    # Define story topics and world details
    story_topics = ["The mysterious Island of Atlantis"] 

    #Define the world details in the format of "title": "World Description"
    world_details = {"The mysterious Island of Atlantis": "Atlantis is a legendary island first mentioned in Plato's dialogues Timaeus and Critias, written about 360 BC. According to Plato, Atlantis was a naval power lying beyond the Pillars of Hercules that conquered many parts of Western Europe and Africa 9,000 years before the time of Solon, or approximately 9600 BC. After a failed attempt to invade Athens, Atlantis sank into the ocean in a single day and night of misfortune . The island was said to be larger than Asia and Libya combined, and was the home of a technologically advanced civilization. The story of Atlantis has captivated the imagination of people for centuries, with many theories and speculations about its possible location and existence."}


    # Step 1: Generate the stories, specifying the audience of the story as appropriate ex/ "all", "children", "adults"
    logging.info("The story creation process has begun, please wait... this may take a few minutes")
    generated_story_paths, total_cost = generate_story(api_key, story_topics, world_details, intended_audience="all")

    # Display the total cost
    logging.info(f"Total cost for generating all stories: ${total_cost:.2f}")

    # Step 2: Generate and save images based on the story
    for story_path in generated_story_paths:
        with open(story_path, "r", encoding="utf-8") as file:
            story = file.read()

        # Generate summary of the story
        summary, _ = generate_summary(client, story)


        for i in range(1, 5):
            # Generate X amount of images to use from summary
            image_url, _ = generate_image_from_summary(client, summary)
            logging.info(f"Generated image URL: {image_url}")

            # Define image save path
            audio_filename = Path(story_path).stem
            output_dir = Path(story_path).parent
            image_save_path = output_dir / f"{audio_filename}_image_{i}.png"
            save_image(image_url, image_save_path)
            logging.info(f"Image saved to {image_save_path}")

        # Step 3: Convert each generated story text to audio
        final_audio_path = text_to_audio(client, story_path)
        logging.info(f"Story creation and conversion to audio completed successfully for {story_path}. Final audio file is located at: {final_audio_path}")
        
        # Step 4: Convert each generated audio to video
        audio_file = Path(final_audio_path)
        video_filename = audio_file.stem + '.mp4'
        output_video_path = output_dir / video_filename

        audio_to_video(str(audio_file), str(output_video_path))
        logging.info(f"Audio to video conversion completed successfully for {audio_file}. Final video file is located at: {output_video_path}")

if __name__ == "__main__":
    main()
