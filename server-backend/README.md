# Server Backend (FastAPI)

## Запуск

```bash
cd server-backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Эндпоинты

- `POST /servers/register` — регистрирует IP сервера, который обратился к backend.
- `GET /servers` — возвращает список всех зарегистрированных серверов.

`server.py` при старте отправляет `POST` в URL из переменной `BACKEND_REGISTER_URL` (по умолчанию `http://127.0.0.1:8000/servers/register`).
