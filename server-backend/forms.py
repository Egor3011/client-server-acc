from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

import json
import aiomysql

router = APIRouter(prefix="/forms", tags=["Forms Router"])


class DriverData(BaseModel):
    agree_rules: bool
    driver_name: str = Field(..., examples=["ewrwer"])
    discord: str = Field(..., examples=["werwerew"])
    car_model: str = Field(..., examples=["Porsche 911 GT3 Cup (992)"])
    car_number: int = Field(..., examples=[911])
    experience_months: int
    rating_sa: int


# 2. Описываем общую структуру всей формы
class TournamentSubmission(BaseModel):
    data: DriverData
    submitted_at: datetime = Field(..., examples=["2026-06-10T12:21:58.283Z"])
    form_id: str = Field(..., examples=["pcup_tournament_round1"])
    steamId: str

DB_CONFIG = {
    "host": "172.19.0.1",
    "user": "admin",
    "password": "30112008mysql",
    "db": "racehub",
    "autocommit": True
}


def get_car_id(cars_dict, car_name):
    # Приводим поисковый запрос к нижнему регистру и убираем лишние пробелы
    query = car_name.strip().lower()
    
    # Ищем ID всех машин, в названии которых есть поисковый запрос
    found_ids = [car_id for car_id, name in cars_dict.items() if query in name.lower()]
    
    # Если нашли ровно одну машину, возвращаем её ID как число
    if len(found_ids) == 1:
        return found_ids[0]
    # Если нашли несколько (например, при запросе "Nissan GT-R"), возвращаем список всех ID
    elif len(found_ids) > 1:
        return found_ids
    
    # Если ничего не нашли, возвращаем None
    return None


@router.post("/pcup-round1", summary="Форм Porsche Cup ROUND 1")
async def post_pcup_round1(submission: TournamentSubmission):
    try:
        # 1. Логирование полученных данных в консоль
        print(f"Получена заявка от пилота: {submission.data.driver_name}")
        print(f"Машина: {submission.data.car_model} (№{submission.data.car_number})")

        # 2. Подготовка данных из Pydantic-модели для MySQL
        # Извлекаем вложенный объект data и переводим его в JSON-строку
        data_json_str = json.dumps(submission.data.dict(), ensure_ascii=False)
        
        # Корректно форматируем время для MySQL (без таймзон и 'Z')
        if submission.submitted_at:
            # Если submitted_at уже является объектом datetime
            if isinstance(submission.submitted_at, datetime):
                formatted_date = submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # Если это строка, очищаем её и парсим
                clean_date = str(submission.submitted_at).replace('Z', '')[:19]
                formatted_date = datetime.fromisoformat(clean_date).strftime('%Y-%m-%d %H:%M:%S')
        else:
            formatted_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # 3. Асинхронная запись в базу данных MySQL
        conn = await aiomysql.connect(**DB_CONFIG)
        try:
            async with conn.cursor() as cursor:
                sql = """
                    INSERT INTO forms (form_id, data, steamId, submitted_at)
                    VALUES (%s, %s, %s, %s)
                """
                values = (
                    submission.form_id,
                    data_json_str,
                    submission.steamId,
                    formatted_date
                )
                await cursor.execute(sql, values)
        finally:
            conn.close()

        # 4. Успешный ответ клиенту
        return {
            "status": "success",
            "message": "Заявка успешно принята и сохранена в БД",
            "processed_at": datetime.utcnow(),
            "driver": submission.data.driver_name,
        }

    except Exception as e:
        # Логируем ошибку в консоль сервера, чтобы вы видели детали
        print(f"Ошибка при обработке заявки: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


@router.post("/post", summary="Форма")
async def post_pcup_round1(submission: TournamentSubmission):
    import cfg

    try:


        submission.data.car_model = get_car_id(cfg.all_cars_id, submission.data.car_model)
        # 1. Логирование полученных данных в консоль
        print(f"Получена заявка от пилота: {submission.data.driver_name}")
        print(f"Машина: {submission.data.car_model} (№{submission.data.car_number})")

        # 2. Подготовка данных из Pydantic-модели для MySQL
        # Извлекаем вложенный объект data и переводим его в JSON-строку
        data_json_str = json.dumps(submission.data.dict(), ensure_ascii=False)
        
        # Корректно форматируем время для MySQL (без таймзон и 'Z')
        if submission.submitted_at:
            # Если submitted_at уже является объектом datetime
            if isinstance(submission.submitted_at, datetime):
                formatted_date = submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # Если это строка, очищаем её и парсим
                clean_date = str(submission.submitted_at).replace('Z', '')[:19]
                formatted_date = datetime.fromisoformat(clean_date).strftime('%Y-%m-%d %H:%M:%S')
        else:
            formatted_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # 3. Асинхронная запись в базу данных MySQL
        conn = await aiomysql.connect(**DB_CONFIG)
        try:
            async with conn.cursor() as cursor:
                sql = """
                    INSERT INTO forms (form_id, data, steamId, submitted_at)
                    VALUES (%s, %s, %s, %s)
                """
                values = (
                    submission.form_id,
                    data_json_str,
                    submission.steamId,
                    formatted_date
                )
                await cursor.execute(sql, values)
        finally:
            conn.close()

        # 4. Успешный ответ клиенту
        return {
            "status": "success",
            "message": "Заявка успешно принята и сохранена в БД",
            "processed_at": datetime.utcnow(),
            "driver": submission.data.driver_name,
        }

    except Exception as e:
        # Логируем ошибку в консоль сервера, чтобы вы видели детали
        print(f"Ошибка при обработке заявки: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )