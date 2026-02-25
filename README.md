# s_hunter (MVP)

## Local run
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
python -m app.run_once
uvicorn app.main:app --reload

## Render
- Web Service: Docker
- Cron Job: `python -m app.run_once`