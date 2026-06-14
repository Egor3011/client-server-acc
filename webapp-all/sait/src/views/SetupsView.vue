<template>
    <div class="app-container">
      <header class="header">
        <h1>RaceHub Setups</h1>
        <p class="subtitle">Поиск готовых конфигураций автомобилей</p>
      </header>
  
      <!-- Блок фильтров -->
      <div class="search-box">
        <input 
          v-model="filters.car_model" 
          type="text" 
          placeholder="Модель авто (например, Porsche)" 
          @input="fetchSetups"
        />
        <input 
          v-model="filters.track_map" 
          type="text" 
          placeholder="Трасса (например, Monza)" 
          @input="fetchSetups"
        />
      </div>
  
      <!-- Состояния загрузки и ошибок -->
      <div v-if="loading" class="message">Загрузка сетапов...</div>
      <div v-else-if="error" class="message error">{{ error }}</div>
      <div v-else-if="setups.length === 0" class="message">Сетапы не найдены. Попробуйте изменить фильтры.</div>
  
      <!-- Список результатов -->
      <div v-else class="setups-grid">
        <div v-for="setup in setups" :key="setup.id" class="setup-card">
          <div class="card-header">
            <span class="track">{{ setup.track_map }}</span>
            <span class="time" v-if="setup.lap_time">{{ setup.lap_time }}</span>
          </div>
          
          <h3 class="car-title">{{ setup.car_model }}</h3>
          <p v-if="setup.description" class="description">{{ setup.description }}</p>
          
          <div class="card-footer">
            <div class="creator">
              <span>Автор: </span>
              <a v-if="setup.creator_url" :href="setup.creator_url" target="_blank" class="link">
                {{ setup.creator_nickname }}
              </a>
              <span v-else>{{ setup.creator_nickname }}</span>
            </div>
            
            <!-- Открытие чистого PDF в новой вкладке -->
            <a :href="setup.setup_url" target="_blank" class="btn-primary">
              Открыть PDF
            </a>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  
  // Реактивные переменные
  const setups = ref([]);
  const loading = ref(false);
  const error = ref(null);
  
  const filters = reactive({
    car_model: '',
    track_map: ''
  });
  
  // Функция запроса к бэкенду FastAPI
  const fetchSetups = async () => {
    loading.value = true;
    error.value = null;
    try {
        const url = new URL('/api/setups/search', window.location.origin);
        if (filters.car_model) url.searchParams.append('car_model', filters.car_model);
        if (filters.track_map) url.searchParams.append('track_map', filters.track_map);

        const response = await fetch(url);
        if (!response.ok) throw new Error('Ошибка сервера');
        setups.value = await response.json();
    } catch (err) {
        console.error(err);
        error.value = 'Не удалось загрузить данные с бэкенда';
    } finally {
        loading.value = false;
    }
    };
  
  // Загружаем все сетапы при первом открытии страницы
  onMounted(() => {
    fetchSetups();
  });
  </script>
  
  <style scoped>

  /* Минималистичные стили в темных тонах */
  .app-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
    font-family: "Formula1", -apple-system, Helvetica, Arial, sans-serif;
    color: #e0e0e0;
    background-color: #121212;
    min-height: 100vh;
  }
  
  .header {
    margin-bottom: 40px;
    text-align: center;
  }
  
  h1 {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -1px;
    margin: 0 0 8px 0;
    color: #ffffff;
  }
  
  .subtitle {
    color: #888;
    margin: 0;
    font-size: 1rem;
  }
  
  /* Поля ввода */
  .search-box {
    display: flex;
    gap: 16px;
    margin-bottom: 40px;
  }
  
  input {
    flex: 1;
    padding: 14px 20px;
    background-color: #1e1e1e;
    border: 1px solid #2d2d2d;
    border-radius: 8px;
    color: #fff;
    font-size: 1rem;
    transition: border-color 0.2s;
  }
  
  input:focus {
    outline: none;
    border-color: #555;
  }
  
  .message {
    text-align: center;
    color: #888;
    padding: 40px;
  }
  
  .message.error {
    color: #ff5252;
  }
  
  /* Сетка карточек: изменена с flex-column на адаптивный grid */
.setups-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr)); /* Ровно две колонки в ряд */
  gap: 16px;
}

.setup-card {
  background-color: #1e1e1e;
  border: 1px solid #2d2d2d;
  border-radius: 8px;
  padding: 24px;
  display: flex;
  flex-direction: column; /* Позволяет прижать футер к низу карточки */
  justify-content: space-between; /* Выравнивает контент, если описания разной длины */
  transition: transform 0.2s, border-color 0.2s;
}

.setup-card:hover {
  border-color: #444;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.track {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #00e676;
  font-weight: 600;
}

.time {
  font-family: "Formula1";
  background: #2d2d2d;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #fff;
}

.car-title {
  margin: 0 0 12px 0;
  font-size: 1.3rem;
  color: #fff;
}

.description {
  color: #aaa;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 20px 0;
  flex-grow: 1; /* Растягивает блок текста, удерживая футеры на одной линии */
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #2d2d2d;
  padding-top: 16px;
  font-size: 0.9rem;
  margin-top: auto; /* Жестко фиксирует футер внизу карточки */
}

.creator {
  color: #888;
}

.link {
  color: #4fc3f7;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

/* Кнопка открытия PDF */
.btn-primary {
  display: inline-block;
  background-color: #ffffff;
  color: #000000;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #e0e0e0;
}

/* Адаптивность: на смартфонах (экран меньше 768px) карточки встанут по одной в ряд */
@media (max-width: 768px) {
  .setups-grid {
    grid-template-columns: 1fr;
  }
  .search-box {
    flex-direction: column; /* Поля фильтров на мобилках тоже встанут друг под друга */
  }
}

  </style>
  