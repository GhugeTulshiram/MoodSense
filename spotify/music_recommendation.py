# ==========================================
# MOODSENSE MUSIC RECOMMENDATION
# ==========================================

from spotify.spotify_api import SpotifyAPI

from utils.emotion_mapping import (
    get_music_category,
    get_emotion_description,
    get_emotion_icon
)


class MusicRecommender:

    # ==========================================
    # INITIALIZE SPOTIFY
    # ==========================================

    def __init__(self):

        self.spotify = SpotifyAPI()


    # ==========================================
    # GET MUSIC CATEGORY
    # ==========================================

    def get_music_category(self, emotion):

        return get_music_category(
            emotion
        )


    # ==========================================
    # GET EMOTION DESCRIPTION
    # ==========================================

    def get_emotion_description(
        self,
        emotion
    ):

        return get_emotion_description(
            emotion
        )


    # ==========================================
    # GET EMOTION ICON
    # ==========================================

    def get_emotion_icon(self, emotion):

        return get_emotion_icon(
            emotion
        )


    # ==========================================
    # RECOMMEND SONGS
    # ==========================================

    def recommend_songs(
        self,
        emotion,
        limit=10
    ):

        category = self.get_music_category(
            emotion
        )


        songs = self.spotify.search_songs(
            category,
            limit
        )


        return songs


    # ==========================================
    # GET COMPLETE MUSIC INFORMATION
    # ==========================================

    def get_recommendation_data(
        self,
        emotion,
        limit=10
    ):

        songs = self.recommend_songs(
            emotion,
            limit
        )


        return {

            "emotion": emotion,

            "category":
                self.get_music_category(
                    emotion
                ),

            "description":
                self.get_emotion_description(
                    emotion
                ),

            "icon":
                self.get_emotion_icon(
                    emotion
                ),

            "songs": songs

        }