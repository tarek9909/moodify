import subprocess
import requests
from flask import Flask, request, jsonify
import tempfile
import base64
import io
from PIL import Image
import captions
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all origins (you can restrict this to specific origins if needed)
CORS(app)

@app.route('/run-file', methods=['POST'])
def run_file():
    # Get the base64 image data from the request data
    image_base64 = request.json.get("image_base64")
    
    if not image_base64:
        # Return a JSON error response with a 400 status code
        return jsonify({"error": "No image data provided"}), 400
    
    try:
        # Decode the base64 image data
        image_path = save_base64_image(image_base64)
        
        if image_path:
            # Call the captions.py script with the saved image path as an argument
            result = captions.generate_captions_from_url(image_path)  # Update the method to accept a local file path
            
            # Return the result from the captions generator
            return jsonify(result), 200
        else:
            return jsonify({"error": "Failed to save the image"}), 400
    
    except Exception as e:
        # Return a JSON error response for general errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def save_base64_image(image_base64):
    try:
        # Remove the base64 prefix (if any)
        if image_base64.startswith('data:image'):
            image_base64 = image_base64.split(',')[1]
        
        # Decode the base64 string to binary data
        image_data = base64.b64decode(image_base64)
        
        # Save the binary data to a temporary image file
        temp_image = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        with open(temp_image.name, 'wb') as f:
            f.write(image_data)
        
        return temp_image.name
    except Exception as e:
        print(f"Error decoding base64 image: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
