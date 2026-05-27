import asyncio
import base64
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

import websockets

# Сервер слушает на всех интерфейсах (0.0.0.0) на порту 8765
HOST = "0.0.0.0"
PORT = 8765
BACKEND_REGISTER_URL = os.getenv("BACKEND_REGISTER_URL", "http://176.123.163.206:8000/servers/register")
CFG_DIR = Path(os.getenv("CFG_DIR", "/home/admin/acc-server/server/cfg"))


def notify_backend_server_started():
    """Сообщает backend-реестру, что текущий сервер запущен."""
    req = urllib.request.Request(
        BACKEND_REGISTER_URL,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            print(f"Backend registration: HTTP {response.status}")
    except urllib.error.URLError as exc:
        print(f"Не удалось зарегистрировать сервер в backend: {exc}")

def safe_cfg_path(filename: str) -> Path:
    if not filename:
        raise ValueError("Имя файла не указано.")
    if os.path.basename(filename) != filename:
        raise ValueError("Неверное имя файла.")
    if not filename.endswith(".json"):
        raise ValueError("Разрешены только .json файлы.")
    return CFG_DIR / filename


async def send_json(websocket, payload: dict):
    await websocket.send(json.dumps(payload, ensure_ascii=False))


async def run_command_set(websocket, command_set_name: str):
    filename = command_set_name.strip() + ".json"

    if os.path.basename(filename) != filename:
        await websocket.send("[Ошибка] Неверное или опасное имя файла.")
        return

    if not os.path.exists(filename):
        await websocket.send(f"[Ошибка] Файл {filename} не найден.")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            commands = data.get("commands", [])

        if not commands:
            await websocket.send(f"[Инфо] В файле {filename} нет команд для выполнения.")
            return

        for cmd in commands:
            await websocket.send(f"[Запуск] {cmd}")
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            if stdout:
                await websocket.send(stdout.decode("utf-8", errors="ignore"))
            if stderr:
                await websocket.send(
                    f"[Код ошибки: {process.returncode}] {stderr.decode('utf-8', errors='ignore')}"
                )

            await websocket.send(f"[Завершено] {cmd}\n---")

    except json.JSONDecodeError:
        await websocket.send(f"[Ошибка] Ошибка чтения JSON в файле {filename}.")
    except Exception as exc:
        await websocket.send(f"[Ошибка сервера] {str(exc)}")


async def handle_json_rpc(websocket, payload: dict):
    action = payload.get("action")
    request_id = payload.get("request_id")

    try:
        if action == "cfg_list":
            CFG_DIR.mkdir(parents=True, exist_ok=True)
            files = sorted(
                [file.name for file in CFG_DIR.iterdir() if file.is_file() and file.suffix == ".json"]
            )
            await send_json(
                websocket,
                {"type": "cfg_list", "request_id": request_id, "ok": True, "files": files},
            )
            return

        if action == "cfg_read":
            filename = str(payload.get("filename", "")).strip()
            path = safe_cfg_path(filename)
            if not path.exists():
                raise FileNotFoundError(f"Файл {filename} не найден.")
            raw_bytes = path.read_bytes()
            content_base64 = base64.b64encode(raw_bytes).decode("ascii")
            await send_json(
                websocket,
                {
                    "type": "cfg_read",
                    "request_id": request_id,
                    "ok": True,
                    "filename": filename,
                    "content_base64": content_base64,
                },
            )
            return

        if action == "cfg_write":
            filename = str(payload.get("filename", "")).strip()
            content_base64 = payload.get("content_base64")
            path = safe_cfg_path(filename)

            if isinstance(content_base64, str):
                raw_bytes = base64.b64decode(content_base64.encode("ascii"), validate=True)
            else:
                # Backward compatibility: старый frontend отправляет текст в поле content.
                content = payload.get("content")
                if not isinstance(content, str):
                    raise ValueError("Нужно передать content_base64 (строка) или content (строка).")
                content_encoding = str(payload.get("content_encoding", "utf-8")).lower()
                if content_encoding not in {"utf-8", "utf-16le", "utf-16be"}:
                    raise ValueError("content_encoding должен быть utf-8, utf-16le или utf-16be.")
                raw_bytes = content.encode(content_encoding)

            CFG_DIR.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw_bytes)

            await send_json(
                websocket,
                {
                    "type": "cfg_write",
                    "request_id": request_id,
                    "ok": True,
                    "filename": filename,
                    "message": "Файл сохранен.",
                },
            )
            return

        raise ValueError(f"Неизвестное действие: {action}")
    except Exception as exc:
        await send_json(
            websocket,
            {
                "type": action or "unknown",
                "request_id": request_id,
                "ok": False,
                "error": str(exc),
            },
        )


async def execute_commands(websocket):
    async for message in websocket:
        text = message.strip()
        if not text:
            continue

        try:
            payload = json.loads(text)
            if isinstance(payload, dict) and payload.get("action"):
                await handle_json_rpc(websocket, payload)
                continue
        except json.JSONDecodeError:
            pass

        # Legacy режим: plain text "start" / "stop" / "restart"
        await run_command_set(websocket, text)

async def main():
    notify_backend_server_started()
    async with websockets.serve(execute_commands, HOST, PORT):
        print(f"WebSocket сервер запущен на ws://{HOST}:{PORT}")
        await asyncio.Future() # Работает бесконечно

if __name__ == "__main__":
    asyncio.run(main())
