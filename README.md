# Hackathon2026UVMeeefj
HACKATHON

## Setup

This project calls the Google Gemini API from `Hackathon/Backend/gemini.py`.
Before running the app you must set an environment variable containing a valid
API key:

```powershell
$env:GEMINI_API_KEY="your_key_here"
# or
$env:GOOGLE_API_KEY="your_key_here"
```

The wrapper includes retry/backoff logic for `429 Too Many Requests` errors. If
you're still getting 429s you may be hitting your quota; reduce the frequency of
calls or request a higher limit from Google.

