<template>
  <section class="home-news">
    <div class="news-backdrop pattern-backdrop" />
    <div class="news-content">
      <header class="news-head">
        <h3>News RACEHUB</h3>
        <span>Latest race updates</span>
      </header>

      <div class="news-grid">
        <article
          v-for="item in news"
          :key="item.id"
          class="news-tile"
          :style="{ backgroundImage: `url(${item.image})` }"
        >
          <div class="overlay">
            <p class="meta">{{ item.date }}</p>
            <h4>{{ item.title }}</h4>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const news = [
  {
    id: 1,
    title: 'Porsche Cup: обновлен регламент Sprint Weekend',
    date: '28 MAY 2026',
    image:
      'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&w=900&q=80',
  },
  {
    id: 2,
    title: 'Monza: открыта регистрация на этап GT3 Pro',
    date: '27 MAY 2026',
    image:
      'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=900&q=80',
  },
  {
    id: 3,
    title: 'Endurance Spa: опубликованы составы команд',
    date: '26 MAY 2026',
    image:
      'https://images.unsplash.com/photo-1471478331149-c72f17e33c73?auto=format&fit=crop&w=900&q=80',
  },
  {
    id: 4,
    title: 'Server update: ускорена синхронизация конфигов',
    date: '24 MAY 2026',
    image:
      'https://images.unsplash.com/photo-1514302240736-b1fee5985889?auto=format&fit=crop&w=900&q=80',
  },
]
</script>

<style scoped>
.home-news {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
}

.news-backdrop {
  position: absolute;
  inset: 0;
  opacity: 0.35;
}

.news-content {
  position: relative;
  z-index: 1;
  padding: 18px;
}

.news-head {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 12px;
}

.news-head h3 {
  color: #fff;
}

.news-head span {
  color: #aeb7c8;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 10px;
}

.news-tile {
  aspect-ratio: 1 / 1;
  background-size: cover;
  background-position: center;
  border: 1px solid rgba(255, 255, 255, 0.16);
  position: relative;
  filter: grayscale(1);
  transition: filter 320ms ease, transform 320ms ease;
}

.news-tile:hover {
  filter: grayscale(0);
  transform: translateY(-3px);
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(10, 11, 16, 0.1), rgba(10, 11, 16, 0.7));
  display: flex;
  flex-direction: column;
  justify-content: end;
  padding: 10px;
}

.meta {
  color: #c8ceda;
  font-size: 0.78rem;
}

h4 {
  margin-top: 6px;
  color: #fff;
  line-height: 1.2;
  font-size: 1rem;
}
</style>
