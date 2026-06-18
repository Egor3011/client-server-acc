<template>
    <div class="yt-profile-container">
      <!-- Узкий постер сверху -->
      <div class="yt-banner-wrapper">
        <div class="yt-banner-section">
          <img :src="driver.posterUrl" alt="Баннер" class="yt-banner-image" />
        </div>
      </div>
  
      <!-- Шапка профиля -->
      <div class="yt-content-section">
        <div class="yt-profile-header">
          <div class="yt-avatar-container">
            <img :src="driver.avatarUrl" :alt="driver.firstName" class="yt-avatar-image" />
          </div>
  
          <div class="yt-info-wrapper">
            <div class="yt-text-block">
              <!-- Изменено: обертка для имени и рейтинга в одну строку -->
              <div class="name-rating-row">
                <h1 class="yt-driver-name">{{ driver.firstName }} {{ driver.lastName }}</h1>
                
                <!-- Изменено: виджет рейтинга перенесен сюда со стрелкой тренда -->
                <div class="yt-rating-badge-inline">
                  <span class="yt-rating-num">{{ driver.rating }}</span>
                  <div class="f1-trend" :class="trendClass">
                    <span>{{ trendArrow }}</span>
                    <span>{{ Math.abs(ratingDiff) }}</span>
                  </div>
                </div>
              </div>
              <p class="yt-driver-category">Профессиональный гонщик / Пилот</p>
            </div>
            <!-- Удалено: старый блок yt-rating-badge справа -->
          </div>
        </div>
  
        <!-- ОБНОВЛЕННЫЙ ДАШБОРД -->
        <div class="profile-dashboard-layout">
          
          <!-- Первая строчка: График (70%) и Информация (30%) -->
          <div class="dashboard-row">
            <DriverRatingChart class="block-70" />
            <DriverInfo class="block-30" />
          </div>
  
          <!-- Нижние блоки на всю ширину -->
          <DriverSetups />
          <DriverHistory />
          
        </div>
  
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'; // Изменено: добавлен computed
  import DriverRatingChart from '../components/user/DriverRatingChart.vue';
  import DriverInfo from '../components/user/DriverInfo.vue';
  import DriverSetups from '../components/user/DriverSetups.vue';
  import DriverHistory from '../components/user/DriverHistory.vue';
  
  const driver = ref({
    firstName: 'Egor',
    lastName: 'Aksenov',
    rating: 94,          // Изменено: тип данных теперь число для математических операций
    previousRating: 91,  // Изменено: добавлено поле для сравнения со старым рейтингом
    avatarUrl: 'https://unsplash.com',
    posterUrl: 'https://unsplash.com'
  });

  // Изменено: добавлены три вычисляемые функции для стрелки
  const ratingDiff = computed(() => driver.value.rating - driver.value.previousRating);

  const trendClass = computed(() => {
    if (ratingDiff.value > 0) return 'trend-up';
    if (ratingDiff.value < 0) return 'trend-down';
    return 'trend-neutral';
  });

  const trendArrow = computed(() => {
    if (ratingDiff.value > 0) return '▲';
    if (ratingDiff.value < 0) return '▼';
    return '•';
  });
  </script>
  
  <style>
  /* ОБЩИЕ ГЛОБАЛЬНЫЕ СТИЛИ */
  .yt-profile-container {
    font-family: 'Titillium Web', sans-serif;
    background-color: none;
    min-height: 100vh;
    color: #e1e1e1;
    padding-top: 24px;
    padding-bottom: 60px;
  }
  
  .block-title, 
  .yt-driver-name, 
  .yt-rating-num,
  .important-text {
    font-family: 'Formula1', 'Titillium Web', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
  }
  
  .profile-block {
    
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    box-sizing: border-box;
  }
  
  .block-title {
    font-size: 1.25rem;
    color: #ffffff;
    margin: 0 0 20px 0;
    letter-spacing: 0.5px;
    border-left: 4px solid #ffffff;
    padding-left: 10px;
  }
  
  /* ОБНОВЛЕННАЯ СТРУКТУРА СЕТКИ ДАШБОРДА */
  .profile-dashboard-layout {
    display: flex;
    flex-direction: column;
    gap: 24px; /* Вертикальный отступ между строками */
    margin-top: 40px;
  }
  
  /* Контейнер для первой строчки */
  .dashboard-row {
    display: flex;
    gap: 24px; /* Горизонтальный разрыв между blocks */
    width: 100%;
  }
  
  /* Пропорции 70% на 30% с учетом отступа gap */
  .block-70 {
    width: calc(70% - 12px);
    flex-shrink: 0;
  }
  
  .block-30 {
    width: calc(30% - 12px);
    flex-grow: 1;
  }
  
  /* Стили шапки */
  .yt-banner-wrapper { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
  .yt-banner-section { position: relative; width: 100%; height: 200px; overflow: hidden; background-color: #212121; border: 2px solid #3f3f3f; border-radius: 16px; }
  .yt-banner-image { width: 100%; height: 100%; object-fit: cover; }
  .yt-content-section { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
  .yt-profile-header { display: flex; position: relative; align-items: flex-start; padding: 0 16px; }
  .yt-avatar-container { width: 140px; height: 140px; border-radius: 50%; overflow: hidden; margin-top: -70px; border: 4px solid #0f0f0f; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5); background-color: #212121; flex-shrink: 0; z-index: 10; }
  .yt-avatar-image { width: 100%; height: 100%; object-fit: cover; }
  .yt-info-wrapper { display: flex; justify-content: space-between; align-items: center; flex-grow: 1; margin-left: 24px; padding-top: 16px; }
  .yt-driver-name { font-size: 2.2rem; color: #ffffff; margin: 0; }
  .yt-driver-category { font-size: 0.95rem; margin: 4px 0 0 0; color: #aaaaaa; }

  /* Изменено: Новые стили позиционирования строки имени и рейтинга */
  .name-rating-row {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .yt-rating-badge-inline {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #212121;
    border: 1px solid #3f3f3f;
    padding: 4px 12px;
    border-radius: 6px;
  }

  .f1-trend {
    display: flex;
    align-items: center;
    gap: 2px;
    font-size: 0.9rem;
    font-weight: bold;
  }

  /* Изменено: Цветовые классы для стрелки */
  .trend-up { color: #10b981; }
  .trend-down { color: #ff3333; }
  .trend-neutral { color: #64748b; }
  
  .yt-rating-num { font-size: 1.4rem; color: #ffffff; }
  
  /* Адаптивность для планшетов и мобильных устройств */
  @media (max-width: 992px) {
    .dashboard-row {
      flex-direction: column; /* На маленьких экранах выстраиваем 1 и 2 блоки друг под друга */
    }
    
    .block-70, .block-30 {
      width: 100%;
    }
  
    .yt-profile-header { flex-direction: column; align-items: center; text-align: center; padding: 0; }
    .yt-avatar-container { margin-top: -60px; }
    .yt-info-wrapper { flex-direction: column; margin-left: 0; gap: 16px; }
    .name-rating-row { justify-content: center; } /* Изменено: центрирование строки на мобильных */
  }
  </style>
