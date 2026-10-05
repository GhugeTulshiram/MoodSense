import os
import cv2
import numpy as np
import tensorflow as tf


# ==========================================
# EMOTION DETECTOR CLASS
# ==========================================
class EmotionDetector:

    def __init__(self):

        # Project root path
        base_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        # Model path
        self.model_path = os.path.join(
            base_path,
            "model",
            "emotion_model.h5"
        )

        # Labels path
        self.labels_path = os.path.join(
            base_path,
            "model",
            "labels.txt"
        )

        # Load emotion labels
        with open(self.labels_path, "r") as file:
            self.labels = [
                line.strip()
                for line in file
                if line.strip()
            ]

        # Load trained model
        if os.path.exists(self.model_path) and os.path.getsize(self.model_path) > 0:
            self.model = tf.keras.models.load_model(
                self.model_path
            )
        else:
            self.model = None

    # ==========================================
    # PREDICT EMOTION
    # ==========================================
    def predict_emotion(self, face):

        # Check whether model is available
        if self.model is None:
            return "Model Not Found", 0.0

        # Convert face to grayscale
        gray = cv2.cvtColor(
            face,
            cv2.COLOR_BGR2GRAY
        )

        # Resize face
        resized = cv2.resize(
            gray,
            (48, 48)
        )

        # Normalize pixel values
        normalized = resized / 255.0

        # Prepare image for model
        input_data = np.expand_dims(
            normalized,
            axis=(0, -1)
        )

        # Predict emotion
        prediction = self.model.predict(
            input_data,
            verbose=0
        )[0]

        # Find highest probability
        emotion_index = np.argmax(prediction)

        # Get emotion name
        emotion = self.labels[emotion_index]

        # Confidence
        confidence = float(
            prediction[emotion_index]
        )

        return emotion, confidence