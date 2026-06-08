from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/porsche-cup", tags=["Porsche Cup"])


# ── Модели ──────────────────────────────────────────────────────────────────

class Race(BaseModel):
    id: int
    track_number: int          # порядковый номер трассы
    track_name: str
    track_image: str           # URL / путь к картинке трассы
    date: str                  # "2025-06-19"
    time: str                  # "14:00"
    participants_count: int


class Driver(BaseModel):
    position: int              # место в рейтинге
    first_name: str
    last_name: str
    car_number: str
    total_points: int
    tracks_completed: int


class CupInfo(BaseModel):
    title: str
    date_start: str
    date_end: str
    description: str


# ── Эндпоинты ────────────────────────────────────────────────────────────────

@router.get("/info", response_model=CupInfo, summary="Общая информация о кубке")
async def get_cup_info():
    return CupInfo(
        title="Porsche Cup 2025",
        date_start="2025-06-19",
        date_end="2025-07-03",
        description=(
            "Porsche Cup — серия гонок на трассах Северной Европы. "
            "Участники соревнуются на автомобилях Porsche 911 GT3 Cup."
        ),
    )


@router.get("/races", response_model=List[Race], summary="Список предстоящих заездов")
async def get_races():
    """Возвращает список запланированных гонок."""
    return [
        Race(
            id=1,
            track_number=1,
            track_name="Monza",
            track_image="/images/tracks/anderstorp.jpg",
            date="2025-06-19",
            time="19:00",
            participants_count=18,
        ),
        Race(
            id=2,
            track_number=2,
            track_name="Spa-Francorchamps",
            track_image="/images/tracks/knutstorp.jpg",
            date="2025-06-21",
            time="19:30",
            participants_count=20,
        ),
        Race(
            id=3,
            track_number=3,
            track_name="Silverstone",
            track_image="/images/tracks/mantorp.jpg",
            date="2025-06-24",
            time="19:30",
            participants_count=17,
        ),
        Race(
            id=4,
            track_number=4,
            track_name="Nürburgring GP",
            track_image="/images/tracks/gelleransen.jpg",
            date="2025-06-26",
            time="19:00",
            participants_count=19,
        ),
        Race(
            id=5,
            track_number=5,
            track_name="Imola",
            track_image="/images/tracks/gotlands.jpg",
            date="2025-06-27",
            time="19:00",
            participants_count=21,
        ),
        Race(
            id=6,
            track_number=6,
            track_name="Barcelona",
            track_image="/images/tracks/gotlands.jpg",
            date="2025-06-28",
            time="19:00",
            participants_count=21,
        ),
        Race(
            id=7,
            track_number=7,
            track_name="Zolder",
            track_image="/images/tracks/gotlands.jpg",
            date="2025-07-03",
            time="19:00",
            participants_count=21,
        ),
        Race(
            id=8,
            track_number=8,
            track_name="Mount Panorama Circuit",
            track_image="/images/tracks/gotlands.jpg",
            date="2025-07-04",
            time="19:00",
            participants_count=21,
        ),
    ]


@router.get("/standings", response_model=List[Driver], summary="Рейтинг гонщиков")
async def get_standings():
    """Возвращает таблицу рейтинга гонщиков, отсортированную по очкам."""
    return [
        Driver(position=1, first_name="Erik",    last_name="Lindqvist",  car_number="911", total_points=87, tracks_completed=3),
        Driver(position=2, first_name="Anna",    last_name="Bergström",  car_number="23",  total_points=74, tracks_completed=3),
        Driver(position=3, first_name="Marcus",  last_name="Holm",       car_number="7",   total_points=68, tracks_completed=3),
        Driver(position=4, first_name="Sofia",   last_name="Karlsson",   car_number="44",  total_points=61, tracks_completed=2),
        Driver(position=5, first_name="Johan",   last_name="Persson",    car_number="18",  total_points=55, tracks_completed=3),
        Driver(position=6, first_name="Maja",    last_name="Nilsson",    car_number="3",   total_points=49, tracks_completed=2),
        Driver(position=7, first_name="Lukas",   last_name="Andersson",  car_number="99",  total_points=42, tracks_completed=2),
        Driver(position=8, first_name="Hanna",   last_name="Svensson",   car_number="55",  total_points=35, tracks_completed=1),
    ]