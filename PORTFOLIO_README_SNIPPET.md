Music Recommender — Portfolio README snippet

Title: Music Recommender Simulation

One-line summary:
A transparent content-based music recommender with retrieval-grounded explanations and workflow guardrails.

Run (local):

```bash
python -m pytest tests/test_recommender.py
streamlit run src/main.py
```

Quick demo cases to show in the UI:
- High-Energy Pop (preset): genre=pop, mood=happy, energy≈0.82, acoustic=False — expect high-confidence matches.
- Chill Lofi (preset): genre=lofi, mood=chill, acoustic=True — expect acoustic, low-energy matches.
- Guardrail / normalization: edit genre/mood to include extra spaces (e.g., " Pop ") and generate — expect normalization and a warning.

What this repo demonstrates (short):
- Deterministic scoring in `src/recommender.py` for reproducibility.
- Lightweight evidence retrieval in `src/retriever.py` for grounded explanations (RAG-style, no embedding DB).
- A workflow controller in `src/workflow.py` that validates inputs, converts dataclasses, and packages results with warnings and a confidence score.
- A Streamlit UI in `src/main.py` for reproducible, graded demos.

Reflection (short):
This project shows I can design and ship reliable, explainable AI features: I balanced deterministic ranking with retrieval for explanations, added input guardrails and tests for robustness, and built a user-facing demo for inspection and grading.

Docs & evaluation:
- See `model_card.md` for strengths and limitations.
- See `reliability_report.md` for test coverage and known issues.

Contact:
- Add your GitHub repo URL here after pushing so graders can access the project.
