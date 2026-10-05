# ==========================================
# MOODSENSE MAIN FLASK APPLICATION
# ==========================================

from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

import cv2
import base64
import numpy as np

from detection.face_detection import FaceDetector
from detection.emotion_detection import EmotionDetector

from spotify.music_recommendation import (
    MusicRecommender
)


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# INITIALIZE DETECTORS
# ==========================================

face_detector = FaceDetector()

emotion_detector = EmotionDetector()


# Spotify recommender is initialized
# only when it is required.

music_recommender = None


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# RESULT PAGE
# ==========================================

@app.route("/result")
def result():

    return render_template(
        "result.html"
    )


# ==========================================
# PLAYER PAGE
# ==========================================

@app.route("/player")
def player():

    return render_template(
        "player.html"
    )


# ==========================================
# EMOTION DETECTION API
# ==========================================

@app.route(
    "/detect",
    methods=["POST"]
)
def detect_emotion():

    try:

        # ----------------------------------
        # GET JSON DATA
        # ----------------------------------

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "emotion": None,

                "confidence": 0,

                "message":
                    "No image data received."

            })


        # ----------------------------------
        # GET BASE64 IMAGE
        # ----------------------------------

        image_data = data.get(
            "image"
        )


        if not image_data:

            return jsonify({

                "success": False,

                "emotion": None,

                "confidence": 0,

                "message":
                    "Camera image is missing."

            })


        # ----------------------------------
        # REMOVE BASE64 HEADER
        # ----------------------------------

        if "," in image_data:

            image_data = image_data.split(
                ",",
                1
            )[1]


        # ----------------------------------
        # DECODE IMAGE
        # ----------------------------------

        image_bytes = base64.b64decode(
            image_data
        )


        # ----------------------------------
        # CONVERT TO NUMPY ARRAY
        # ----------------------------------

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )


        # ----------------------------------
        # CONVERT TO OPENCV IMAGE
        # ----------------------------------

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )


        if frame is None:

            return jsonify({

                "success": False,

                "emotion": None,

                "confidence": 0,

                "message":
                    "Unable to read camera image."

            })


        # ==================================
        # DETECT FACES
        # ==================================

        faces = face_detector.detect_faces(
            frame
        )


        if len(faces) == 0:

            return jsonify({

                "success": False,

                "emotion": None,

                "confidence": 0,

                "message":
                    "No face detected. "
                    "Please position your face "
                    "clearly in front of the camera."

            })


        # ==================================
        # FIND LARGEST FACE
        # ==================================

        largest_face = max(
            faces,
            key=lambda face:
                face[2] * face[3]
        )


        x, y, w, h = largest_face


        # ==================================
        # CROP FACE
        # ==================================

        face = frame[
            y:y + h,
            x:x + w
        ]


        if face.size == 0:

            return jsonify({

                "success": False,

                "emotion": None,

                "confidence": 0,

                "message":
                    "Unable to process detected face."

            })


        # ==================================
        # PREDICT EMOTION
        # ==================================

        emotion, confidence = (
            emotion_detector.predict_emotion(
                face
            )
        )


        # ==================================
        # CHECK MODEL
        # ==================================

        if emotion == "Model Not Found":

            return jsonify({

                "success": False,

                "emotion": None,

                "confidence": 0,

                "message":
                    "Emotion model not found. "
                    "Please add "
                    "model/emotion_model.h5."

            })


        # ==================================
        # RETURN RESULT
        # ==================================

        return jsonify({

            "success": True,

            "emotion": emotion,

            "confidence": confidence

        })


    except Exception as error:

        print(
            "Detection Error:",
            error
        )


        return jsonify({

            "success": False,

            "emotion": None,

            "confidence": 0,

            "message":
                "An error occurred during "
                "emotion detection."

        })


# ==========================================
# MUSIC RECOMMENDATION API
# ==========================================

@app.route(
    "/recommend/<emotion>"
)
def recommend_music(emotion):

    global music_recommender


    try:

        # ----------------------------------
        # INITIALIZE SPOTIFY
        # ----------------------------------

        if music_recommender is None:

            music_recommender = (
                MusicRecommender()
            )


        # ----------------------------------
        # GET SONGS
        # ----------------------------------

        songs = (
            music_recommender
            .recommend_songs(
                emotion,
                limit=10
            )
        )


        # ----------------------------------
        # RETURN SONGS
        # ----------------------------------

        return jsonify({

            "success": True,

            "emotion": emotion,

            "songs": songs

        })


    except Exception as error:

        print(
            "Music Recommendation Error:",
            error
        )


        return jsonify({

            "success": False,

            "emotion": emotion,

            "songs": [],

            "message":
                str(error)

        })


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )