import json
from google import genai
from google.genai import types

GEMINI_API_KEY = "AIzaSyB7GBGSK6vkBP9q0xqWD91hv1vR9xAf1xE"


def get_response_from_gemini(prompt):
    """
    Simulate getting a response from the Gemini model.
    In a real implementation, this function would call the Gemini API.

    Args:
        prompt (str): The prompt to send to Gemini.
    Returns:
        str: Simulated response from Gemini.
    """

    client = genai.Client(api_key=GEMINI_API_KEY)
    config = types.GenerateContentConfig(temperature=0.1, max_output_tokens=1024)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    print("Gemini Response:", response.text)
    return response.text


def extract_and_append_emotions(json_file_path):
    """
    Extract summaries from the JSON file, construct prompts, and append emotional mechanisms.

    Args:
        json_file_path (str): Path to the JSON file.
    """
    try:
        # Load the JSON data
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        count = 0

        # Iterate through each entry and process the summary
        for entry in data:
            summary = entry.get("Summary", "")
            if summary:
                # Construct the prompt for Gemini
                prompt = f"Given the following summary: {summary}\nGenerate only the names of emotional mechanisms associated with the above summary. Separate multiple mechanisms with commas. Return in the form of a json array."

                print("Prompt to Gemini:", prompt)

                # Simulate Gemini response (replace this with actual Gemini API call if available)
                response = get_response_from_gemini(
                    prompt
                )  # Use the actual Gemini API call

                # print("Emotional Mechanisms Generated:", response)

                # Append the emotional mechanisms to the entry
                entry["Emotional Mechanisms (Generated)"] = (
                    response  # Store the response
                )

                count += 1

                if count == 2:
                    break  # Remove or adjust this line to process all entries

        # Save the updated JSON data back to the file
        # with open(json_file_path, "w", encoding="utf-8") as json_file:
        # json.dump(data, json_file, indent=2, ensure_ascii=False)

        print("✅ Emotional mechanisms appended successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


# Define the path to the JSON file
json_file_path = "Romance_Scam_Dataset.json"

# Call the function to process the JSON file
extract_and_append_emotions(json_file_path)
