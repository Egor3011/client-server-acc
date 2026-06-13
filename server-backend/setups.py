from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
import aiomysql

router = APIRouter(prefix="/setups", tags=["Setups Search Router"])

# 1. Схема ответа для фронтенда (что вернет API)
class SetupResponse(BaseModel):
    id: int
    car_model: str = Field(..., examples=["Porsche 911 GT3 Cup (992)"])
    track_map: str = Field(..., examples=["Monza"])
    setup_url: str = Field(..., examples=["/files/porsche_monza.pdf"])
    lap_time: Optional[str] = Field(None, examples=["1:47.234"])
    creator_nickname: str = Field(..., examples=["JohnDoe"])
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

async def get_db_pool():
    return await aiomysql.create_pool(**DB_CONFIG)

# 2. Эндпоинт поиска сетапов
@router.get("/search", response_model=List[SetupResponse])
async def search_car_setups(
    car_model: Optional[str] = Query(None, description="Поиск по названию/модели автомобиля"),
    track_map: Optional[str] = Query(None, description="Поиск по названию карты/трека")
):
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        # DictCursor автоматически соберет строки в словари со свойствами как имена колонок в БД
        async with conn.cursor(aiomysql.DictCursor) as cur:
            
            # Базовый SQL запрос к таблице setaps
            query = "SELECT id, car_model, track_map, setup_url, description FROM setaps WHERE 1=1"
            params = []
            
            # Фильтр по модели машины (частичное совпадение LIKE)
            if car_model:
                query += " AND car_model LIKE %s"
                params.append(f"%{car_model}%")
                
            # Фильтр по карте/треку
            if track_map:
                query += " AND track_map LIKE %s"
                params.append(f"%{track_map}%")
                
            try:
                await cur.execute(query, params)
                rows = await cur.fetchall()
                
                # Возвращаем массив словарей. FastAPI автоматически провалидирует 
                # их через схему `SetupResponse` и преобразует в JSON
                return rows
                
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Ошибка базы данных: {str(e)}"
                )
            finally:
                pool.close()
                await pool.wait_closed()
