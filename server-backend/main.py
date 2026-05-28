from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from typing import Dict
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen
import urllib.request

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


app = FastAPI(title="ACC Server Registry")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Храним сервера в памяти: ip -> время последней регистрации.
servers: Dict[str, str] = {}
steam_players_file = Path(__file__).resolve().parent / "steam_players.json"
steam_players: Dict[str, dict[str, str]] = {}

STEAM_OPENID_ENDPOINT = "https://steamcommunity.com/openid/login"


def load_steam_players() -> None:
    global steam_players
    if not steam_players_file.exists():
        steam_players = {}
        return
    try:
        import json

        content = json.loads(steam_players_file.read_text(encoding="utf-8"))
        steam_players = content if isinstance(content, dict) else {}
    except Exception:
        steam_players = {}


def save_steam_players() -> None:
    import json

    steam_players_file.write_text(
        json.dumps(steam_players, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def append_query_params(url: str, params: dict[str, str]) -> str:
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.update(params)
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            urlencode(query),
            parsed.fragment,
        )
    )


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


@app.get("/auth/steam/login")
async def steam_login(request: Request, next: str | None = None):
    next_url = next or str(request.base_url)
    
    base_callback = str(request.url_for("steam_callback"))
    if "/api/" not in base_callback and ".ru/auth/" in base_callback:
        callback_url = base_callback.replace(".ru/auth/", ".ru/api/auth/")
    else:
        callback_url = base_callback

    return_to = append_query_params(callback_url, {"next": next_url})

    realm_parsed = urlparse(next_url)
    realm = f"{realm_parsed.scheme}://{realm_parsed.netloc}"

    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": return_to,
        "openid.realm": realm,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
    }
    return RedirectResponse(url=f"{STEAM_OPENID_ENDPOINT}?{urlencode(params)}", status_code=302)


@app.get("/auth/steam/callback", name="steam_callback")
async def steam_callback(request: Request, next: str | None = None):
    query_params = dict(request.query_params)

    verify_params = {k: v for k, v in query_params.items() if k.startswith("openid.")}
    verify_params["openid.mode"] = "check_authentication"

    verify_request = urllib.request.Request(
        STEAM_OPENID_ENDPOINT,
        data=urlencode(verify_params).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        },
    )
    verify_response = urllib.request.urlopen(verify_request, timeout=8).read().decode("utf-8", errors="ignore")

    if "is_valid:true" not in verify_response:
        redirect_to = append_query_params(next or str(request.base_url), {"steam_error": "invalid_response"})
        return RedirectResponse(url=redirect_to, status_code=302)

    claimed_id = query_params.get("openid.claimed_id", "")
    steam_id = claimed_id.rstrip("/").split("/")[-1] if claimed_id else ""
    if not steam_id.isdigit():
        redirect_to = append_query_params(next or str(request.base_url), {"steam_error": "missing_steam_id"})
        return RedirectResponse(url=redirect_to, status_code=302)

    steam_players[steam_id] = {
        "steam_id": steam_id,
        "last_login_at": datetime.now(timezone.utc).isoformat(),
    }
    save_steam_players()

    redirect_to = append_query_params(next or str(request.base_url), {"steam_id": steam_id})
    return RedirectResponse(url=redirect_to, status_code=302)


@app.get("/players")
async def list_players() -> dict[str, Any]:
    return {
        "count": len(steam_players),
        "players": list(steam_players.values()),
    }


load_steam_players()
