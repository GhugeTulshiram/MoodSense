# ==========================================
# MOODSENSE EMOTION MAPPING
# ==========================================

EMOTION_MUSIC = {

    "happy": {
        "category": "happy pop music",
        "description": "Feel-good and energetic music",
        "icon": "😊"
    },

    "sad": {
        "category": "sad emotional music",
        "description": "Emotional and relaxing music",
        "icon": "😢"
    },

    "angry": {
        "category": "rock powerful music",
        "description": "Powerful and energetic music",
        "icon": "😠"
    },

    "fear": {
        "category": "calm relaxing music",
        "description": "Calm and peaceful music",
        "icon": "😨"
    },

    "disgust": {
        "category": "alternative chill music",
        "description": "Alternative and chill music",
        "icon": "🤢"
    },

    "surprise": {
        "category": "energetic exciting music",
        "description": "Energetic and exciting music",
        "icon": "😲"
    },

    "neutral": {
        "category": "chill relaxing music",
        "description": "Chill and relaxing music",
        "icon": "😐"
    }

}


def get_music_category(emotion):

    emotion = emotion.lower().strip()

    emotion_data = EMOTION_MUSIC.get(
        emotion
    )

    if emotion_data:
        return emotion_data["category"]

    return "chill relaxing music"


def get_emotion_description(emotion):

    emotion = emotion.lower().strip()

    emotion_data = EMOTION_MUSIC.get(
        emotion
    )

    if emotion_data:
        return emotion_data["description"]

    return "Personalized music for your mood."


def get_emotion_icon(emotion):

    emotion = emotion.lower().strip()

    emotion_data = EMOTION_MUSIC.get(
        emotion
    )

    if emotion_data:
        return emotion_data["icon"]

    return "🎵"