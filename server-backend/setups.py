from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List, Optional
import aiomysql

router = APIRouter(prefix="/setups", tags=["Setups Search Router"])

# 1. Схема ответа для фронтенда
class SetupResponse(BaseModel):
    id: int
    car_model: str = Field(..., examples=["Porsche 911 GT3 Cup (992)"])
    track_map: str = Field(..., examples=["Monza"])
    setup_url: str = Field(..., examples=["/files/porsche_monza.pdf"])
    lap_time: Optional[str] = Field(None, examples=["1:47.234"])
    creator_nickname: str = Field(..., default="Система", examples=["JohnDoe"])
    creator_url: Optional[str] = Field(None, examples=["https://steamcommunity.com"])
    description: Optional[str] = Field(None, examples=["Агрессивный сетап для квалификации"])

# Конфигурация подключения к БД
DB_CONFIG = {
    "host": "172.19.0.1",
    "user": "admin",
    "password": "30112008mysql",
    "db": "racehub",
    "autocommit": True
}

# 2. Эндпоинт поиска сетапов (Оптимизированный)
@router.get("/search", response_model=List[SetupResponse])
async def search_car_setups(
    car_model: Optional[str] = Query(None, description="Поиск по названию/модели автомобиля"),
    track_map: Optional[str] = Query(None, description="Поиск по названию карты/трека")
):
    # Используем прямое асинхронное подключение, чтобы не плодить пулы на каждый запрос
    conn = await aiomysql.connect(**DB_CONFIG)
    
    try:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # ВАЖНО: Добавили пустые значения для полей lap_time, creator_nickname, creator_url,
            # чтобы они соответствовали схеме SetupResponse и не вызывали ошибку валидации.
            query = """
                SELECT 
                    id, 
                    car_model, 
                    track_map, 
                    setup_url, 
                    description,
                    NULL AS lap_time,
                    'Система' AS creator_nickname,
                    NULL AS creator_url
                FROM setaps 
                WHERE 1=1
            """
            params = []
            
            # Фильтр по модели машины
            if car_model:
                query += " AND car_model LIKE %s"
                params.append(f"%{car_model}%")
                
            # Фильтр по карте/треку
            if track_map:
                query += " AND track_map LIKE %s"
                params.append(f"%{track_map}%")
                
            await cur.execute(query, params)
            rows = await cur.fetchall()
            return rows
                
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка базы данных: {str(e)}"
        )
    finally:
        # Гарантированно закрываем соединение после генерации ответа
        conn.close()
