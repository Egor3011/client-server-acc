from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

import json
import aiomysql

router = APIRouter(prefix="/gt3-am", tags=["GT3-Am"])

# Схема данных для валидации
class Leader(BaseModel):
    rank: int
    username: str
    score: int
    car_number: str  # Новый гоночный номер
    car_model: str   # Новая модель авто


# Имитация базы данных (данные автоматически отсортируются по score)
db_leaders = [
    {"username": "Egor Aksenov", "score": 15, "car_number": "3", "car_model": "McLaren 720S GT3 Evo"},
    {"username": "Павел Евдокимов", "score": 12, "car_number": "86", "car_model": "McLaren 720S GT3 Evo"},
    {"username": "Meyirim Shyn", "score": 25, "car_number": "555", "car_model": "Porsche 992 GT3 R"},
    {"username": "Gleb Stat1covich", "score": 18, "car_number": "4", "car_model": "McLaren 720S GT3 Evo"},
    {"username": "Денис Голубев", "score": 10, "car_number": "13", "car_model": "Ferrari 296 GT3"},
]

@router.get("/leaders", response_model=List[Leader])
async def get_leaders():
    sorted_leaders = sorted(db_leaders, key=lambda x: x["score"], reverse=True)
    return [
        {
            "rank": i + 1, 
            "username": user["username"], 
            "score": user["score"],
            "car_number": user["car_number"], # Отдаем номер
            "car_model": user["car_model"]    # Отдаем модель
        }
        for i, user in enumerate(sorted_leaders)
    ]
