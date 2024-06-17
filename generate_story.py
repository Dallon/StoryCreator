import os
import logging
import time
import re
from openai import OpenAI

def setup_openai_client(api_key: str):
    return OpenAI(api_key=api_key)

def generate_story_segment(client, prompt: str, max_tokens: int = 4095):
    try:
        start_time = time.time()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
            max_tokens=max_tokens
        )
        end_time = time.time()
        time_taken = end_time - start_time
        tokens_used = chat_completion.usage.total_tokens
        return chat_completion.choices[0].message.content, tokens_used, time_taken
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        return "", 0, 0

def generate_intro(client, story_topic: str, world_details: str, max_tokens: int = 500):
    try:
        intro_prompt = f"""
        You are an expert storyteller. Provide a brief, engaging introduction to the story titled '{story_topic}'.
        This introduction should be from the presenter's perspective, sharing their thoughts on the story and what the audience can expect without giving away major plot points.
        The intro should be intriguing and set the tone for the story, no more than 3 or 4 sentences, making the listeners excited to hear more. Don't use "Ladies and Gentelemen" use "all", and avoid cut off sentences.

        Initial World Details: {world_details}
        """
        intro_content, tokens_used, time_taken = generate_story_segment(client, intro_prompt, max_tokens)
        if not intro_content.strip():
            logging.error("Intro generation failed, no content returned.")
            return "", 0, 0
        return intro_content, tokens_used, time_taken
    except Exception as e:
        logging.error(f"Error during intro generation: {e}")
        return "", 0, 0

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def save_story_to_file(story: str, foldername: str, filename: str):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
        logging.info(f"Created directory: {foldername}")

    sanitized_filename = sanitize_filename(filename)
    
    filepath = os.path.join(foldername, sanitized_filename)
    with open(filepath, "w", encoding="utf-8") as text_file:
        text_file.write(story)
    logging.info(f"Story generated and saved to {filepath}")
    return filepath

def generate_story(api_key, story_topics, world_details, max_tokens_per_call=4095, total_token_limit=20000):
    client = setup_openai_client(api_key)

    token_cost_per_million = 15 / 1_000_000
    end_markers = ["<END OF STORY>", "The End"]

    generated_story_paths = []
    total_cost = 0

    for story_topic in story_topics:
        current_story = ""
        total_tokens_used = 0
        total_time_taken = 0
        world_detail = world_details.get(story_topic, "")

        while total_tokens_used < total_token_limit:
            remaining_tokens = total_token_limit - total_tokens_used
            is_final_segment = remaining_tokens <= max_tokens_per_call
            story_completion_percentage = (total_tokens_used / total_token_limit) * 100

            prompt = f"""
            You are a master storyteller with a gift for captivating narratives. Ensure the story builds elements of mystery, adventure, has a surprising twist, and is engaging for a general audience. Your style resembles that of renowned modern literary works.

            Initial World Details(which may have changed, review the story): {world_detail}

            Continue the story titled '{story_topic}', maintaining engagement and emotional depth, avoiding repetition of themes. Create chapters thoughtfully, only when a story section naturally concludes, and provide each chapter with a unique and intriguing title.

            The story is approximately {story_completion_percentage:.2f}% complete. You have approximately {total_token_limit - total_tokens_used} tokens remaining to conclude the narrative. Review the existing story so far, noting themes covered, pacing, and direction to ensure the continuation aligns seamlessly with the established style and format. Reviewing the story provided thus far and noting key details, build upon the previous segment, preserving coherence and continuity while balancing narrative progression with consideration of your segments position in the story timeline.

            Current Story:
            {current_story}

            Continue the story from here.
            """

            if story_completion_percentage >= 80:
                prompt += f"\nIf the story is past 90% complete, you may conclude the story with an epilogue if you see fit, and mark the end of the story with one of the following end markers: {end_markers}.\n"
            
            segment_content, tokens_used, time_taken = generate_story_segment(client, prompt, min(max_tokens_per_call, remaining_tokens))
            
            if not segment_content.strip():
                logging.error("Story generation failed, no content returned.")
                break

            current_story += " " + segment_content
            total_tokens_used += tokens_used
            total_time_taken += time_taken
            logging.info(f"Generated segment in {time_taken:.2f} seconds using {tokens_used} tokens. Total tokens used: {total_tokens_used}")

            if any(marker in segment_content for marker in end_markers):
                logging.info("End marker detected, concluding story generation.")
                break

        current_story += "\n\nThat is the end of our story today, thank you so much for listening. Please, let me know your thoughts, and be well my friends."

        intro_content, _, _ = generate_intro(client, story_topic, world_detail)
        final_story = f"Today's story is called '{story_topic}'\n\n{intro_content}\n\n{current_story}"

        foldername = story_topic.replace(' ', '_').lower()
        filename = f"{foldername}.txt"
        filepath = save_story_to_file(final_story, foldername, filename)

        story_cost = total_tokens_used * token_cost_per_million
        total_cost += story_cost
        logging.info(f"Total time taken: {total_time_taken:.2f} seconds")
        logging.info(f"Total tokens used: {total_tokens_used}")
        logging.info(f"Total cost: ${story_cost:.2f}")

        generated_story_paths.append(filepath)

    logging.info(f"Overall total cost for generating all stories: ${total_cost:.2f}")
    return generated_story_paths, total_cost

def generate_summary(client, story_content, max_tokens=4095):
    prompt = f"Provide a concise summary of the following story:\n\n{story_content}"
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
            max_tokens=max_tokens
        )
        summary = response.choices[0].message.content.strip()
        tokens_used = response.usage.total_tokens
        return summary, tokens_used
    except Exception as e:
        logging.error(f"Error during summary generation: {e}")
        return "", 0

# Export generate_summary and generate_story functions
__all__ = ["generate_summary", "generate_story"]
