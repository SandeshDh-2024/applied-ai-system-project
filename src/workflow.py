"""Workflow orchestration for the music recommender simulation."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List, Tuple

try:
    from .recommender import recommend_songs
except ImportError:
    from recommender import recommend_songs


def validate_profile(user_prefs: Dict[str, Any]) -> List[str]:
    """Return lightweight warnings for obviously risky inputs."""
    warnings: List[str] = []

    target_energy = user_prefs.get("target_energy")
    if not isinstance(target_energy, (int, float)):
        warnings.append("target_energy is non-numeric")
    elif not (0.0 <= float(target_energy) <= 1.0):
        warnings.append("target_energy is outside [0, 1]")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if not isinstance(likes_acoustic, bool):
        warnings.append("likes_acoustic is not a bool")

    genre = str(user_prefs.get("favorite_genre", ""))
    mood = str(user_prefs.get("favorite_mood", ""))
    if genre != genre.strip() or mood != mood.strip():
        warnings.append("genre/mood include leading or trailing whitespace")

    return warnings


def _coerce_songs(songs: List[Any]) -> List[Dict[str, Any]]:
    """Convert dataclass songs to dicts so the functional recommender can process them."""
    coerced: List[Dict[str, Any]] = []
    for song in songs:
        if is_dataclass(song):
            coerced.append(asdict(song))
        else:
            coerced.append(song)
    return coerced


def run_recommendation_workflow(
    user_prefs: Dict[str, Any],
    songs: List[Dict[str, Any]],
    k: int = 5,
) -> Dict[str, Any]:
    """Validate, rank, and package recommendations for presentation."""
    warnings = validate_profile(user_prefs)
    normalized_songs = _coerce_songs(songs)
    recommendations = recommend_songs(user_prefs, normalized_songs, k=k)

    return {
        "warnings": warnings,
        "recommendations": recommendations,
        "confidence": 1.0 if not warnings else 0.75,
    }