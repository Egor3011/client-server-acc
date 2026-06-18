<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Данные календаря
const calendar = ref([
  { 
    id: 1, 
    stage: 1, 
    track: 'Monza', 
    image: '/images/tracks/anderstorp.jpg', 
    date: '19.06.2025', 
    time: '19:00', 
    participants: 18, 
    format: '45 минут (1 обязательный пит-стоп)', 
    active: true 
  },
  { 
    id: 2, 
    stage: 2, 
    track: 'Spa-Francorchamps', 
    image: '/images/tracks/knutstorp.jpg', 
    date: '21.06.2025', 
    time: '19:30', 
    participants: 20, 
    format: '90 минут (Ночь, х2 износ)', 
    active: false 
  },
  { 
    id: 3, 
    stage: 3, 
    track: 'Silverstone', 
    image: '/images/tracks/mantorp.jpg', 
    date: '24.06.2025', 
    time: '19:30', 
    participants: 17, 
    format: '2 x 30 минут (Спринт, реверс)', 
    active: false 
  },
  { 
    id: 4, 
    stage: 4, 
    track: 'Nürburgring GP', 
    image: '/images/tracks/gelleransen.jpg', 
    date: '26.06.2025', 
    time: '19:00', 
    participants: 19, 
    format: '60 минут (Переменчивая погода)', 
    active: false 
  },
  { 
    id: 5, 
    stage: 5, 
    track: 'Imola', 
    image: '/images/tracks/gotlands.jpg', 
    date: '27.06.2025', 
    time: '19:00', 
    participants: 21, 
    format: '60 минут (Опасная классика)', 
    active: false 
  },
  { 
    id: 6, 
    stage: 6, 
    track: 'Barcelona', 
    image: '/images/tracks/gotlands.jpg', 
    date: '28.06.2025', 
    time: '19:00', 
    participants: 21, 
    format: '60 минут (Спринт)', 
    active: false 
  },
  { 
    id: 7, 
    stage: 7, 
    track: 'Zolder', 
    image: '/images/tracks/gotlands.jpg', 
    date: '03.07.2025', 
    time: '19:00', 
    participants: 21, 
    format: '60 минут (Стандартный формат)', 
    active: false 
  },
  { 
    id: 8, 
    stage: 8, 
    track: 'Mount Panorama Circuit', 
    image: '/images/tracks/gotlands.jpg', 
    date: '04.07.2025', 
    time: '19:00', 
    participants: 21, 
    format: '120 минут (Финал, х2 очки)', 
    active: false 
  }
])


// Расписание дня
const schedule = ref([
  { time: '19:00 – 19:15', title: 'Практика', desc: '15 минут для официальной тренировки' },
  { time: '19:15 – 19:25', title: 'Квалификация', desc: '10 минут, быстрый круг решает всё' },
  { time: '19:25 – 19:30', title: 'Перерыв', desc: '5 минут, рфинальная подготовка, заправка машин' },
  { time: '19:30', title: 'Старт гонки', desc: 'Зеленый флаг, борьба до последнего поворота' },

  { time: '20:15', title: 'Окончание гонки', desc: 'Оглашение результатов в течении 1-2 часов на сайте' },
  ])



// Переключатель вкладок в блоке правил
const activeTab = ref('stewarding')

// Жесткая и безопасная инициализация реактивного объекта таймера
const countdown = ref({
  days: 0,
  hours: '00',
  minutes: '00',
  seconds: '00'
})

let timerInterval = null

// Вспомогательная функция форматирования чисел
const formatNum = (num) => {
  return num < 10 ? '0' + num : String(num)
}

const updateCountdown = () => {
  const targetDate = new Date('2026-06-19T19:00:00+03:00').getTime() 
  const now = new Date().getTime()
  const difference = targetDate - now

  if (difference <= 0) {
    countdown.value = { days: 0, hours: '00', minutes: '00', seconds: '00' }
    if (timerInterval) clearInterval(timerInterval)
    return
  }

  const d = Math.floor(difference / (1000 * 60 * 60 * 24))
  const h = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const m = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60))
  const s = Math.floor((difference % (1000 * 60)) / 1000)

  countdown.value = {
    days: d,
    hours: formatNum(h),
    minutes: formatNum(m),
    seconds: formatNum(s)
  }
}

onMounted(() => {
  updateCountdown()
  timerInterval = setInterval(updateCountdown, 1000)
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})
</script>


<template>
  <div class="landing-page">
    
    <!-- Главный баннер (Hero) -->
    <section class="hero-section">
      <div class="container hero-container">
        
        <!-- Блок таймера обратного отсчета -->
        <div class="countdown-wrapper">
          <span class="countdown-label">До старта Сезона осталось:</span>
          <div class="countdown-tiles">
            <div class="tile"><span class="num">{{ countdown.days }}</span><span class="lbl">дн</span></div>
            <div class="tile-divider">:</div>
            <div class="tile"><span class="num">{{ countdown.hours }}</span><span class="lbl">ч</span></div>
            <div class="tile-divider">:</div>
            <div class="tile"><span class="num">{{ countdown.minutes }}</span><span class="lbl">мин</span></div>
            <div class="tile-divider">:</div>
            <div class="tile"><span class="num">{{ countdown.seconds }}</span><span class="lbl">сек</span></div>
          </div>
        </div>

        <h1 class="hero-title">
          Стань частью <br/>
          <span class="gradient-text">GT3 AM Summer</span>
        </h1>
        <p class="hero-subtitle">
          Устал от хаоса в открытых лобби? Ищешь чистую, азартную и уважительную борьбу среди пилотов своего уровня? Никаких киберспортсменов — только увлеченные любители.
        </p>
        
        <div class="quick-stats">
          <div class="stat-card">
            <span class="stat-label">Симулятор</span>
            <span class="stat-value">ACC (PC)</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Класс машин</span>
            <span class="stat-value">GT3 (Все DLC)</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Уровень</span>
            <span class="stat-value">AM / Silver</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Старт сезона</span>
            <span class="stat-value accent-text">Июнь 2026</span>
          </div>
        </div>

        <div class="hero-actions">
          <a href="http://race-hub.ru/form/gt3-am-summer" class="btn btn-primary btn-large">Регистрация на сезон</a>
          <a href="#rules" class="btn btn-secondary btn-large">Читать регламент</a>
        </div>
      </div>
    </section>

    <!-- Календарь -->
    <section id="calendar" class="container section">
      <div class="section-header">
        <span class="section-tag">Расписание этапов</span>
        <h2>Календарь сезона</h2>
      </div>
      <div class="grid-calendar">
        <div v-for="race in calendar" :key="race.stage" 
             class="card-stage"
             :class="{ 'active-stage': race.active }">
          <div class="stage-top">
            <span class="stage-num">Этап {{ race.stage }}</span>
            <span class="stage-date">{{ race.date }}</span>
          </div>
          <h3 class="stage-track">{{ race.track }}</h3>
          <p class="stage-format">{{ race.format }}</p>
          <div v-if="race.active" class="live-dot"></div>
        </div>
      </div>
    </section>

    <!-- Расписание дня -->
    <section id="schedule" class="section bg-alt">
      <div class="container">
        <div class="section-header center">
          <span class="section-tag">Тайминги (Четверг, МСК)</span>
          <h2>Расписание гоночного дня</h2>
        </div>
        <div class="timeline">
          <div v-for="(item, index) in schedule" :key="index" class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-time">{{ item.time }}</span>
              <h3 class="timeline-title">{{ item.title }}</h3>
              <p class="timeline-desc">{{ item.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Правила и Регламент -->
    <section id="rules" class="container section max-width-md">
      <div class="tabs-nav">
        <button @click="activeTab = 'realism'" :class="{ active: activeTab === 'realism' }">
          Настройки реализма
        </button>
        <button @click="activeTab = 'stewarding'" :class="{ active: activeTab === 'stewarding' }">
          Судейство и Очки
        </button>
        <button @click="activeTab = 'connection'" :class="{ active: activeTab === 'connection' }">
          Подключение
        </button>
        <button @click="activeTab = 'protection'" :class="{ active: activeTab === 'protection' }">
          Защита и Безопасность
        </button>
      </div>

      <!-- Контент вкладок -->
      <div class="tab-content">
        <div v-if="activeTab === 'requirements'">
          <h3>Требования к пилотам GT3-AM</h3>
          <ul class="rules-list">
            <li>Лицензия ACC: рейтинг безопасности <strong>SA не ниже 70</strong>.</li>
            <li>Стабильное интернет-соединение (пинг до сервера до 150 мс).</li>
            <li>Корректный профиль: Имя_Фамилия на латинице (без никнеймов).</li>
          </ul>
        </div>

        <div v-if="activeTab === 'realism'">
          <h3>Игровые настройки сервера</h3>
          <ul class="rules-list">
            <li><strong>Погода:</strong> Динамическая, на основе реального прогноза метеослужб.</li>
            <li><strong>Помощники:</strong> Только заводские (TC, ABS). Идеальная траектория отключена.</li>
            <li><strong>Камера:</strong> Только из кабины (кокпит, капот, бампер). Вид сзади запрещен.</li>
          </ul>
        </div>

        <div v-if="activeTab === 'stewarding'">
          <h3>Судейство и начисление очков</h3>
          <p class="sub-text">На чемпионате действует строгое пост-гоночное судейство по видеоповторам.</p>
          <ul class="rules-list">
            <li>Протесты подаются через форму в Discord в течение 24 часов после заезда.</li>
            <li>Система очков (Топ-15): 25, 18, 15, 12, 10, 8, 6, 4, 2, 1.</li>
            <li>Бонусы: +1 балл за Поул-позицию, +1 балл за Лучший круг в гонке.</li>
          </ul>
        </div>

        <div v-if="activeTab === 'connection'">
          <h3>Подключение на закрытый сервер</h3>
          <p class="sub-text">Доступ к серверу имеют только зарегистрированные пилоты лиги GT3-AM.</p>
          <ul class="rules-list">
            <li><strong>Поиск в ACC:</strong> Введите в строке поиска серверов тег <code>[GT3-AM]</code>.</li>
            <li><strong>Пароль:</strong> Публикуется в закрытом Discord-канале за 30 минут до старта практики.</li>
            <li><strong>Бронирование слотов:</strong> Сервер настроен по списку entry-list, зайти под чужим именем нельзя.</li>
          </ul>
        </div>

        <div v-if="activeTab === 'protection'">
          <h3>Защита и регламент безопасности</h3>
          <ul class="rules-list">
            <li><strong>Античит:</strong> На сервере активна серверная проверка валидности файлов игры.</li>
            <li><strong>Поведение на первом круге:</strong> Действует жесткий режим контроля контактов.</li>
            <li><strong>Безопасный возврат (Rejoin):</strong> Возврат на трассу после разворота только вне траектории.</li>
            <li><strong>Защита позиции:</strong> Разрешено только одно изменение траектории для защиты (смена линии).</li>
          </ul>
        </div>
      </div>

    </section>

    <!-- Философия лиги -->
    <section id="prizes" class="section bg-alt-2">
      <div class="container">
        <div class="section-header center">
          <span class="section-tag">Философия лиги</span>
          <h2>Что дает участие в чемпионате?</h2>
        </div>
        <div class="prizes-grid">
          <div class="prize-card">
            <h3>Чистый рейтинг SA</h3>
            <p>Забудь про безумные аварии в пабликах. Наше судейство мотивирует пилотов ехать аккуратно, сохраняя безопасность соперников.</p>
          </div>
          <div class="prize-card gold">
            <h3>Равный и сильный темп</h3>
            <p>Никаких профессиональных киберспортсменов со сверхъестественным временем. Твоя борьба на трассе будет плотной от старта до финального круга.</p>
          </div>
          <div class="prize-card">
            <h3>Признание в Зале Славы</h3>
            <p>Все результаты сессий, статистика обгонов и итоговая таблица лидеров сезона навсегда фиксируются в архивах нашего комьюнити.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Как принять участие (Регистрация) -->
    <section id="join" class="section join-section">
      <div class="container max-width-md center">
        <h2 class="join-title">Готов занять место на гриде?</h2>
        <p class="join-subtitle">Всего 3 простых шага отделяют тебя от участия в самом честном чемпионате любителей ACC.</p>
        
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-num">01</div>
            <h4>Войти в Discord</h4>
            <p>Основной хаб лиги. Здесь публикуются пароли, серверы и анонсы.</p>
          </div>
          <div class="step-card">
            <div class="step-num">02</div>
            <h4>Выбрать машину</h4>
            <p>Заполни анкету и зафиксируй один автомобиль класса GT3 на весь сезон.</p>
          </div>
          <div class="step-card">
            <div class="step-num">03</div>
            <h4>Хотлап тест</h4>
            <p>Проедь 5 чистых кругов на сервере в Монце для подтверждения темпа.</p>
          </div>
        </div>

        <a href="/dc" target="_blank" rel="noopener noreferrer" class="btn btn-discord">
          Присоединиться в Discord
        </a>
      </div>
    </section>

  </div>
</template>

<style setup>
/* Глобальные настройки страницы и CSS переменные */
.landing-page {
  --bg-main: none;        /* Очень темный серый, почти черный */
  --bg-card: #121215;        /* Темно-серый для карточек */
  --bg-alt: #16161a;         /* Чуть более светлый серый для контрастных блоков */
  --text-main: #ffffff;      /* Чистый белый для главных заголовков */
  --text-body: #e4e4e7;      /* Светло-серый для основного текста */
  --text-muted: #71717a;     /* Серый для второстепенного текста и подписей */
  --border-color: #27272a;   /* Серый обод в 1px для карточек и элементов */
  --border-button: #52525b;  /* Более заметный серый обод в 1px для кнопок */
  --border-hover: #a1a1aa;   /* Светло-серый обод при наведении */
  
  background-color: none;
  color: var(--text-body);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
  line-height: 1.5;
}

/* Контейнеры */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}

.max-width-md {
  max-width: 800px;
}

/* Общие стили секций */
.section {
  padding: 80px 0;
  border-bottom: 1px solid var(--border-color);
}

.bg-alt { 
  background-color: var(--bg-alt); 
}

.bg-alt-2 { 
  background-color: #0d0d11; 
}

.center { 
  text-align: center; 
}

.accent-text { 
  color: var(--text-main);
  font-weight: 700;
}

.section-header {
  margin-bottom: 40px;
}

.section-tag {
  color: var(--text-muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 600;
  display: block;
}

.section-header h2 {
  font-size: 32px;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--text-main);
  margin: 5px 0 0 0;
}

/* Кнопки с закруглением и серым ободом в 1px */
.btn {
  display: inline-block;
  padding: 12px 24px;
  border-radius: 9999px;     /* Полное закругление (капсула) */
  font-weight: 600;
  text-transform: uppercase;
  text-decoration: none;
  letter-spacing: 1px;
  font-size: 13px;
  transition: all 0.2s ease;
  cursor: pointer;
  background-color: transparent;
  color: var(--text-main);
  border: 1px solid var(--border-button);
  box-sizing: border-box;
}

.btn:hover {
  border-color: var(--border-hover);
  background-color: rgba(255, 255, 255, 0.03);
}

.btn-primary {
  background-color: var(--text-main);
  color: #000000;
  border: 1px solid var(--text-main);
}

.btn-primary:hover {
  background-color: transparent;
  color: var(--text-main);
  border-color: var(--text-main);
}

.btn-large {
  padding: 16px 36px;
  font-size: 14px;
}

.btn-discord {
  /* Кнопка Discord теперь также соответствует черно-белой гамме */
  background-color: transparent;
  color: var(--text-main);
  border: 1px solid var(--border-button);
  padding: 16px 36px;
  font-size: 14px;
}

.btn-discord:hover {
  border-color: var(--text-main);
  background-color: rgba(255, 255, 255, 0.05);
}

/* Главный баннер (Hero Секция) */
.hero-section {
  padding: 120px 0 80px 0;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
}

.hero-title {
  font-size: 56px;
  font-weight: 900;
  text-transform: uppercase;
  line-height: 1.1;
  color: var(--text-main);
  margin-bottom: 20px;
}

.gradient-text {
  /* Градиент заменен на строгое монохромное выделение */
  color: var(--text-main);
  display: block;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-muted);
  max-width: 700px;
  margin: 0 auto 50px auto;
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
  max-width: 800px;
  margin: 0 auto 50px auto;
}

.stat-card {
  background-color: var(--bg-card);
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.stat-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  display: block;
  margin-bottom: 5px;
}

.stat-value {
  font-weight: 700;
  font-size: 16px;
  color: var(--text-main);
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

/* Календарь этапов */
.grid-calendar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.card-stage {
  background-color: var(--bg-card);
  padding: 25px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  position: relative;
  transition: border-color 0.2s;
}

.card-stage:hover {
  border-color: var(--border-button);
}

.active-stage {
  border-color: var(--border-hover);
}

.stage-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.stage-num {
  background-color: var(--bg-alt);
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

.stage-date {
  font-size: 13px;
  color: var(--text-muted);
}

.stage-track {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-main);
  margin: 0 0 10px 0;
}

.stage-format {
  font-size: 14px;
  color: var(--text-muted);
  margin: 0;
}

.live-dot {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 6px;
  height: 6px;
  background-color: var(--text-main);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--text-main);
}

/* Таймлайн расписания дня */
.timeline {
  max-width: 600px;
  margin: 0 auto;
  border-left: 1px solid var(--border-color);
  padding-left: 30px;
  position: relative;
}

.timeline-item {
  position: relative;
  margin-bottom: 40px;
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -36px;
  top: 8px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--bg-main);
  border: 1px solid var(--border-button);
}

.timeline-time {
  color: var(--text-muted);
  font-weight: 600;
  font-size: 15px;
  display: block;
}

.timeline-title {
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-main);
  margin: 2px 0 8px 0;
}

.timeline-desc {
  color: var(--text-body);
  margin: 0;
  font-size: 15px;
}

/* Переключаемые вкладки регламента */
.tabs-nav {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 30px;
  overflow-x: auto;
}

.tabs-nav button {
  background: none;
  border: none;
  padding: 15px 25px;
  color: var(--text-muted);
  text-transform: uppercase;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  cursor: pointer;
  border-bottom: 1px solid transparent;
  transition: all 0.2s;
  white-space: nowrap;
}

.tabs-nav button:hover {
  color: var(--text-main);
}

.tabs-nav button.active {
  color: var(--text-main);
  border-bottom-color: var(--text-main);
}

.tab-content {
  background-color: var(--bg-card);
  padding: 30px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.tab-content h3 {
  margin-top: 0;
  font-size: 20px;
  color: var(--text-main);
}

.sub-text {
  color: var(--text-muted);
  font-size: 14px;
}

.rules-list {
  list-style: none;
  padding: 0;
  margin: 20px 0 0 0;
}

.rules-list li {
  position: relative;
  padding-left: 20px;
  margin-bottom: 12px;
  font-size: 15px;
}

.rules-list li::before {
  content: "—";
  position: absolute;
  left: 0;
  color: var(--text-muted);
}

/* Призовой фонд */
.prizes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  max-width: 900px;
  margin: 0 auto;
  align-items: stretch;
}

.prize-card {
  background-color: var(--bg-card);
  padding: 30px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.prize-emoji {
  font-size: 32px;
  margin-bottom: 10px;
  filter: grayscale(100%);   /* Перевод эмодзи в монохромный вид */
}

.prize-card h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: var(--text-main);
}

.prize-card p {
  color: var(--text-muted);
  font-size: 14px;
  margin: 0;
}

.prize-card.gold {
  border-color: var(--border-button);
  background-color: var(--bg-alt);
}

/* Секция регистрации (Вступления) */
.join-section {
  background: var(--bg-main);
}

.join-title {
  font-size: 42px;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--text-main);
  margin-bottom: 10px;
}

.join-subtitle {
  color: var(--text-muted);
  margin-bottom: 50px;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  text-align: left;
  margin-bottom: 40px;
}

.step-card {
  background-color: var(--bg-card);
  padding: 25px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.step-num {
  color: var(--text-muted);
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 10px;
}

.step-card h4 {
  margin: 0 0 5px 0;
  font-size: 16px;
  color: var(--text-main);
}

.step-card p {
  color: var(--text-muted);
  font-size: 13px;
  margin: 0;
}

/* Подвал (Footer) */
.footer {
  background-color: var(--bg-main);
  padding: 40px 0;
  text-align: center;
  font-size: 12px;
  color: var(--text-muted);
}

.footer p {
  margin: 0 0 5px 0;
}

.disclaimer {
  max-width: 600px;
  margin: 0 auto;
}

/* Адаптивность для мобильных экранов */
@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
  
  .hero-actions {
    flex-direction: column;
    padding: 0 20px;
  }
  
  .hero-actions .btn {
    width: 100%;
  }
}





/* Контейнер всего блока таймера */
.countdown-wrapper {
  margin-bottom: 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

/* Текст-подпись над цифрами */
.countdown-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #71717a; /* Серый цвет */
  font-weight: 600;
}

/* Линия, в которой лежат плитки с цифрами и двоеточия */
.countdown-tiles {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Плитка (карточка) для отдельной единицы времени */
.tile {
  display: flex;
  align-items: baseline;
  background-color: #121215;     /* Очень темный серый фон */
  border: 1px solid #27272a;     /* Тонкий серый обод 1px */
  padding: 6px 14px;
  border-radius: 8px;            /* Закругление углов */
}

/* Сама цифра внутри плитки */
.tile .num {
  font-size: 24px;
  font-weight: 800;
  font-family: monospace;        /* Моноширинный шрифт, чтобы цифры не прыгали */
  color: #ffffff;                /* Чистый белый цвет */
}

/* Короткая текстовая подпись внутри плитки (дн, ч, мин, сек) */
.tile .lbl {
  font-size: 11px;
  color: #71717a;                /* Серый цвет */
  margin-left: 4px;
}

/* Разделительные двоеточия между плитками */
.tile-divider {
  font-size: 20px;
  font-weight: 700;
  color: #52525b;                /* Темно-серый цвет */
  padding-bottom: 4px;
}

</style>