import google.generativeai as genai
from hashtags import generate_and_print_hashtags
import json
import requests
import tempfile

# Function to download image from URL
def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        # Save the image to a temporary file
        temp_image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_image.write(response.content)
        temp_image.close()
        return temp_image.name
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")

# Configure Google Generative AI API
genai.configure(api_key="AIzaSyBOgj4YkbMWPruuDOpczhlkRAbu43tGktQ")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Function to generate captions and hashtags based on the image URL
def generate_captions_from_url(image_url):
    try:
        # Download the image from URL
        image_path = download_image(image_url)
        
        # Specify the emotion labels file path (if needed)
        emotion_labels_path = 'hashtag.json'

        # Call the function to generate and print hashtags
        results_hashtags = generate_and_print_hashtags(image_path, emotion_labels_path)

        # Create prompt for caption generation
        prompt_parts = [
            f"generate one modern caption that represents the emotion found in the words of this list, but do not put any words of the list in it: {', '.join(results_hashtags)}",
        ]

        # Generate the response using your model
        response = model.generate_content(prompt_parts)

        # Filter unsafe content
        for candidate in response.candidates:
            for rating in candidate.safety_ratings:
                if rating.probability == 'HIGH':  # Block unsafe content
                    return json.dumps({"error": f"Content blocked due to: {rating.category}"}), 400

        # Parse and return the output in JSON format
        output = {
            "hashtags": results_hashtags,
            "captions": response.text.strip() if hasattr(response, 'text') else "No valid caption generated."
        }
        return json.dumps(output)

    except Exception as e:
        return json.dumps({"error": str(e)}), 500


