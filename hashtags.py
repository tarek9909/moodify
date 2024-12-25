import json
import random
from img_predict import predict_emotion

def load_emotion_labels_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def generate_hashtags(keyword, min_count_to_select=5, max_count_to_select=30, max_attempts=100, emotion_labels=None):
    if emotion_labels is None:
        raise ValueError("Emotion labels not provided.")

    for _ in range(max_attempts):
        synonyms = set()

        # Use emotion labels from the file instead of NLTK
        if keyword in emotion_labels:
            synonyms.update(emotion_labels[keyword])

        # Add the original keyword to the set
        synonyms.add(keyword.lower())

        # Generate a random count between min_count_to_select and max_count_to_select
        count_to_select = random.randint(min_count_to_select, max_count_to_select)

        # Check if the set of synonyms is large enough
        if len(synonyms) >= count_to_select:
            # Create hashtags by adding '#' to each word
            hashtags = ['#' + word.lower() for word in synonyms]

            # Shuffle the hashtags to get a random order
            random.shuffle(hashtags)

            # Select a random number of hashtags between min_count_to_select and max_count_to_select
            selected_hashtags = hashtags[:count_to_select]

            return selected_hashtags

    raise ValueError(f"Could not generate unique hashtags after {max_attempts} attempts")

def generate_and_print_hashtags(image_path, emotion_labels_path='hashtag.json'):
    # Load emotion labels from the file
    emotion_labels = load_emotion_labels_from_file(emotion_labels_path)

    # Example usage
    predicted = predict_emotion(image_path)
    hashtags = generate_hashtags(predicted, emotion_labels=emotion_labels)
    return hashtags

