import json
import glob
import os

# Обновленный словарь ID машин ACC по вошему списку
CAR_MODELS = {
    0: "Porsche 991 GT3 R",
    1: "Mercedes-AMG GT3",
    2: "Ferrari 488 GT3",
    3: "Audi R8 LMS",
    4: "Lamborghini Huracan GT3",
    5: "McLaren 650S GT3",
    6: "Nissan GT-R Nismo GT3",
    7: "BMW M6 GT3",
    8: "Bentley Continental GT3",
    9: "Porsche 991II GT3 Cup",
    10: "Nissan GT-R Nismo GT3",
    11: "Bentley Continental GT3",
    12: "Aston Martin V12 Vantage GT3",
    13: "Lamborghini Gallardo R-EX",
    14: "Jaguar G3",
    15: "Lexus RC F GT3",
    16: "Lamborghini Huracan Evo",
    17: "Honda NSX GT3",
    18: "Lamborghini Huracan SF",
    19: "Audi R8 LMS Evo",
    20: "AMR V8 Vantage",
    21: "Honda NSX Evo",
    22: "McLaren 720S GT3",
    23: "Porsche 911II GT3 R",
    24: "Ferrari 488 GT3 Evo",
    25: "Mercedes-AMG GT3",
    26: "Ferrari 488 Challenge Evo",
    27: "BMW M2 CS Racing",
    28: "Porsche 911 GT3 Cup (992)",
    29: "Lamborghini Huracán SF EVO2",
    30: "BMW M4 GT3",
    31: "Audi R8 LMS GT3 evo II",
    32: "Ferrari 296 GT3",
    33: "Lamborghini Huracan Evo2",
    34: "Porsche 992 GT3 R",
    35: "McLaren 720S GT3 Evo",
    36: "Ford Mustang GT3",
    50: "Alpine A110 GT4",
    51: "AMR V8 Vantage GT4",
    52: "Audi R8 LMS GT4",
    53: "BMW M4 GT4",
    55: "Chevrolet Camaro GT4",
    56: "Ginetta G55 GT4",
    57: "KTM X-Bow GT4",
    58: "Maserati MC GT4",
    59: "McLaren 570S GT4",
    60: "Mercedes-AMG GT4",
    61: "Porsche 718 Cayman GT4",
    80: "Audi R8 LMS GT2",
    82: "KTM XBOW GT2",
    83: "Maserati MC20 GT2",
    84: "Mercedes AMG GT2",
    85: "Porsche 911 GT2 RS CS Evo",
    86: "Porsche 935"
}


def ms_to_laptime(ms):
    """Конвертирует миллисекунды в строку формата M:SS.mmm"""
    if ms == 2147483647 or ms <= 0:
        return "-"
    minutes = ms // 60000
    seconds = (ms % 60000) / 1000
    return f"{minutes}:{seconds:06.3f}"


def process_single_file(json_data, global_db):
    """Парсит файл и добавляет лучшие круги в базу данных только по трассам"""
    track = json_data.get("trackName", "unknown_track")

    # Создаем структуру для трассы, если её еще нет
    if track not in global_db:
        global_db[track] = {}

    leaderboard = json_data.get("sessionResult", {}).get("leaderBoardLines", [])

    for entry in leaderboard:
        driver = entry.get("currentDriver", {})
        player_id = driver.get("playerId")

        # Если у игрока нет ID (баг лога), пропускаем
        if not player_id:
            continue

        best_lap_ms = entry.get("timing", {}).get("bestLap", 2147483647)

        # Пропускаем, если у пилота нет валидного круга в этой сессии
        if best_lap_ms == 2147483647 or best_lap_ms <= 0:
            continue

        # Проверяем, есть ли уже этот пилот на этой трассе и улучшил ли он время
        if player_id in global_db[track]:
            if best_lap_ms >= global_db[track][player_id]["best_lap_ms"]:
                continue  # Старое время на этой трассе было лучше, пропускаем

        # Формируем имя пилота "И. Фамилия"
        first_name = driver.get("firstName", "").strip()
        last_name = driver.get("lastName", "Unknown").strip()

        if first_name:
            name_str = f"{first_name[0]}. {last_name}"
        else:
            name_str = last_name

        car_model_id = entry.get("car", {}).get("carModel", -1)
        car_name = CAR_MODELS.get(car_model_id, f"Unknown Car (ID: {car_model_id})")

        # Сохраняем во временную базу по ключу трассы
        global_db[track][player_id] = {
            "name": name_str,
            "car": car_name,
            "best_lap_ms": best_lap_ms
        }


def generate_final_report(global_db):
    """Сортирует результаты по трассам, рассчитывает gap и собирает финальный JSON"""
    final_json = {}

    for track, drivers_dict in global_db.items():
        # Сортируем всех водителей на конкретной трассе по возрастанию времени лучшего круга
        sorted_drivers = sorted(drivers_dict.values(), key=lambda x: x["best_lap_ms"])

        formatted_list = []
        leader_best_lap = None

        for index, driver_data in enumerate(sorted_drivers):
            best_lap_ms = driver_data["best_lap_ms"]
            best_lap_str = ms_to_laptime(best_lap_ms)

            if index == 0:
                leader_best_lap = best_lap_ms
                gap_str = "Leader"
            else:
                gap_ms = best_lap_ms - leader_best_lap
                gap_str = f"+{gap_ms / 1000:.3f}"

            formatted_list.append({
                "position": index + 1,
                "name": driver_data["name"],
                "car": driver_data["car"],
                "gap": gap_str,
                "best_lap": best_lap_str
            })

        final_json[track] = formatted_list

    return final_json

def generate_file(folder_path: str, output_file: str):

    global_database = {}
    processed_count = 0

    # Сканируем папку
    for file_path in glob.glob(os.path.join(folder_path, "*.json")):
        try:
            data = None
            # Пробуем UTF-16
            try:
                with open(file_path, "r", encoding="utf-16le") as f:
                    data = json.load(f)
            except (UnicodeDecodeError, json.JSONDecodeError):
                # Если не вышло — пробуем UTF-8
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

            if data is not None:
                process_single_file(data, global_database)
                processed_count += 1

        except Exception as e:
            print(f"Ошибка при обработке файла {os.path.basename(file_path)}: {e}")

    # Генерируем финальную структуру без сессий и сохраняем в один файл
    final_report = generate_final_report(global_database)

    with open(output_file, "w", encoding="utf-8") as out_f:
        json.dump(final_report, out_f, indent=4, ensure_ascii=False)

    print(f"\nУспешно обработано файлов: {processed_count}")
    print(f"Итоговый файл сохранен в: {output_file}")
