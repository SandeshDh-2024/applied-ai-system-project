# Music Recommender Simulation

## Title and Summary

**Original project name:** Music Recommender Simulation

This project started as a small, transparent music recommender built in Modules 1-3. Its original goal was to turn a user taste profile into a ranked list of songs using simple, explainable rules instead of a black-box model. In the current version, the project still focuses on content-based recommendation, but it also emphasizes evaluation, explanation, and reliability so the results are easier to trust and easier to present in a portfolio.

Why it matters: recommender systems shape what people see, hear, and explore online. A clear simulation like this is useful because it shows how ranking rules work, where bias can enter, and why testing matters even for a small AI system.

## Demo video

Watch a short walkthrough of the UI and three demo cases here:

[Watch the demo on Loom](https://www.loom.com/share/865e5a339cd346f7a3a9ea2f86e65fbb)

The video shows the High-Energy Pop, Chill Lofi, and guardrail/normalization examples you can reproduce with the Streamlit UI.

## Presentation deck

Slides for this demo are available here:

[Canva slide deck](https://canva.link/o93opeadmkbgx0p)

You can use the slide deck during your recorded walkthrough or open it for graders who prefer a slides view.

## Architecture Overview

The system is intentionally simple and easy to inspect.

```mermaid
`assets/mermaid.png`
```

The flow is: user input goes into validation, a small workflow controller checks the profile and normalizes song inputs, the recommender scores each song from `data/songs.csv`, the retriever pulls grounded evidence from the song metadata, and the CLI prints the top matches with evidence-backed explanation text. Automated tests check ranking, explanation content, normalization, retrieval, and workflow warnings, while human review confirms the output still makes sense in plain language.

## How the System Works

The core logic lives in `src/recommender.py`.

The recommender uses these song features:
- `genre`
- `mood`
- `energy`
- `tempo_bpm`
- `valence`
- `danceability`
- `acousticness`

The user profile stores:
- favorite genre
- favorite mood
- target energy
- target tempo
- target valence
- target danceability
- target acousticness
- whether the user likes acoustic music

The scoring rule is transparent:
- genre match adds points
- mood match adds points
- energy closeness adds points based on distance from the target
- acoustic preference adds a small bonus

The top songs are then sorted by total score, with tie-breaking based on energy closeness and title order.

The retrieval layer is intentionally lightweight. It does not build embeddings or use a vector database; instead, it returns grounded facts from the selected song and user profile so explanations stay faithful to the input data.

## Setup Instructions

1. Create and activate a virtual environment.

   Windows:

   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

   macOS/Linux:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Run the web app.

   ```bash
   streamlit run src/main.py
   ```

4. Optional: run the CLI demo.

   ```bash
   python src/main.py
   ```

5. Run tests.

   ```bash
   python -m pytest
   ```

## Sample Interactions

These examples were captured from the current project output.

### Example 1: High-Energy Pop

Input profile:
- genre: pop
- mood: happy
- target energy: 0.82

Top results:
1. Sunrise City, final score 5.50, reasons: genre match, mood match, energy close, less acoustic preference
2. Gym Hero, final score 4.28, reasons: genre match, energy close, less acoustic preference
3. Rooftop Lights, final score 3.38, reasons: mood match, energy close, less acoustic preference

### Example 2: Chill Lofi

Input profile:
- genre: lofi
- mood: chill
- target energy: 0.38

Top results:
1. Library Rain, final score 5.44, reasons: genre match, mood match, energy close, acoustic preference
2. Midnight Coding, final score 5.42, reasons: genre match, mood match, energy close, acoustic preference
3. Focus Flow, final score 4.46, reasons: genre match, energy close, acoustic preference

### Example 3: Deep Intense Rock

Input profile:
- genre: rock
- mood: intense
- target energy: 0.92

Top results:
1. Storm Runner, final score 5.48, reasons: genre match, mood match, energy close, less acoustic preference
2. Gym Hero, final score 3.48, reasons: mood match, energy close, less acoustic preference
3. Iron Anthem, final score 2.44, reasons: energy close, less acoustic preference

### Example 4: Guardrail Behavior (Boolean Trap)

Input profile:
- genre: rock
- mood: intense
- likes_acoustic: "False" (string, not boolean)

Observed output behavior:
1. The workflow emits warning: `likes_acoustic is not a bool`
2. Confidence is lowered from 1.00 to 0.75
3. Recommendations still return using deterministic scoring

## Design Decisions

I built this as a rule-based recommender because it is easy to explain, easy to debug, and a good fit for a small dataset. That trade-off means the system is less flexible than a learned model, but it is much more transparent for a class project and much easier to justify in a portfolio interview.

I also kept the feature set small. The code includes extra profile fields like tempo, valence, and danceability so the system looks realistic, but the current scoring logic mainly relies on genre, mood, energy, and acoustic preference. That keeps the implementation understandable while leaving room for future improvement.

## Reliability and Evaluation

I tested the project in two ways: automated checks and human review of the printed recommendations.

Automated tests now pass after the test file was updated to match the current `UserProfile` dataclass and after workflow normalization plus retrieval were added. The test command that works cleanly from the repository root is `python -m pytest`, and it confirmed that the recommender returns stable rankings, non-empty explanations, retrieval-backed evidence, and workflow warnings when needed.

Human review worked better for the current demo. The built-in profiles produced sensible top results, especially for High-Energy Pop, Chill Lofi, and Deep Intense Rock. The recommender also exposed a weakness during adversarial testing: exact string matching was fragile at first, so I added normalization to make the system more dependable.

Summary:
- `src/main.py` runs successfully and prints ranked recommendations.
- `python -m pytest` passes all 6 current tests.
- The built-in profiles produce coherent top songs.
- The system is most reliable when user inputs are clean and consistent.

Detailed reliability notes are documented in `reliability_report.md`.

## Testing Summary

What worked:
- the scoring logic produced stable rankings for the built-in profiles
- explanation strings were non-empty and matched the scoring reasons
- tie-breaking behaved consistently

What did not work:
- exact string matching creates failures for case and whitespace mismatches

What I learned:
- even small systems can break when interfaces drift
- input validation is just as important as ranking logic
- a recommendation that is explainable is easier to debug than one that is only accurate on the surface

## Reflection

This project taught me that AI systems are often a combination of logic, data, and evaluation rather than just a model. I learned how a simple recommendation rule can still produce useful results, but also how quickly bias and fragility appear when the rules are too exact or the input is not normalized. I also learned that testing is part of the AI product itself, not just a separate engineering step.

## Reflection and Ethics

The main limitation of this system is that it only understands a tiny catalog and a narrow definition of taste. It can also over-prioritize exact genre and mood labels, which means it may miss songs that a human would consider a good match. In a real product, that kind of rigidity could unfairly narrow what users discover.

Could it be misused? Yes. A recommender like this could be presented as more intelligent or more personalized than it really is. The best prevention is to keep the system transparent, label it as a simulation, show the scoring reasons, and add validation so bad inputs do not silently distort the output.

What surprised me most was how much small input formatting issues changed the results. A missing space or a different capitalization level could change whether a song matched at all.

I used AI as a collaborator during this project mainly for structuring the explanation, summarizing the architecture, and shaping the README into a portfolio-ready format. One helpful suggestion was to frame the project as a transparent, content-based recommender with explanation output, because that matched the actual code well. One flawed suggestion was to treat the project like a full RAG system; for this dataset and codebase, that would have added complexity without improving the core demo.

## Files

- `src/main.py` runs the sample profiles and prints recommendations.
- `src/workflow.py` validates input and orchestrates the recommendation flow.
- `src/recommender.py` contains the scoring logic and data classes.
- `src/retriever.py` returns grounded evidence snippets for explanations.
- `data/songs.csv` stores the song catalog.
- `tests/test_recommender.py` contains the current automated checks.
- `model_card.md` explains the model's strengths, limitations, and evaluation.
- `reliability_report.md` summarizes test coverage, guardrails, failures, and fixes.
