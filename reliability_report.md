# Reliability Report: Music Recommender Simulation

## Scope

This report summarizes how reliability is checked in the current version of the recommender (deterministic ranker + retrieval-backed explanations + workflow guardrails).

## Test Command

```bash
python -m pytest tests/test_recommender.py
```

Latest result: **6/6 tests passed**.

## What Is Tested

1. Ranking behavior is deterministic for a fixed profile.
2. Explanations are returned and non-empty.
3. Explanation text includes key grounded score reasons.
4. Boolean guardrail blocks accidental truthiness from string values like "False".
5. Input normalization handles case/whitespace for genre and mood.
6. Workflow warnings and confidence adjustments trigger for invalid boolean input.

## Guardrails Implemented

1. Input validation in `src/workflow.py`:
   - numeric range checks for energy
   - boolean type check for `likes_acoustic`
   - whitespace warnings for text inputs
2. Normalization in `src/recommender.py`:
   - trims and lowercases genre/mood before matching
3. Safe boolean handling:
   - only real `True` is treated as acoustic preference
4. Confidence signal:
   - confidence drops when warnings are present

## Known Failure Patterns and Fixes

1. **Problem:** Deployed UI showed blank/black page.
   **Cause:** Entry point was console-oriented and rendered no Streamlit UI elements.
   **Fix:** Converted `src/main.py` to render a Streamlit app page with controls and result panels.

2. **Problem:** CSV load failures when app launched from different working directories.
   **Cause:** Relative path `data/songs.csv` depended on launch location.
   **Fix:** Resolved path from `__file__` in `src/main.py`.

3. **Problem:** Boolean trap (`"False"`) could behave unexpectedly.
   **Cause:** Python truthiness can treat non-empty strings as true.
   **Fix:** Guardrail now accepts only actual boolean `True` as acoustic preference.

## Human Evaluation Notes

1. Baseline profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) return coherent top songs.
2. Adversarial profiles trigger warnings as expected while still returning deterministic recommendations.
3. Retrieval-backed explanation snippets stay grounded in song metadata.

## Next Reliability Improvements

1. Add regression snapshots for top-3 outputs on fixed profiles.
2. Add tests for unknown label fallback behavior.
3. Add stricter output-format guardrails for explanation length and phrasing.