<template>
    <div class="cup-page">
  
      <!-- ╔══════════════════════════════════════════════════════╗ -->
      <!-- ║  HERO — full-viewport header                        ║ -->
      <!-- ╚══════════════════════════════════════════════════════╝ -->
      <section class="hero">
        <div class="hero__bg-grid" />
        <div class="hero__noise" />
  
        <img
          src="./porsche.png"
          alt="Porsche 911 GT3 Cup"
          class="hero__car"
        />
  
        <div class="hero__text">
            <span class="hero__eyebrow">19 ИЮНЯ — 4 ИЮЛЯ 2026</span>
            <h1 class="hero__title">
                <span class="hero__title-porsche hero__text-left">PORSCHE</span>
                <span class="hero__title-cup hero__text-right">CUP</span>
            </h1>
            <p class="hero__sub">911 GT3R Cup Series (992)</p>

            <!-- НОВАЯ КНОПКА РЕГИСТРАЦИИ -->
            <button class="hero__btn" @click="navigateToRegistration">
                <span class="hero__btn-text">Регистрация на турнир</span>
                <span class="hero__btn-arrow">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
                </span>
            </button>
        </div>
      </section>
  
      <!-- ╔══════════════════════════════════════════════════════╗ -->
      <!-- ║  RACES LIST                                         ║ -->
      <!-- ╚══════════════════════════════════════════════════════╝ -->
      <a href="/pdf/Reglament_PorscheCup-ROUND1.pdf" target="_blank">Регламент турнира</a>

      <section class="section races-section">
        <h2 class="section__title">Предстоящие заезды</h2>
  
        <div v-if="racesLoading" class="loader">Загрузка…</div>
        <div v-else-if="racesError" class="error">{{ racesError }}</div>
  
        <ul v-else class="races-list">
          <li
            v-for="race in races"
            :key="race.id"
            class="race-card"
          >
            <div class="race-card__num">#{{ race.track_number }}</div>
  
            <img
              :src="race.track_image"
              class="race-card__img"
              @error="handleImgError"
            />
  
            <div class="race-card__info">
              <span class="race-card__name">{{ race.track_name }}</span>
              <span class="race-card__date">{{ formatDate(race.date) }} · {{ race.time }}</span>
            </div>
  
            <div class="race-card__participants">
              <svg class="race-card__icon" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 10a4 4 0 100-8 4 4 0 000 8zm-7 8a7 7 0 1114 0H3z"/>
              </svg>
              <span>{{ race.participants_count }}</span>
            </div>
          </li>
        </ul>
      </section>
  
      <!-- ╔══════════════════════════════════════════════════════╗ -->
      <!-- ║  STANDINGS TABLE                                    ║ -->
      <!-- ╚══════════════════════════════════════════════════════╝ -->
      <section class="section standings-section">
        <h2 class="section__title">Рейтинг гонщиков</h2>
  
        <div v-if="standingsLoading" class="loader">Загрузка…</div>
        <div v-else-if="standingsError" class="error">{{ standingsError }}</div>
  
        <div v-else class="table-wrap">
          <table class="standings-table">
            <thead>
              <tr>
                <th>№</th>
                <th>Гонщик</th>
                <th>Авто</th>
                <th>Очки</th>
                <th>Трасс</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="driver in standings"
                :key="driver.position"
                :class="{ 'standings-table__row--top': driver.position <= 3 }"
              >
                <td class="standings-table__pos">
                  <span class="pos-badge" :data-pos="driver.position">
                    {{ driver.position }}
                  </span>
                </td>
                <td class="standings-table__name">
                  {{ driver.first_name }} {{ driver.last_name }}
                </td>
                <td class="standings-table__car">#{{ driver.car_number }}</td>
                <td class="standings-table__pts">{{ driver.total_points }}</td>
                <td class="standings-table__tracks">{{ driver.tracks_completed }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
  
    </div>
  </template>
  
  <script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

// Регистрируем плагин в GSAP
gsap.registerPlugin(ScrollTrigger)

let ctx; // Контекст GSAP для безопасной очистки памяти во Vue

// ── Config ──────────────────────────────────────────────────────────────────
const API_BASE = import.meta.env.VITE_API_BASE ?? '/api'

// ── State ────────────────────────────────────────────────────────────────────
const races            = ref([])
const racesLoading     = ref(true)
const racesError       = ref(null)

const standings        = ref([])
const standingsLoading = ref(true)
const standingsError   = ref(null)


function navigateToRegistration() {
  const url = "http://race-hub.ru/form/pcup-round1"
  
  // Открывает ссылку в новой вкладке (аналог target="_blank")
  window.open(url, '_blank', 'noopener,noreferrer')
  
  // Если в будущем понадобится трекинг, код пишется прямо здесь:
  // ym(XXXXXX, 'reachGoal', 'click_reg_button')
}

// ── Fetch ────────────────────────────────────────────────────────────────────
async function fetchRaces() {
  try {
    const res = await fetch(`${API_BASE}/porsche-cup/races`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    races.value = await res.json()
  } catch (e) {
    racesError.value = 'Не удалось загрузить список заездов.'
    console.error(e)
  } finally {
    racesLoading.value = false
  }
}

async function fetchStandings() {
  try {
    const res = await fetch(`${API_BASE}/porsche-cup/standings`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    standings.value = await res.json()
  } catch (e) {
    standingsError.value = 'Не удалось загрузить рейтинг.'
    console.error(e)
  } finally {
    standingsLoading.value = false
  }
}

// ── Watchers для динамических анимаций (Каскад) ──────────────────────────────

// Следим за окончанием загрузки гонок
watch(racesLoading, async (isLoading) => {
  if (!isLoading) {
    // Ждем, пока Vue обновит DOM и отрисует карточки
    await nextTick()
    
    if (ctx) {
      ctx.add(() => {
        gsap.from('.race-card', {
          scrollTrigger: {
            trigger: '.races-section',
            start: 'top 85%',
            toggleActions: 'play none none reverse',
          },
          opacity: 0,
          y: 50,
          scale: 0.9,
          stagger: 0.15, // Теперь каскад сработает идеально
          duration: 0.8,
          ease: 'power2.out',
          onComplete: () => ScrollTrigger.refresh() // Обновляем расчеты высот скролла
        })
      })
    }
  }
})

// Следим за окончанием загрузки таблицы рейтинга
watch(standingsLoading, async (isLoading) => {
  if (!isLoading) {
    // Ждем отрисовку строк таблицы
    await nextTick()
    
    if (ctx) {
      ctx.add(() => {
        // Появление всей секции таблицы
        gsap.from('.standings-section', {
          scrollTrigger: {
            trigger: '.standings-section',
            start: 'top 80%',
            toggleActions: 'play none none reverse',
          },
          opacity: 0,
          y: 60,
          duration: 1,
          ease: 'power3.out'
        })

        // Поочередный каскад для строк таблицы
        gsap.from('.standings-table tbody tr', {
          scrollTrigger: {
            trigger: '.standings-table',
            start: 'top 80%',
          },
          opacity: 0,
          x: -20,
          stagger: 0.05, // Быстрый каскад сверху вниз
          duration: 0.5,
          ease: 'power2.out',
          delay: 0.2,
          onComplete: () => ScrollTrigger.refresh()
        })
      })
    }
  }
})

// ── Lifecycle Hooks ──────────────────────────────────────────────────────────
onMounted(() => {
  ctx = gsap.context(() => {
      
      /* ── 1. HERO АНИМАЦИЯ (Элементы статичны, анимируем сразу) ── */
      const heroTl = gsap.timeline({
        scrollTrigger: {
            trigger: '.hero',
            start: 'top top',
            end: 'bottom top',
            scrub: 1,
        }
    })

    heroTl
        .to('.hero__text-left', { x: '-150px', opacity: 0, ease: 'none' }, 0)
        .to('.hero__text-right', { x: '150px', opacity: 0, ease: 'none' }, 0)
        // ДОБАВИЛИ .hero__btn СЮДА: кнопка будет плавно улетать вверх и исчезать при скролле
        .to('.hero__eyebrow, .hero__sub, .hero__btn', { y: '-50px', opacity: 0, ease: 'none' }, 0)
        .to('.hero__car', { x: '80px', y: '40px', scale: 0.95, ease: 'none' }, 0)
  })

  // Запуск запросов к бэкенду
  fetchRaces()
  fetchStandings()
})

// ── Helpers ──────────────────────────────────────────────────────────────────
function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    day: 'numeric', month: 'long'
  })
}

function handleImgError(e) {
  e.target.src = '/images/tracks/placeholder.jpg'
}

onUnmounted(() => {
  if (ctx) ctx.revert() // Очищаем все триггеры и watchers при уходе со страницы
})
</script>

  
  
  <style scoped>
  /* ── Design tokens ──────────────────────────────────────────────────────────── */
  .cup-page {
    --c-bg:        #0a0a0c;
    --c-surface:   #111116;
    --c-border:    rgba(255,255,255,.07);
    --c-text:      #e8e8ec;
    --c-muted:     #5a5a6e;
    --c-accent:    #ffffff;     /* Porsche gold */
    --c-accent2:   #c0392b;     /* racing red */
    --c-top1:      #d1b606;
    --c-top2:      #a8b2c0;
    --c-top3:      #b87333;
  
    font-family: "Titillium Web", Arial, Helvetica, sans-serif;
    background: none;
    color: var(--c-text);
    overflow-x: hidden;
  }
  
  /* ── Google Fonts (Barlow Condensed) via @import ── */
  @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,300;0,400;0,600;0,700;0,800;1,700&display=swap');
  
  /* ══════════════════════════════════════════════════════════════════════════════
     HERO
  ══════════════════════════════════════════════════════════════════════════════ */
  .hero {
    position: relative;
    min-height: 85vh;
    display: flex;
    align-items: flex-end;
    overflow: hidden;
    background: none;
  }
  
  /* car image — bleeds right, slightly overlapping */
  .hero__car {
    position: absolute;
    right: 0%;
    bottom: -15%;
    width: 90%;
    max-width: 1000px;
    object-fit: contain;
    object-position: bottom right;
    filter: drop-shadow(-40px 0 80px rgba(212, 193, 23, 0.25));
    animation: carSlide 3s cubic-bezier(.16,1,.3,1) both;
    pointer-events: none;
  }
  
  @keyframes carSlide {
    from { transform: translateX(80px); opacity: 0; }
    to   { transform: translateX(0);    opacity: 1; }
  }
  
  /* text block — bottom-left */
  .hero__text {
    position: relative;
    z-index: 2;
    padding: 0 5vw 8vh;
    animation: textFade 2s .2s ease both;
  }
  
  @keyframes textFade {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  
  .hero__eyebrow {
    display: block;
    font-size: clamp(.7rem, 1.4vw, .95rem);
    font-weight: 600;
    letter-spacing: .22em;
    color: var(--c-accent);
    margin-bottom: .6rem;
  }
  
  .hero__title {
    margin: 0;
    line-height: .88;
    text-transform: uppercase;
  }
  
  .hero__title-porsche {
    display: block;
    font-size: clamp(4rem, 12vw, 10rem);
    font-weight: 800;
    color: var(--c-text);
    letter-spacing: -.01em;
  }
  
  .hero__title-cup {
    display: block;
    font-size: clamp(5.5rem, 17vw, 14rem);
    font-weight: 800;
    /* stroke effect */
    -webkit-text-stroke: 2px var(--c-accent);
    color: transparent;
    letter-spacing: -.02em;
  }
  
  .hero__sub {
    margin: 1.2rem 0 0;
    font-size: clamp(.9rem, 1.8vw, 1.15rem);
    font-weight: 300;
    letter-spacing: .15em;
    color: var(--c-muted);
    text-transform: uppercase;
  }
  
  /* scroll hint */
  .hero__scroll-hint {
    position: absolute;
    bottom: 2.5rem;
    right: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: .5rem;
    font-size: .65rem;
    letter-spacing: .2em;
    color: var(--c-muted);
    z-index: 3;
    animation: fadeIn 1.5s 1s ease both;
  }
  
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  
  .hero__scroll-line {
    width: 1px;
    height: 50px;
    background: linear-gradient(to bottom, var(--c-accent), transparent);
    animation: scrollPulse 1.6s ease-in-out infinite;
  }
  
  @keyframes scrollPulse {
    0%, 100% { transform: scaleY(1);   opacity: .8; }
    50%       { transform: scaleY(.5); opacity: .3; }
  }
  
  /* ══════════════════════════════════════════════════════════════════════════════
     COMMON SECTION
  ══════════════════════════════════════════════════════════════════════════════ */
  .section {
    max-width: 1100px;
    margin: 0 auto;
    padding: 6rem 5vw;
  }
  
  .section__title {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .05em;
    margin: 0 0 2.5rem;
    color: var(--c-text);
    position: relative;
    padding-left: 1.2rem;
  }
  
  .section__title::before {
    content: '';
    position: absolute;
    left: 0;
    top: 10%;
    height: 80%;
    width: 4px;
    background: var(--c-accent);
    border-radius: 2px;
  }
  
  /* ══════════════════════════════════════════════════════════════════════════════
     RACES LIST
  ══════════════════════════════════════════════════════════════════════════════ */
  .races-section {
    border-top: 1px solid var(--c-border);
  }
  
  .races-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: .75rem;
  }
  
  .race-card {
    display: grid;
    grid-template-columns: 2.5rem 90px 1fr auto;
    align-items: center;
    gap: 1.2rem;
    padding: 1rem 1.4rem;
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: 6px;
    transition: border-color .2s, transform .2s;
  }
  
  .race-card:hover {
    border-color: rgba(212,160,23,.4);
    transform: translateX(4px);
  }
  
  .race-card__num {
    font-size: 1.1rem;
    font-weight: 700;
    font-style: italic;
    color: var(--c-accent);
    letter-spacing: .03em;
  }
  
  .race-card__img {
    width: 90px;
    height: 56px;
    object-fit: cover;
    border-radius: 4px;
    background: #1c1c24;
    border: 1px solid var(--c-border);
  }
  
  .race-card__info {
    display: flex;
    flex-direction: column;
    gap: .25rem;
  }
  
  .race-card__name {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--c-text);
  }
  
  .race-card__date {
    font-size: .8rem;
    font-weight: 400;
    color: var(--c-muted);
    letter-spacing: .06em;
    text-transform: uppercase;
  }
  
  .race-card__participants {
    display: flex;
    align-items: center;
    gap: .4rem;
    font-size: .95rem;
    font-weight: 600;
    color: var(--c-muted);
    white-space: nowrap;
  }
  
  .race-card__icon {
    width: 16px;
    height: 16px;
    opacity: .6;
  }
  
  /* ══════════════════════════════════════════════════════════════════════════════
     STANDINGS TABLE
  ══════════════════════════════════════════════════════════════════════════════ */
  .standings-section {
    border-top: 1px solid var(--c-border);
  }
  
  .table-wrap {
    overflow-x: auto;
  }
  
  .standings-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 1rem;
  }
  
  .standings-table thead tr {
    border-bottom: 1px solid var(--c-border);
  }
  
  .standings-table th {
    padding: .7rem 1.2rem;
    text-align: left;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--c-muted);
  }
  
  .standings-table tbody tr {
    border-bottom: 1px solid var(--c-border);
    transition: background .15s;
  }
  
  .standings-table tbody tr:hover {
    background: rgba(255,255,255,.03);
  }
  
  .standings-table tbody tr.standings-table__row--top {
    background: rgba(212, 160, 23, .04);
  }
  
  .standings-table td {
    padding: .85rem 1.2rem;
    vertical-align: middle;
  }
  
  /* position badge */
  .pos-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    font-weight: 800;
    font-size: .9rem;
    color: #0a0a0c;
  }
  
  [data-pos="1"] { background: var(--c-top1); }
  [data-pos="2"] { background: var(--c-top2); }
  [data-pos="3"] { background: var(--c-top3); }
  [data-pos]:not([data-pos="1"]):not([data-pos="2"]):not([data-pos="3"]) {
    background: transparent;
    color: var(--c-muted);
    border: 1px solid var(--c-border);
  }
  
  .standings-table__name {
    font-weight: 600;
    color: var(--c-text);
  }
  
  .standings-table__car {
    font-weight: 700;
    color: var(--c-accent);
    letter-spacing: .05em;
  }
  
  .standings-table__pts {
    font-weight: 800;
    font-size: 1.1rem;
    color: var(--c-text);
  }
  
  .standings-table__tracks {
    color: var(--c-muted);
    font-weight: 600;
  }
  
  /* ── Utility ─────────────────────────────────────────────────────────────── */
  .loader {
    padding: 2rem;
    color: var(--c-muted);
    letter-spacing: .12em;
    font-size: .85rem;
  }
  
  .error {
    padding: 1rem 1.4rem;
    background: rgba(192, 57, 43, .12);
    border: 1px solid rgba(192, 57, 43, .3);
    border-radius: 6px;
    color: #e74c3c;
    font-size: .9rem;
  }

  .hero__text-left,
.hero__text-right {
  display: block;
  will-change: transform, opacity;
}

.hero__eyebrow,
.hero__sub,
.hero__car {
  will-change: transform, opacity;
}

/* Оптимизация для карточек и таблиц, чтобы анимация не "дёргалась" */
.race-card,
.standings-section,
.standings-table tbody tr {
  will-change: transform, opacity;
}

/* Скролл станет выглядеть аккуратнее, если убрать резкие скачки */
.section {
  overflow: hidden; /* Чтобы вылетающие элементы не ломали ширину экрана */
}

.race-card {
  display: flex; /* или block, в зависимости от вашей верстки */
  /* transition: all 0.3s; <-- ЭТУ СТРОКУ НУЖНО УДАЛИТЬ, ЕСЛИ ОНА ЕСТЬ! */
  will-change: transform, opacity; /* Оставляем только это для GPU */
}
  
  /* ── Responsive ─────────────────────────────────────────────────────────── */
  @media (max-width: 640px) {
    .hero__car    { width: 100%; right: -10%; }
    .hero__title-porsche { font-size: 3rem; }
    .hero__title-cup     { font-size: 4.5rem; }
  
    .race-card {
      grid-template-columns: 2rem 70px 1fr auto;
      gap: .8rem;
      padding: .75rem 1rem;
    }
  
    .race-card__img { width: 70px; height: 44px; }
  }

  .hero__btn {
  margin-top: 2rem;
  display: inline-flex;
  align-items: center;
  gap: 1.5rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.8rem 2rem;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-family: "Barlow Condensed", sans-serif;
  font-size: clamp(0.9rem, 1.2vw, 1.1rem);
  font-weight: 600;
  color: var(--c-text);
  transition: border-color 0.4s ease, transform 0.2s ease;
  will-change: transform, opacity;
}

/* Эффект гоночной неоновой подложки сзади кнопки */
.hero__btn::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(
    90deg, 
    transparent, 
    rgba(255, 255, 255, 0.1), 
    transparent
  );
  transition: left 0.6s ease;
}

.hero__btn-text {
  position: relative;
  z-index: 2;
}

/* Иконка стрелочки */
.hero__btn-arrow {
  display: flex;
  align-items: center;
  width: 16px;
  height: 16px;
  transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

.hero__btn-arrow svg {
  width: 100%;
  height: 100%;
}

/* ── Hover состояния ── */
.hero__btn:hover {
  border-color: var(--c-top1); /* Меняется на гоночный красный при наведении */
  background: rgba(192, 180, 43, 0.05); /* Легкий красный оттенок */
}

.hero__btn:hover::before {
  left: 100%; /* Блик пролетает слева направо */
}

.hero__btn:hover .hero__btn-arrow {
  transform: translateX(6px); /* Стрелочка динамично дергается вперед */
  color: var(--c-accent1);
}

.hero__btn:active {
  transform: scale(0.98); /* Эффект физического нажатия */
}

  </style>