<template>
<div class="dashboard-block pattern-backdrop">
    <div class="dashboard-header-block">
        <div>
            <h2>Event: Faster on SPA</h2>
            <p>Set the fastest lap on this week and get cool prizes</p>
        </div>
        <div class="timer-container">
            <h2 id="timer">{{formattedTime}}</h2>
            <p>до конца</p>
        </div>
    </div>
      <!-- Левая часть: Трасса и Карта -->
    <div class="dashboard-main-block">
      <div class="track-section">
        <div class="track-bg"></div>
        <img src="https://racehub.s3.cloud.ru/spa-map" alt="Track Map" class="track-map" />
      </div>
  
      <!-- Правая часть: Лидерборд ACC -->
      <div class="leaderboard-section">
        <div
            class="driver-row"
            v-if="hasDriverData"
            :class="{ 'highlighted-user': medriver.steam_id === `S${currentUserSteamId}` }"
          >
            <div class="number-div">
                <span class="col-pos top-three">
                {{ medriver.position }}
                </span>
            </div>
            <div class="text-col">

                <span class="col-name">{{ medriver.name }}</span>
                <span class="col-car">{{ medriver.car }}</span>
                <span class="col-gap">
                {{ medriver.gap }}
                </span>
                <span class="col-lap">{{ medriver.best_lap }}</span>
            </div>
        </div>
        <div class="leaderboard-header">
          <span class="col-pos">#</span>
          <span class="col-name">DRIVER</span>
          <span class="col-car">CAR</span>
          <span class="col-gap">GAP</span>
          <span class="col-lap">BEST LAP</span>
        </div>
        <div class="leaderboard-list">
          <div 
            v-for="(driver, index) in leaderboard" 
            :key="driver.position" 
            class="driver-row"
            :class="{ 'highlighted-user': driver.steam_id === `S${currentUserSteamId}` }"
            :style="{ '--delay': `${index * 0.05}s` }"
            :id="driver.steam_id"
          >
            <div class="number-div">
                <span class="col-pos" :class="{ 'top-three': driver.position <= 3 }">
                {{ driver.position }}
                </span>
            </div>
            <div class="text-col">

                <span class="col-name">{{ driver.name }}</span>
                <span class="col-car">{{ driver.car }}</span>
                <span class="col-gap" :class="{ 'leader-gap': index === 0 }">
                {{ driver.gap }}
                </span>
                <span class="col-lap">{{ driver.best_lap }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
</div>
</template>
  
<script setup>
  import { ref, onMounted, computed, onUnmounted, inject } from 'vue'

  const currentUserSteamId = inject('currentUserSteamId', ref(null))

  const targetDate = new Date(2026, 5, 13, 23, 59, 59); // 10 секунд для теста
  const diff = ref(targetDate - Date.now());
  const isTimerOver = ref(false);
  let intervalId = null;

  // Форматируем строку времени (С ДНЯМИ)
  const formattedTime = computed(() => {
    if (isTimerOver.value || diff.value <= 0) return "00:00:00";

    const days = Math.floor(diff.value / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff.value % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff.value % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff.value % (1000 * 60)) / 1000);

    const timeArray = [
        String(hours).padStart(2, '0'),
        String(minutes).padStart(2, '0'),
        String(seconds).padStart(2, '0')
    ];

    // Если дни есть, добавляем их в начало строки
    if (days > 0) {
        return String(days).padStart(2, '0') + ':' + timeArray.join(':');
    }

    return timeArray.join(':');
  });

  // Обновление таймера
  const updateTimer = () => {
    const currentDiff = targetDate - Date.now();
    
    if (currentDiff <= 0) {
        diff.value = 0;
        isTimerOver.value = true;
        clearInterval(intervalId);
    } else {
        diff.value = currentDiff;
    }
  };

  onUnmounted(() => {
      if (intervalId) clearInterval(intervalId);
  });

  
  const leaderboard = ref([]);

  const medriver = ref([])


  const BACKEND_URL = '/api/event/leaderboard'

    const fetchLeaderboard = async () => {
        try {
            loading.value = true
            const response = await fetch(BACKEND_URL)
            
            if (!response.ok) {
            throw new Error('Не удалось загрузить данные с сервера')
            }
            
            // Получаем именно JSON объект, а не файл
            leaderboard.value = await response.json()
        } catch (err) {
            error.value = err.message
            console.error("Ошибка Fetch:", err)
        } finally {
            loading.value = false
        }
    }
  
    onMounted(async () => {
        console.log(currentUserSteamId.value)
        // ОБНОВЛЕНО: Изменили интервал на 1000мс (1 секунда), так как МС больше нет
        intervalId = setInterval(updateTimer, 1000);

        const params = new URLSearchParams({
            steam_id: currentUserSteamId.value // передаем наш ID
            // сюда можно добавить еще параметры, например: limit: 10
        })
        
        try {
        const response = await fetch(BACKEND_URL) 

        const medriver_res = await fetch(`/api/event/myposition?${params.toString()}`)

        console.log(`/api/event/myposition?${params.toString()}`)
        if (response.ok) {
            leaderboard.value = await response.json()
        }
        if (medriver_res != null) {
            medriver.value = await medriver_res.json()
        }
        } catch (error) {
        console.error('Ошибка загрузки лидерборда:', error)
        }
    })

    const hasDriverData = computed(() => {
        return medriver.value && Object.keys(medriver.value).length > 0;
    });
  </script>
  
  <style scoped>

    #timer {
        transition: color 0.2s ease;
    }
    #timer.finished {
        color: #ff3333;
        text-shadow: 0 0 10px rgba(255, 51, 51, 0.6);
    }


    .driver-row.highlighted-user {
        background: rgba(255, 215, 0, 0.15); /* Золотистый полупрозрачный фон */
        border-left: 4px solid #ffd700;       /* Акцентная линия слева */
        box-shadow: inset 0 0 10px rgba(255, 215, 0, 0.1);
    }

    /* Опционально: можно сделать имя текущего пользователя ярче */
    .driver-row.highlighted-user .col-name {
        color: #ffd700;
        text-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
    }

  /* Главный контейнер */
  .dashboard-block {
    
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 12px 0;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  }

  .dashboard-main-block {
    display: flex;
    width: 100%;
    max-width: 1200px;
    height: 500px;
    overflow: hidden;
  }
  
  .dashboard-header-block {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    
  }

  /* Левая секция (Трасса) */
  .track-section {
    position: relative;
    width: 40%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    box-sizing: border-box;
  }
  
  /* Затемненный фон на 40% (rgba 0.4) */
  .track-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    clip-path: polygon(
        20px 0,                       /* Срез верхнего левого */
        100% 0,                       /* Верхний правый (острый) */
        100% calc(100% - 20px),       /* Начало среза нижнего правого */
        calc(100% - 20px) 100%,       /* Конец среза нижнего правого */
        0 100%,                       /* Нижний левый (острый) */
        0 20px                        /* Возврат к срезу верхнего левого */
        );

    background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)), 
                      url('https://i.pinimg.com/1200x/d7/84/78/d784789e23bd5705af81c8c0ee90a7f1.jpg');
    background-size: cover;
    background-position: center;
    z-index: 1;
  }
  
  /* Карта поверх фона (Максимальный размер без деформации и выхода за рамки) */
  .track-map {
    position: relative;
    z-index: 2;
    width: 70%;
    height: 70%;
    object-fit: contain; /* Увеличивает карту по максимуму, сохраняя пропорции */
    pointer-events: none;
  }
  
  /* Правая секция (Лидерборд) */
  .leaderboard-section {
    width: 60%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 5px 15px;
    box-sizing: border-box;
    scrollbar-gutter: stable; 
    overflow-x: hidden;
  }
  
  /* Шапка таблицы */
  .leaderboard-header {
    display: flex;
    padding: 10px;
    padding-top: 0;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
    font-family: Formula1;
    color: #64748b;
    border-bottom: 1px solid #232730;
    text-transform: uppercase;
  }
  
  /* Сетка колонок в стиле симуляторов */
  .col-pos { 
    width: 80px; text-align: center; 
    font-family: Formula1;
    font-size: 16px;
    }
  .col-name { 
    flex: 2; padding-left: 10px;
    font-weight: 700;
    font-family: Formula1;
    }
  .col-car { flex: 1.5; color: #94a3b8; }
  .col-gap { width: 90px; text-align: right; }
  .col-lap { width: 100px; text-align: right; }
  
  /* Список */
  .leaderboard-list {
    flex: 1;
    overflow-y: auto;
    margin-top: 5px;
  }

  .number-div {
    display: flex;
    align-items: center;
    padding: 0;
    height: 51px;
    border-radius: 20px 0;
    width: 80px;
    
    border-right: 1px solid rgba(255, 255, 255, 0.16);
  }

  .text-col {
    display: flex;
    align-items: center;
    padding: 12px 10px;
    width: 100%;
    margin-bottom: 4px;
    }
  
  /* Строка гонщика */
  .driver-row {
    display: flex;
    align-items: center;
    padding: 0px;
    margin-bottom: 4px;
    background-color: rgba(17, 19, 25, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.16);
    color: #e2e8f0;
    font-size: 14px;

    border-radius: 20px 0;
    
    /* Анимация появления */
    opacity: 0;
    transform: translateX(-30px);
    animation: slideIn 0.5s ease-out forwards;
    animation-delay: var(--delay);

    transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;

  }
  
  /* Стили элементов ACC */
  .driver-row:hover {

    background-color: #222933;
  }

  .driver-row:hover .number-div {
    background: rgba(141, 13, 13, 0.96);
  }
  
  .top-three {
    color: #ffffff; /* Выделение топ-3 */
    font-weight: bold;
  }
  
  .leader-gap {
    color: #10b981;
    font-weight: bold;
  }
  .timer-container{
    text-align: center;
    }
  /* Анимация выезда слева из прозрачности */
  @keyframes slideIn {
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  </style>
  