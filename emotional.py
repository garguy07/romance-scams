import json
import os
import google.generativeai as genai 

GEMINI_API_KEY = "AIzaSyBfcZFOlDRMZAKptSna6WV77bjwlU8haHY"
CHECKPOINT_FILE = "checkpoint.json"  # File to save progress

def get_response_from_gemini(prompt):
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    print("Gemini Response:", response.text)
    return response.text


def load_checkpoint():
    """
    Load the checkpoint to determine the last processed index.

    Returns:
        int: The index of the last processed summary, or 0 if no checkpoint exists.
    """
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as file:
            checkpoint = json.load(file)
            return checkpoint.get("last_processed_index", 0)
    return 0


def save_checkpoint(last_processed_index):
    """
    Save the checkpoint to record the last processed index.

    Args:
        last_processed_index (int): The index of the last processed summary.
    """
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as file:
        json.dump({"last_processed_index": last_processed_index}, file)


def extract_and_append_emotions(json_file_path, batch_size=5):
    """
    Extract summaries from the JSON file, construct prompts in batches, and append emotional mechanisms.

    Args:
        json_file_path (str): Path to the JSON file.
        batch_size (int): Number of summaries to process in each batch.
    """
    try:
        # Load the JSON data
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        # Load the last processed index from the checkpoint
        last_processed_index = load_checkpoint()

        # Collect summaries in batches starting from the last processed index
        summaries = []
        entries = []
        for idx, entry in enumerate(data):
            if idx < last_processed_index:
                continue  # Skip already processed entries

            summary = entry.get("Summary", "")
            if summary:
                summaries.append(summary)
                entries.append(entry)

                # Process the batch when it reaches the batch size
                if len(summaries) == batch_size:
                    process_batch(summaries, entries)
                    summaries = []
                    entries = []

                    # Save the checkpoint
                    save_checkpoint(idx + 1)

        # Process any remaining summaries
        if summaries:
            process_batch(summaries, entries)
            save_checkpoint(len(data))  # Save the final checkpoint

        print("✅ Emotional mechanisms appended successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


def process_batch(summaries, entries):
    """
    Process a batch of summaries and append the generated emotional mechanisms to the corresponding entries.

    Args:
        summaries (list): List of summaries to process.
        entries (list): List of corresponding entries in the JSON data.
    """
    # Construct a single prompt for the batch
    prompt = "Given the following summaries:\n"
    for i, summary in enumerate(summaries, start=1):
        prompt += f"{i}. {summary}\n"
    prompt += "Generate only the names of emotional mechanisms associated with each summary. Separate multiple mechanisms with commas. Return in the form of a JSON array, where each element corresponds to a summary."

    print("Prompt to Gemini:", prompt)

    # Get the response from Gemini
    response = get_response_from_gemini(prompt)

    try:
        # Parse the response as a JSON array
        emotional_mechanisms = json.loads(response)

        # Append the emotional mechanisms to the corresponding entries
        for entry, mechanisms in zip(entries, emotional_mechanisms):
            entry["Emotional Mechanisms (Generated)"] = mechanisms

    except json.JSONDecodeError:
        print("❌ Failed to parse Gemini response as JSON:", response)


# Define the path to the JSON file
json_file_path = "Romance_Scam_Dataset.json"

# Call the function to process the JSON file
extract_and_append_emotions(json_file_path, batch_size=5)