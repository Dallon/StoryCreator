import os
import logging
from openai import OpenAI

def setup_openai_client(api_key: str):
    return OpenAI(api_key=api_key)

def generate_story_segment(client, prompt: str, max_tokens: int = 4000):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4",
            max_tokens=max_tokens
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        return ""

def save_story_to_file(story: str, filename: str):
    with open(filename, "w") as text_file:
        text_file.write(story)
    logging.info(f"Story generated and saved to {filename}")

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("API key not found in environment variables.")
        return

    client = setup_openai_client(api_key)

    story_topic = "The end of days - an Apocalyptic story"
    max_tokens = 4000

    # Initial prompt to generate the story outline
    outline_prompt = f"""
    You are an expert storyteller. Generate a detailed and captivating outline for a story titled '{story_topic}'.
    The story should have clear chapters with titles and summaries. Ensure the story flows logically and consistently from chapter to chapter.
    """

    # Generate the story outline
    outline = generate_story_segment(client, outline_prompt, max_tokens)
    logging.debug("Outline generated.")

    if not outline.strip():
        logging.error("Outline generation failed, no content returned.")
        return

    # Initialize the story with the intro
    current_story = f"Welcome to StoryStream, or welcome back for our regulars. Today's story is called '{story_topic}'\n\n"

    # Append the generated outline to the story
    current_story += outline + "\n"

    # Generate the actual story based on the outline
    story_prompt = f"""
    Using the following outline, continue writing the story titled '{story_topic}'. Ensure that the story is consistent, engaging, and follows the outlined chapters. Write the story in a detailed and immersive manner.

    Outline:
    {outline}
    """

    # Generate the full story
    story_content = generate_story_segment(client, story_prompt, max_tokens)
    
    if not story_content.strip():
        logging.error("Story generation failed, no content returned.")
        return

    current_story += story_content

    # Finalize the story with the outro
    current_story += "\n\nThat is the end of our story today, thank you so much for listening. Please, let me know your thoughts, and be well my friends."

    # Save the final story to a file
    save_story_to_file(current_story, "generated_story.txt")

if __name__ == "__main__":
    main()
