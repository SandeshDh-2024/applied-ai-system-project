"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from pathlib import Path
    import streamlit as st
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    from .recommender import load_songs
    from .workflow import run_recommendation_workflow
except ImportError:
    from pathlib import Path
    import streamlit as st
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
    except ImportError:
        get_script_run_ctx = lambda: None  # type: ignore[assignment]

    from recommender import load_songs
    from workflow import run_recommendation_workflow


def _songs_csv_path() -> str:
    """Return the absolute path to the songs CSV regardless of the launch directory."""
    return str(Path(__file__).resolve().parents[1] / "data" / "songs.csv")


def _profile_catalog() -> dict[str, dict]:
    return {
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


def _render_profile_result(title: str, workflow_result: dict) -> None:
    st.subheader(title)
    st.caption(f"Confidence: {workflow_result['confidence']:.2f}")

    if workflow_result["warnings"]:
        st.warning("Profile warnings:\n- " + "\n- ".join(workflow_result["warnings"]))

    for rank, (song, score, explanation) in enumerate(workflow_result["recommendations"], start=1):
        with st.container(border=True):
            st.markdown(f"**{rank}. {song['title']}**  ")
            st.write(f"Artist: {song['artist']}")
            st.write(f"Final score: {score:.2f}")
            st.write(f"Reasons: {explanation}")


def render_streamlit_app() -> None:
    st.set_page_config(page_title="Music Recommender Simulation", layout="wide")
    st.title("Music Recommender Simulation")
    st.write(
        "A transparent music recommender with deterministic ranking, lightweight retrieval, "
        "and simple workflow guardrails."
    )

    songs = load_songs(_songs_csv_path())
    profiles = _profile_catalog()

    col_left, col_right = st.columns([0.9, 1.1])

    with col_left:
        st.subheader("User Profile")
        selected_profile_name = st.selectbox("Choose a starting profile", list(profiles.keys()))
        selected_profile = profiles[selected_profile_name].copy()

        favorite_genre = st.text_input("Favorite genre", value=selected_profile["favorite_genre"])
        favorite_mood = st.text_input("Favorite mood", value=selected_profile["favorite_mood"])
        target_energy = st.slider("Target energy", 0.0, 1.0, float(selected_profile["target_energy"]), 0.01)
        target_tempo_bpm = st.number_input("Target tempo (BPM)", min_value=40, max_value=220, value=int(selected_profile["target_tempo_bpm"]), step=1)
        target_valence = st.slider("Target valence", 0.0, 1.0, float(selected_profile["target_valence"]), 0.01)
        target_danceability = st.slider("Target danceability", 0.0, 1.0, float(selected_profile["target_danceability"]), 0.01)
        target_acousticness = st.slider("Target acousticness", 0.0, 1.0, float(selected_profile["target_acousticness"]), 0.01)
        likes_acoustic = st.checkbox("Likes acoustic music", value=bool(selected_profile["likes_acoustic"]))
        top_k = st.slider("Number of recommendations", 1, 5, 3)

        run_button = st.button("Generate recommendations", type="primary")

    with col_right:
        st.subheader("Results")
        if run_button:
            user_prefs = {
                "favorite_genre": favorite_genre,
                "favorite_mood": favorite_mood,
                "target_energy": target_energy,
                "target_tempo_bpm": target_tempo_bpm,
                "target_valence": target_valence,
                "target_danceability": target_danceability,
                "target_acousticness": target_acousticness,
                "likes_acoustic": likes_acoustic,
            }
            workflow_result = run_recommendation_workflow(user_prefs, songs, k=top_k)
            _render_profile_result("Recommendations", workflow_result)
        else:
            st.info("Choose a profile and click Generate recommendations to see ranked songs.")

    with st.expander("How it works", expanded=False):
        st.write(
            "The app validates the user profile, ranks songs with deterministic scoring, retrieves grounded facts "
            "for the top songs, and returns a short explanation with a confidence value."
        )


def run_cli_demo() -> None:
    songs = load_songs(_songs_csv_path())
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

    workflow_result = run_recommendation_workflow(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    if workflow_result["warnings"]:
        print("Profile warnings:")
        for warning in workflow_result["warnings"]:
            print(f" - {warning}")
        print()

    print(f"Confidence: {workflow_result['confidence']:.2f}\n")

    for rank, rec in enumerate(workflow_result["recommendations"], start=1):
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
        flags = run_recommendation_workflow(prefs, songs, k=3)["warnings"]
        if flags:
            print("  Flags:")
            for flag in flags:
                print(f"   - {flag}")
        else:
            print("  Flags: none")

        top = run_recommendation_workflow(prefs, songs, k=3)["recommendations"]
        for rank, (song, score, explanation) in enumerate(top, start=1):
            print(f"  {rank}. {song['title']} | score={score:.2f}")
            print(f"     reasons: {explanation}")
        print()


def main() -> None:
    if get_script_run_ctx() is not None:
        render_streamlit_app()
        return

    run_cli_demo()


if __name__ == "__main__":
    main()
