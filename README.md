# 🎵 Music Recommender Simulation

Screenshots:

Phase3: Implementation:
![alt text](pop/happy_profile.png)

Phase 4: Evaluate and Explain
![alt text](adverse_1.png) 
![alt text](adverse_2.png)

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works
Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world recommenders (like Spotify or YouTube) blend behavior data (what similar users liked, skipped, replayed, or saved) with content signals (the attributes of each song or video) to predict what a specific person will enjoy next. This simulation prioritizes transparent, content-based matching: each song gets a score based on how closely its vibe-related features match the user's preferences, and the highest-scoring songs are recommended.

`Song` features used in this simulation:
- `genre`
- `mood`
- `energy`
- `tempo_bpm`
- `valence`
- `danceability`
- `acousticness`

`UserProfile` features used in this simulation:

- `preferred_genres` (or one target genre)
- `preferred_moods` (or one target mood)
- `target_energy`
- `target_tempo_bpm`
- `target_valence`
- `target_danceability`
- `target_acousticness`

`Recommender` flow:
- Compute a weighted score for each song using exact matches for categorical features and closeness for numeric features.
- Rank songs by total score.
- Return the top `N` songs as recommendations.


This recommender uses a transparent, content-based scoring process. It compares each song in the catalog to one user profile, gives each song a score, then returns the highest-scoring results.

Input (User Preferences):

- Preferred genre
- Preferred mood
- Target energy value (0.0 to 1.0)
- Number of recommendations to return (Top K)

Process (Scoring Each Song):

For each song in the CSV, compute:

- Genre match: +2.0 points if the song genre matches the preferred genre
- Mood match: +1.0 point if the song mood matches the preferred mood
- Energy similarity: from 0.0 to +2.0 points based on closeness to the user's target energy

Energy similarity formula:

energy_points = 2.0 * (1 - abs(target_energy - song_energy))

Total score formula:

total_score = genre_points + mood_points + energy_points

Output (Ranking):

- Store each song with its total score
- Sort songs by score (highest to lowest)
- Use tie-breakers for equal scores (smaller energy difference first, then title order)
- Return Top K songs as recommendations

Potential bias to watch for:
- Compute a weighted score for each song using exact matches for categorical features and closeness for numeric features.
- Rank songs by total score.
- Return the top `N` songs as recommendations.
- This system may over-prioritize genre (+2.0) relative to mood (+1.0), which can cause it to miss songs that strongly match mood and energy but use a different genre label.
- Exact-match rules for genre and mood can also under-recommend cross-genre or mood-adjacent songs that a human listener might still enjoy.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"



