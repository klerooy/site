# Artistic Shop

Интернет-магазин художественных принадлежностей на стеке `FastAPI + Vue 3`.

## Запуск в Docker (рекомендуется)

Одна команда:

```bash
docker compose up --build -d
```

Открыть сайт: `http://localhost:8080`  
API: `http://localhost:8000/api`

Альтернатива через `Makefile`:

```bash
make up
```

Остановка:

```bash
docker compose down
```

Логи:

```bash
docker compose logs -f
```

## Локальный запуск без Docker

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`  
Backend API: `http://localhost:8000/api`
