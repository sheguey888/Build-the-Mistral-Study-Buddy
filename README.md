# Mistral Study Buddy

Command-line tutor built with the `mistralai` SDK (`mistral-small-latest`, temperature 0.3, max_tokens 500). It keeps the whole conversation in a `messages` list so follow-up questions work.

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # put your key from https://console.mistral.ai/api-keys
```
`.env` is git-ignored; the key never appears in the code.

## Run
```bash
python study_buddy.py
```
Type `quit` or `exit` to leave.

## Notes
- With `mistralai` 2.x the import is `from mistralai.client import Mistral` (older: `from mistralai import Mistral`).
- `python test_memory.py` checks offline that each turn resends the full history.
- Stretch goal (`--openai` endpoint) not implemented.

## Multi-turn transcript
_Paste your own transcript here after running with a real key (3+ connected questions)._
