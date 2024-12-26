import cv2
import numpy as np
from tensorflow.keras.utils import register_keras_serializable
from tensorflow.keras import Sequential
from keras.models import model_from_json
from keras.preprocessing import image
from PIL import Image
import os

register_keras_serializable()(Sequential)

def convert_png_to_jpg(image_path):
    """Converts a PNG image to JPG format and returns the new file path."""
    img = Image.open(image_path)
    # Handle transparency by converting to RGB
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    # Create new path with .jpg extension
    new_path = os.path.splitext(image_path)[0] + '.jpg'
    img.save(new_path, 'JPEG')
    return new_path

def predict_emotion(image_path):
    # Check if the input image is in PNG format
    if image_path.lower().endswith('.png'):
        # Convert PNG to JPG
        image_path = convert_png_to_jpg(image_path)

    # Load model from JSON file
    json_file = open('top_models\\fer.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)

    # Load weights into model
    model.load_weights('top_models/fer.h5')

    # Load face classifier
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Read the image
    img = cv2.imread(image_path)
    if img is None:  # Check if image is loaded properly
        print("Error: Could not load image.")
        return None

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces_detected = classifier.detectMultiScale(gray_img, 1.18, 5)

    # Default prediction if no face is detected
    predicted_emotion = "No face detected"

    # Process each detected face
    for (x, y, w, h) in faces_detected:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray_img[y:y + w, x:x + h]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        img_pixels = image.img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255.0

        predictions = model.predict(img_pixels, verbose=0)
        max_index = int(np.argmax(predictions))

        # Emotion labels
        emotions = ['neutral', 'happy', 'surprise', 'sadness', 'anger', 'disgust', 'fear']
        predicted_emotion = emotions[max_index]

        # Label the image
        cv2.putText(img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    # Display the image
    resized_img = cv2.resize(img, (1024, 768))
    cv2.imshow('Emotion Detection', resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(predicted_emotion)
    return predicted_emotion

