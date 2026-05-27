import asyncio
import json
import os
import subprocess
import websockets

# Сервер слушает на всех интерфейсах (0.0.0.0) на порту 8765
HOST = "0.0.0.0"
PORT = 8765

async def execute_commands(websocket):
    async for message in websocket:
        # Очистка имени файла от пробелов и переносов
        filename = message.strip()
        
        # Безопасность: запрещаем пути вроде '../../etc/passwd'
        if os.path.basename(filename) != filename:
            await websocket.send("[Ошибка] Неверное или опасное имя файла.")
            continue

        if not os.path.exists(filename):
            await websocket.send(f"[Ошибка] Файл {filename} не найден.")
            continue

        try:
            # Чтение команд из JSON
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                commands = data.get("commands", [])

            if not commands:
                await websocket.send(f"[Инфо] В файле {filename} нет команд для выполнения.")
                continue

            # Последовательное выполнение команд
            for cmd in commands:
                await websocket.send(f"[Запуск] {cmd}")
                
                # Запуск команды в подпроцессе shell
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()

                # Отправка результатов клиенту
                if stdout:
                    await websocket.send(stdout.decode('utf-8', errors='ignore'))
                if stderr:
                    await websocket.send(f"[Код ошибки: {process.returncode}] {stderr.decode('utf-8', errors='ignore')}")
                
                await websocket.send(f"[Завершено] {cmd}\n---")

        except json.JSONDecodeError:
            await websocket.send(f"[Ошибка] Ошибка чтения JSON в файле {filename}.")
        except Exception as e:
            await websocket.send(f"[Ошибка сервера] {str(e)}")

async def main():
    async with websockets.serve(execute_commands, HOST, PORT):
        print(f"WebSocket сервер запущен на ws://{HOST}:{PORT}")
        await asyncio.Future() # Работает бесконечно

if __name__ == "__main__":
    asyncio.run(main())
