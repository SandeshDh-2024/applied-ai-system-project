"""Lightweight retrieval layer for grounded recommendation explanations."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List


def _normalize_text(value: Any) -> str:
    return str(value).strip().lower()


def _coerce_song(song: Any) -> Dict[str, Any]:
    if is_dataclass(song):
        return asdict(song)
    return song


def _get_profile_value(profile: Any, key: str, default: Any = None) -> Any:
    """Helper to get a value from a dict or an object (like a dataclass)."""
    if isinstance(profile, dict):
        return profile.get(key, default)
    return getattr(profile, key, default)


class SongRetriever:
    """Retrieve grounded evidence snippets from user preferences and song metadata."""

    def __init__(self, songs: List[Any]):
        self.songs = [_coerce_song(song) for song in songs]

    def retrieve(self, user_prefs: Any, song: Any) -> List[str]:
        # Handle both dict and object/dataclass for user_prefs
        normalized_user = {
            "favorite_genre": _normalize_text(_get_profile_value(user_prefs, "favorite_genre", "")),
            "favorite_mood": _normalize_text(_get_profile_value(user_prefs, "favorite_mood", "")),
            "target_energy": float(_get_profile_value(user_prefs, "target_energy", 0.0)),
            "likes_acoustic": _get_profile_value(user_prefs, "likes_acoustic") is True,
        }

        song_data = _coerce_song(song)
        song_genre = _normalize_text(song_data["genre"])
        song_mood = _normalize_text(song_data["mood"])
        song_energy = float(song_data["energy"])
        song_acousticness = float(song_data["acousticness"])

        evidence: List[str] = [
            f"song genre: {song_genre}",
            f"song mood: {song_mood}",
            f"song energy: {song_energy:.2f}",
            f"song acousticness: {song_acousticness:.2f}",
        ]

        if song_genre == normalized_user["favorite_genre"]:
            evidence.append(f"genre match: {song_genre} matches user preference {normalized_user['favorite_genre']}")
        if song_mood == normalized_user["favorite_mood"]:
            evidence.append(f"mood match: {song_mood} matches user preference {normalized_user['favorite_mood']}")

        energy_gap = abs(normalized_user["target_energy"] - song_energy)
        evidence.append(f"energy gap: {energy_gap:.2f} from target {normalized_user['target_energy']:.2f}")

        if normalized_user["likes_acoustic"] and song_acousticness >= 0.7:
            evidence.append("acoustic preference: high acousticness supports this user's preference")
        elif not normalized_user["likes_acoustic"] and song_acousticness <= 0.4:
            evidence.append("acoustic preference: lower acousticness supports this user's preference")

        return evidence
