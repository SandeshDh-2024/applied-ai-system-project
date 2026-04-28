from src.recommender import Song, UserProfile, Recommender
from src.workflow import run_recommendation_workflow

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def make_user_profile() -> UserProfile:
    return UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_tempo_bpm=120,
        target_valence=0.9,
        target_danceability=0.8,
        target_acousticness=0.2,
        likes_acoustic=False,
    )


def test_recommend_returns_songs_sorted_by_score():
    user = make_user_profile()
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = make_user_profile()
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_recommendation_explanation_mentions_key_match_reasons():
    user = make_user_profile()
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)

    assert "genre match" in explanation
    assert "mood match" in explanation
    assert "energy close" in explanation


def test_string_false_does_not_count_as_acoustic_preference():
    user = make_user_profile()
    user.likes_acoustic = "False"
    rec = make_small_recommender()
    song = rec.songs[1]

    explanation = rec.explain_recommendation(user, song)

    assert "acoustic preference" not in explanation


def test_text_inputs_are_normalized_before_matching():
    user = make_user_profile()
    user.favorite_genre = " Pop "
    user.favorite_mood = " HAPPY "
    rec = make_small_recommender()

    reasons = rec.explain_recommendation(user, rec.songs[0])

    assert "genre match" in reasons
    assert "mood match" in reasons


def test_workflow_reports_boolean_warning_for_string_value():
    user = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_tempo_bpm": 120,
        "target_valence": 0.9,
        "target_danceability": 0.8,
        "target_acousticness": 0.2,
        "likes_acoustic": "False",
    }
    rec = make_small_recommender()

    result = run_recommendation_workflow(user, rec.songs, k=1)

    assert "likes_acoustic is not a bool" in result["warnings"]
    assert result["confidence"] < 1.0
