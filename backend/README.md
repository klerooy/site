# Backend (FastAPI)

## Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API base: `http://localhost:8000/api`

## Docker image

```bash
docker build -t artistic-backend ./backend
```
