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
    "host": "127.0.0.1",
    "user": "admin",
    "password": "30112008mysql",
    "db": "racehub",
    "autocommit": True
}

@router.post("/pcup-round1", summary="Форма Porsche Cup ROUND 1")
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
                    INSERT INTO forms (form_id, data, steamId, userid, submitted_at)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                    submission.form_id,
                    data_json_str,
                    submission.steamId,
                    submission.userid,
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