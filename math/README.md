# Math Agent

A Math solver agent backed by Google Gemini.

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
python test_client.py "Solve x^2 - 4 = 0"
```
