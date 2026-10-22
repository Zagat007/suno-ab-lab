# Suno A/B Lab

Open-source local blind A/B audio comparison app for AI-generated music and other audio. **Not affiliated with Suno or Anthropic.**

## Features
- 2–10 WAV, FLAC or OGG uploads (up to 60 MB each)
- Blind, randomized pairwise listening; 30-second mono previews
- Preference ranking via Elo (not a scientific quality score)
- Peak/RMS/crest/silence/duration measurements
- CSV export of results
- No API keys or paid services

## Quick start
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Tests
```bash
pytest -q
```

## Privacy and limitations
Uploads remain in the Streamlit server process memory. Run locally for sensitive files; a hosted Streamlit server receives uploaded audio. No external AI model is used in v0.1. Automatic AI analysis is planned as an optional adapter with explicit user consent. For now, results reflect only user preferences and descriptive signal statistics. This app does not automate Suno, scrape its site, or claim access to a Suno API. Check rights to any audio you upload.

## Roadmap
- [ ] Optional model-assisted qualitative analysis, separately labeled from measured audio features
- [ ] Loudness-matched listening to reduce bias
- [ ] Repeat trials and multiple listener sessions
- [ ] Pairwise confidence intervals and reproducibility reports
- [ ] Accessibility and localization

## Contributing
Issues and PRs welcome. Please include tests for changes in ranking or audio processing.
