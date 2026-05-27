from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ACC Server Registry")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Храним сервера в памяти: ip -> время последней регистрации.
servers: Dict[str, str] = {}


def extract_client_ip(request: Request) -> str:
    """Возвращает реальный IP клиента."""
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # Берем первый IP из цепочки прокси.
        return forwarded_for.split(",")[0].strip()

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


@app.post("/servers/register")
async def register_server(request: Request) -> dict:
    ip = extract_client_ip(request)
    seen_at = datetime.now(timezone.utc).isoformat()
    servers[ip] = seen_at
    return {"status": "ok", "ip": ip, "seen_at": seen_at}


@app.get("/servers")
async def list_servers() -> dict:
    return {
        "count": len(servers),
        "servers": [
            {"ip": ip, "last_seen_at": last_seen_at}
            for ip, last_seen_at in servers.items()
        ],
    }
