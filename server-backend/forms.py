from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

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


@router.post("/pcup-round1", summary="Форма Porsche Cup ROUND 1")
async def post_pcup_round1(submission: TournamentSubmission):
    try:
        # Здесь ваша логика обработки, например:
        # - Сохранение в базу данных (PostgreSQL/MongoDB)
        # - Отправка уведомления в Discord-вебхук
        print(f"Получена заявка от пилота: {submission.data.driver_name}")
        print(f"Машина: {submission.data.car_model} (№{submission.data.car_number})")

        return {
            "status": "success",
            "message": "Заявка успешно принята",
            "processed_at": datetime.utcnow(),
            "driver": submission.data.driver_name,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )