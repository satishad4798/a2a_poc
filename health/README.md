# Health Agent

A Health information agent backed by Google Gemini.

## Disclaimer
This is an AI agent and not a substitute for professional medical advice.

## Setup

1.  Set `GOOGLE_API_KEY` in `.env`.
2.  Install dependencies:
    ```bash
    uv sync
    ```

## Run

```bash
python __main__.py
```

## Test

```bash
python test_client.py "How to improve sleep quality?"
```
