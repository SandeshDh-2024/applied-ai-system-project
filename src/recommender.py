import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


def _get_value(item, key: str):
    """Return a field value from either a dict or a dataclass object."""
    if isinstance(item, dict):
        return item[key]
    return getattr(item, key)


def score_song(user_prefs, song) -> Tuple[float, List[str]]:
    """Score one song and return its numeric score plus explanation reasons."""
    reasons: List[str] = []
    score = 0.0

    favorite_genre = _get_value(user_prefs, "favorite_genre")
    favorite_mood = _get_value(user_prefs, "favorite_mood")
    target_energy = float(_get_value(user_prefs, "target_energy"))
    likes_acoustic = bool(_get_value(user_prefs, "likes_acoustic"))

    song_genre = _get_value(song, "genre")
    song_mood = _get_value(song, "mood")
    song_energy = float(_get_value(song, "energy"))
    song_acousticness = float(_get_value(song, "acousticness"))

    if song_genre == favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song_mood == favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_points = 2.0 * (1.0 - abs(target_energy - song_energy))
    energy_points = max(0.0, min(2.0, energy_points))
    score += energy_points
    reasons.append(f"energy close (+{energy_points:.1f})")

    if likes_acoustic and song_acousticness >= 0.7:
        score += 0.5
        reasons.append("acoustic preference (+0.5)")
    elif not likes_acoustic and song_acousticness <= 0.4:
        score += 0.5
        reasons.append("less acoustic preference (+0.5)")

    return score, reasons

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences and audio feature targets.
    Required by tests/test_recommender.py
    """
    # Genre and mood preferences
    favorite_genre: str
    favorite_mood: str
    
    # Audio feature targets
    target_energy: float              # Preferred energy level (0-1)
    target_tempo_bpm: float           # Preferred tempo in beats per minute
    target_valence: float             # Preferred valence/positivity (0-1)
    target_danceability: float        # Preferred danceability (0-1)
    target_acousticness: float        # Preferred acousticness (0-1)
    
    # Binary preferences
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked_songs = sorted(
            self.songs,
            key=lambda song: (
                -score_song(user, song)[0],
                abs(float(user.target_energy) - float(song.energy)),
                song.title,
            ),
        )
        return ranked_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(user, song)
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": int(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    ranked_songs = sorted(
        scored_songs,
        key=lambda item: (
            -item[1],
            abs(float(user_prefs["target_energy"]) - float(item[0]["energy"])),
            item[0]["title"],
        ),
    )

    return [
        (song, score, ", ".join(reasons))
        for song, score, reasons in ranked_songs[:k]
    ]
