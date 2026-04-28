# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeMatch Lite 1.0

---

## 2. Intended Use  

This recommender suggests songs a user might like based on simple preferences.
It assumes the user can provide one favorite genre, one favorite mood, a target energy value, and an acoustic preference.
It is designed for classroom exploration and learning, not production music apps.

Intended use: quick demos of recommendation logic, profile testing, and basic explainability.
Non-intended use: high-stakes decisions, mental health support, or real commercial personalization.

---

## 3. How the Model Works  

Each song gets points from a few rules.
The model adds points if genre matches and if mood matches.
It also gives more points when song energy is close to the user's target energy.
It gives a small bonus for acoustic or less-acoustic songs based on the user's binary preference.
Songs are then sorted by total score, with energy closeness used again as a tie-break.
The retrieval layer then collects grounded facts from the selected song so the explanation can point back to metadata instead of inventing a story.

---

## 4. Data  

The dataset has 18 songs.
Each song includes title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.
Genres include pop, lofi, rock, house, hip-hop, jazz, classical, and more.
The dataset is small, so many music tastes are missing and long-tail variety is limited.
I did not add or remove songs during testing.

---

## 5. Strengths  

It works well for clear profiles like High-Energy Pop and Chill Lofi.
The top songs often make sense when user preferences are consistent.
The explanation text helps show why a song ranked highly.
Energy matching is easy to understand and usually behaves predictably.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

One weakness is strict text matching for genre and mood.
Small input changes like capitalization or extra spaces can remove match points.
When that happens, the system falls back mostly to energy and acoustic scoring.
This can over-promote songs like Gym Hero for many energetic profiles.
The model also ignores some profile features (tempo, valence, and danceability) during scoring.
I added a small guardrail so non-boolean values like the string "False" do not accidentally count as a true acoustic preference.
I also added normalization for genre and mood so the model handles spacing and capitalization mistakes more gracefully.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested baseline profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock.
I also tested adversarial profiles with conflicting tastes, bad boolean values, out-of-range energy, and label mismatches.
I compared top recommendations and the reason strings for each result.
I ran one logic experiment by shifting weights, then compared before vs after rankings.
The biggest surprise was how much small input formatting issues changed outcomes.
After updating the test suite, the current automated checks pass.
The workflow layer now also reports validation warnings and a simple confidence score.
The retrieval layer helped keep explanations grounded in the actual song metadata.

---

## 8. Future Work  

1. Add explicit handling for unknown genres and moods (controlled fallback labels instead of silent misses).
2. Use more profile features in scoring, especially tempo, valence, and danceability.
3. Add a diversity rule so top results are not too similar in genre or mood.

---

## 9. Personal Reflection  

I learned that even simple scoring rules can feel convincing at first.
I also learned that small design choices can create hidden bias quickly.
The most interesting part was seeing how one song kept reappearing across different profiles.
This project made me think more carefully about input cleaning, fairness, and recommendation diversity.
