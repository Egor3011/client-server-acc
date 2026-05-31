from fastapi import FastAPI, APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import os
import json

import results_recucle

router = APIRouter(prefix="/event")
security = HTTPBearer()

# НАСТРОЙКИ ГЛАВНОГО СЕРВЕРА
TARGET_DIR = "/app/data/results"       # Папка, куда складывать файлы для "кода №1"
LEADERBOARD_FILE = "/app/data/leaderboard.json"  # Итоговый файл, который генерирует "код №1"
SECRET_TOKEN = "test_token"

os.makedirs(TARGET_DIR, exist_ok=True)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def run_processing_script():
    """
    Здесь вызывается ваш 'Код номер один'.
    Импортируйте его функцию или запускайте как процесс.
    """
    print("Запуск обработки всех файлов...")

    # Пример, если ваш код — это функция process_data() из файла processor.py:
    results_recucle.generate_file(TARGET_DIR, LEADERBOARD_FILE)
    # process_data(TARGET_DIR, LEADERBOARD_FILE)
    pass

@router.post("/upload-result")
async def upload_result(file: UploadFile = File(...), token: None = Depends(verify_token)):
    file_path = os.path.join(TARGET_DIR, file.filename)
    
    # Сохраняем пришедший файл
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        
    # Сразу запускаем пересчет лидерборда
    run_processing_script()
    
    return {"status": "success", "message": f"Файл {file.filename} обработан"}

@router.get("/leaderboard")
async def get_leaderboard():
    # Отдаем данные из итогового JSON (не как файл, а как чистый JSON-объект)
    if not os.path.exists(LEADERBOARD_FILE):
        return [] # Возвращаем пустой список, если гонок еще не было
        
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["monza"][:150]