<template>
  <section class="home-news">
    <div class="news-backdrop pattern-backdrop" />
    <div class="news-content">
      <header class="news-head">
        <h3>News RACEHUB</h3>
        <span>Latest race updates</span>
      </header>

      <div class="news-grid">
        <a
          v-for="item in news"
          :key="item.id"
          class="news-tile"
          :style="{ backgroundImage: `url(${item.image})` }"
          :href="item.href"
          target="_blank"
          rel="noopener noreferrer"
        >
          <div class="overlay">
            <p class="meta">{{ item.date }}</p>
            <h4>{{ item.title }}</h4>
          </div>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const news = [
  {
    id: 1,
    title: 'Porsche Cup: отменен и заменен на GT3-AM',
    date: '19 JUN 2026',
    href: "/gt3-am",
    image:
      'https://coachdaveacademy.com/wp-content/uploads/2023/06/iRacing-Motorsport-Simulator-Screenshot-2024.06.14-12.58.53.26-scaled.jpg',
  },
  {
    id: 2,
    title: 'Porsche Cup: обновлен регламент участия в турнире',
    date: '15 JUN 2026',
    href: "http://race-hub.ru/pdf/Reglament_PorscheCup-ROUND1.pdf",
    image:
      'https://i.pinimg.com/1200x/d7/84/78/d784789e23bd5705af81c8c0ee90a7f1.jpg',
  },
  {
    id: 3,
    title: 'ROUND 1: открыта регистрация на этап Porsche Cup',
    date: '14 JUN 2026',
    href: "http://race-hub.ru/form/pcup-round1",
    image:
      'https://i.pinimg.com/1200x/ca/b2/f0/cab2f03dbdf96ecc44af03caa3ebb535.jpg',
  },
  {
    id: 4,
    title: 'Добавлена страница с готовыми настройками машин',
    date: '11 JUN 2026',
    href: "http://race-hub.ru/setups",
    image:
      'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfhXT0l4Xz3qFuqQMmmPS27yaQQUdlKmMx8bA1Kbh2hAqEoE9vzVCMq_zF&s=10',
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
