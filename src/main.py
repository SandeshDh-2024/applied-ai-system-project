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


def profile_warnings(user_prefs: dict) -> list[str]:
    """Return simple diagnostics for intentionally adversarial profiles."""
    warnings: list[str] = []

    target_energy = user_prefs.get("target_energy")
    if not isinstance(target_energy, (int, float)):
        warnings.append("target_energy is non-numeric")
    elif not (0.0 <= float(target_energy) <= 1.0):
        warnings.append("target_energy is outside [0, 1]")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if not isinstance(likes_acoustic, bool):
        warnings.append("likes_acoustic is not a bool (Python bool coercion may surprise)")

    genre = str(user_prefs.get("favorite_genre", ""))
    mood = str(user_prefs.get("favorite_mood", ""))
    if genre != genre.strip() or mood != mood.strip():
        warnings.append("genre/mood include leading or trailing whitespace")
    if genre.lower() != genre or mood.lower() != mood:
        warnings.append("genre/mood are not lowercase (exact match is case-sensitive)")

    return warnings


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    user_profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.82,
            "target_tempo_bpm": 120,
            "target_valence": 0.85,
            "target_danceability": 0.80,
            "target_acousticness": 0.20,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.38,
            "target_tempo_bpm": 78,
            "target_valence": 0.58,
            "target_danceability": 0.60,
            "target_acousticness": 0.82,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.92,
            "target_tempo_bpm": 150,
            "target_valence": 0.45,
            "target_danceability": 0.55,
            "target_acousticness": 0.12,
            "likes_acoustic": False,
        },
    }

    selected_profile_name = "High-Energy Pop"
    user_prefs = user_profiles[selected_profile_name]
    print(f"Using profile: {selected_profile_name}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{rank}. {song['title']}")
        print(f"   Final score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()

    adversarial_profiles = {
        "Conflict: High-Energy + Melancholic": {
            "favorite_genre": "pop",
            "favorite_mood": "melancholic",
            "target_energy": 0.95,
            "target_tempo_bpm": 120,
            "target_valence": 0.25,
            "target_danceability": 0.75,
            "target_acousticness": 0.80,
            "likes_acoustic": True,
        },
        "Boolean Trap: String False": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.90,
            "target_tempo_bpm": 150,
            "target_valence": 0.50,
            "target_danceability": 0.60,
            "target_acousticness": 0.20,
            "likes_acoustic": "False",
        },
        "Out-of-Range Energy High": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 2.0,
            "target_tempo_bpm": 80,
            "target_valence": 0.60,
            "target_danceability": 0.55,
            "target_acousticness": 0.90,
            "likes_acoustic": True,
        },
        "Out-of-Range Energy Low": {
            "favorite_genre": "house",
            "favorite_mood": "euphoric",
            "target_energy": -1.0,
            "target_tempo_bpm": 126,
            "target_valence": 0.80,
            "target_danceability": 0.90,
            "target_acousticness": 0.10,
            "likes_acoustic": False,
        },
        "Unknown Genre/Mood": {
            "favorite_genre": "hyperpop",
            "favorite_mood": "transcendental",
            "target_energy": 0.80,
            "target_tempo_bpm": 130,
            "target_valence": 0.70,
            "target_danceability": 0.80,
            "target_acousticness": 0.30,
            "likes_acoustic": False,
        },
        "Case + Whitespace Mismatch": {
            "favorite_genre": "Pop ",
            "favorite_mood": "Happy",
            "target_energy": 0.82,
            "target_tempo_bpm": 118,
            "target_valence": 0.80,
            "target_danceability": 0.80,
            "target_acousticness": 0.20,
            "likes_acoustic": False,
        },
    }

    print("\nAdversarial profile simulation:\n")
    for profile_name, prefs in adversarial_profiles.items():
        print(f"Profile: {profile_name}")
        flags = profile_warnings(prefs)
        if flags:
            print("  Flags:")
            for flag in flags:
                print(f"   - {flag}")
        else:
            print("  Flags: none")

        top = recommend_songs(prefs, songs, k=3)
        for rank, (song, score, explanation) in enumerate(top, start=1):
            print(f"  {rank}. {song['title']} | score={score:.2f}")
            print(f"     reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()
