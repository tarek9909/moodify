import subprocess
import requests
from flask import Flask, request, jsonify
import tempfile
import captions
app = Flask(__name__)

@app.route('/run-file', methods=['POST'])
def run_file():
    # Get the image URL from the request data
    image_url = request.json.get("image_url")
    
    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400
    
    try:
        # Download the image from the URL
        image_path = download_image(image_url)
        
        if image_path:
            # Call the captions.py script with the downloaded image as an argument
            result = captions.generate_captions_from_url(image_url)
        
        # If the result is already a string, it's the JSON response
            return result, 200
        else:
            return jsonify({"error": "Failed to download image from the URL"}), 400
    
    except subprocess.CalledProcessError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def download_image(image_url):
    # Download the image and save it temporarily
    response = requests.get(image_url)
    if response.status_code == 200:
        # Save the image to a temporary file
        temp_image = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_image.write(response.content)
        temp_image.close()
        return temp_image.name
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
