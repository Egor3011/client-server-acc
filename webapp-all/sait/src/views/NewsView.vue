<template>
  <section class="news-layout">
    <header class="news-hero">
      <p class="eyebrow">ACC Racing Newsroom</p>
      <h1>Новости и обновления чемпионата</h1>
      <p>
        Анонсы этапов, результаты Porsche Cup, апдейты правил и технические новости по серверам.
      </p>
    </header>

    <div class="news-grid">
      <article v-for="item in news" :key="item.id" class="news-card">
        <p class="meta">{{ item.date }} • {{ item.category }}</p>
        <h3>{{ item.title }}</h3>
        <p>{{ item.excerpt }}</p>
        <a href="#" @click.prevent>Read more</a>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
const news = [
  {
    id: 1,
    date: '27 MAY 2026',
    category: 'Porsche Cup',
    title: 'Monza sprint weekend расписан на три заезда',
    excerpt: 'Обновлен формат этапа: квалификация + 2 спринта + суперфинал с реверсом топ-10.',
  },
  {
    id: 2,
    date: '25 MAY 2026',
    category: 'Server Update',
    title: 'Новая система live-конфигов внедрена на боевых инстансах',
    excerpt: 'Теперь JSON-конфиги применяются в реальном времени из панели управления без ручного деплоя.',
  },
  {
    id: 3,
    date: '22 MAY 2026',
    category: 'Endurance',
    title: 'Открыта регистрация на 3-часовую гонку в Spa',
    excerpt: 'Прием заявок до пятницы. Для участия нужны 2 пилота и стабильный рейтинг безопасности.',
  },
  {
    id: 4,
    date: '20 MAY 2026',
    category: 'Rules',
    title: 'Обновлены правила pit-window и штрафов за лимиты трассы',
    excerpt: 'Новый регламент вступает в силу с этапа Barcelona-Catalunya.',
  },
]
</script>

<style scoped>
.news-layout {
  display: grid;
  gap: 20px;
}

.news-hero {
  padding: 22px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(15, 17, 23, 0.9);
  border-radius: 12px;
}

.eyebrow {
  color: #b9c1ce;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-size: 0.8rem;
}

h1 {
  margin-top: 8px;
  color: #fff;
  font-size: clamp(1.8rem, 4vw, 2.8rem);
}

.news-hero p {
  margin-top: 10px;
  color: #d7dce7;
  max-width: 760px;
}

.news-grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}

.news-card {
  border: 1px solid rgba(255, 255, 255, 0.14);
  padding: 16px;
  background: rgba(8, 10, 16, 0.84);
  border-radius: 0 12px 0 12px;
}

.meta {
  color: #9ca6ba;
  font-size: 0.82rem;
}

h3 {
  margin-top: 8px;
  color: #f9fbff;
}

.news-card p {
  margin-top: 8px;
  color: #c0c8d6;
}

a {
  display: inline-block;
  margin-top: 12px;
  color: #d7deea;
  text-decoration: none;
  border-bottom: 1px solid rgba(215, 222, 234, 0.55);
}
</style>
