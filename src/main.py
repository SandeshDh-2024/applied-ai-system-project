"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    # Taste profile for recommendation comparisons
    # This profile describes a user who enjoys chill, acoustic lofi music
    # suitable for studying, relaxing, or background ambiance
    user_prefs = {
        # Genre and mood preferences
        "favorite_genre": "pop",           # Prefers pop songs
        "favorite_mood": "happy",          # Likes upbeat, positive moods
        
        # Audio feature targets (normalized 0-1 or in BPM)
        "target_energy": 0.82,              # Higher energy for upbeat pop
        "target_tempo_bpm": 120,            # Brisk tempo for pop tracks
        "target_valence": 0.85,             # Positive, cheerful mood
        "target_danceability": 0.80,        # Danceable and catchy
        "target_acousticness": 0.20,        # Less acoustic, more produced sound
        
        # Binary preference
        "likes_acoustic": False,            # Does not strongly prefer acoustic elements
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{rank}. {song['title']}")
        print(f"   Final score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()
