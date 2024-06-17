import re

def clean_story_text(story_text):
    # Step 1: Remove all asterisks
    story_text = story_text.replace('*', '')

    # Step 2: Remove all "-" in sequence unless within paragraph text
    story_text = re.sub(r'\s*-\s*', ' ', story_text)

    # Step 3: Remove all subtitles including the content following "Subtitle:" or any case variation
    story_text = re.sub(r'\s*subtitle:.*?(?=[.?!]|\n|$)', '', story_text, flags=re.IGNORECASE)

    # Step 4: Remove all "#" found in the document except within a sentence
    story_text = re.sub(r'\s*#\s*', '', story_text)

    # Step 5: Remove all occurrences of "Segment" followed by a space and a digit
    story_text = re.sub(r'Segment \d+', '', story_text, flags=re.IGNORECASE)

    # Step 6: Retain only the first instance of each "CHAPTER" followed by an integer digit and title
    seen_chapters = set()
    cleaned_lines = []
    for line in story_text.split('\n'):
        chapter_match = re.match(r'(CHAPTER \d+:.*)', line, re.IGNORECASE)
        if chapter_match:
            chapter_title = chapter_match.group(1).upper()
            if chapter_title not in seen_chapters:
                seen_chapters.add(chapter_title)
                cleaned_lines.append(chapter_title)
        else:
            cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    return cleaned_text.strip()

def main():
    # Read the content of the existing text file
    with open('generated_story.txt', 'r', encoding='utf-8') as file:
        story_text = file.read()

    # Clean the story text
    cleaned_story_text = clean_story_text(story_text)

    # Save the cleaned story text to a new file
    with open('cleaned_story.txt', 'w') as file:
        file.write(cleaned_story_text)

    print("Story has been cleaned and saved to 'cleaned_story.txt'.")

if __name__ == "__main__":
    main()
