# Janamitra AI — Hackathon MVP

A Telugu/English information assistant for **Andhra Pradesh NTR Bharosa old-age pension**. Built to fit a zero-cost hackathon deployment. **Not a government portal, eligibility determination, or legal advice.**

## What works
- Streamlit chatbot with Telugu (Romanized) / English answers.
- A few official-website-backed pension facts and manual citations/links.
- Optional Gemini 3.5 Flash-Lite integration (free-tier API key required), with source-constrained prompt and a non-AI FAQ fallback on quota/API errors.
- Basic browser speak-out-loud button (device/browser voice support varies).
- Local no-key demo remains functional.
- Privacy check avoids forwarding likely identity/contact/banking numbers to the external AI API.

## Important limitations
- Only *AP old-age pension* covered, not all schemes.
- No actual eligibility approval, application submission, live government-data fetching, account login, or verified real-time application status.
- Current exact application window and full document checklist have not been verified.
- Official **About** page still shows a previous pension amount. We rely on later **G.O.Ms.No.43 dated 13 June 2024** (₹4,000/month payable from July 2024) for amount. Users must verify current updates.
- Generated text can be incorrect even when supplied official facts; test and cross-check.
- Free-tier Gemini inputs may be used to improve Google products: **don't submit personal identifiers**. Never commit the API key.

## Official sources
- [AP NTR Bharosa website](https://sspensions.ap.gov.in/SSP)
- [Published criteria / About](https://sspensions.ap.gov.in/SSP/Home/About)
- [G.O.Ms.No.43, 13 June 2024](https://sspensions.ap.gov.in/SSP/Documents/GO%20MS%2043%2013.06.2024.pdf)

## Verification status

The built-in unit tests and Python syntax checks can be run without an API key. A complete Streamlit UI smoke test requires the Python dependencies; if local dependency installation is blocked, use the free Streamlit Community Cloud deployment after connecting your GitHub repository.

## Local run
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac / Linux
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL shown by Streamlit. The app works in FAQ mode without a key.

Optional AI mode, for locally testing only:
```bash
export GEMINI_API_KEY="YOUR_KEY"  # do not paste or commit your real key
streamlit run app.py
```
If you set up a Google API project, **keep billing disabled** and pick a model labelled Free Tier in Google AI Studio. A quota error should not incur a paid charge in a free-only project.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Free public deployment
1. Create a public GitHub repository named `janamitra-ai` (don't upload `.env` or secrets).
2. Commit `app.py`, `core.py`, `requirements.txt`, `.gitignore`, `tests/`, `README.md`.
3. Open https://share.streamlit.io and create an app from your GitHub repository; entry file: `app.py`.
4. Verify the public deployed URL works in a private/incognito browser window.
5. Optional: in the Streamlit app settings **Secrets** add `GEMINI_API_KEY="your-key"` (never put it into GitHub). If this is unavailable, leave FAQ mode active.
6. Put the **actual** public GitHub and deployed URLs into the hackathon submission form.

## Suggested demo questions
- What is the minimum age for old-age pension?
- How much is the old-age pension?
- Am I eligible for NTR Bharosa?
- How do I apply now? (Should transparently report unverified live window.)
- Can I give you my Aadhaar number? (Never send sensitive IDs.)

## Roadmap / possible improvements
Voice-input speech-to-text, expanded schemes, regularly reviewed rule versions, robust source-level citations and audit tests, more accessible rural channels.
