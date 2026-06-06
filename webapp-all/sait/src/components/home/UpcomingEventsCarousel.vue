<template>
  <section class="hero-carousel">
    <div class="carousel-window">
      <div class="carousel-track" :style="trackStyle">
        <article v-for="event in events" :key="event.id" class="event-card" :style="{ backgroundImage: `linear-gradient(to right, rgba(0,0,0,1) 20%, rgba(0,0,0,0.3) 100%), url(${event.image})`}">
          <div class="event-card-content" :href="event.href">
            <p class="event-round">{{ event.round }}</p>
            <h2>{{ event.title }}</h2>
            <p class="event-meta">{{ event.date }} - {{ event.location }}</p>
            <p class="event-series">{{ event.series }}</p>
          </div>
          <div class="event-card-image">
            <img :src="event.imagemap">
          </div>
        </article>
      </div>
    </div>
    <div class="carousel-controls">
      <button class="angled-btn" @click="prevSlide">Prev</button>
      <div class="dots">
        <button
          v-for="(_, index) in events"
          :key="index"
          class="dot-btn"
          :class="{ active: index === activeSlide }"
          @click="goToSlide(index)"
        />
      </div>
      <button class="angled-btn" @click="nextSlide">Next</button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

type EventItem = {
  id: number
  image: string
  imagemap: string
  round: string
  title: string
  date: string
  location: string
  series: string
  href: string
}

const props = defineProps<{
  events: EventItem[]
}>()

const activeSlide = ref(0)
const trackStyle = computed(() => ({ transform: `translateX(-${activeSlide.value * 100}%)` }))
let carouselTimer: number | undefined

function goToSlide(index: number) {
  activeSlide.value = index
}

function nextSlide() {
  if (!props.events.length) return
  activeSlide.value = (activeSlide.value + 1) % props.events.length
}

function prevSlide() {
  if (!props.events.length) return
  activeSlide.value = (activeSlide.value - 1 + props.events.length) % props.events.length
}

onMounted(() => {
  carouselTimer = window.setInterval(nextSlide, 4500)
})

onUnmounted(() => {
  if (carouselTimer) window.clearInterval(carouselTimer)
})
</script>

<style scoped>
.hero-carousel-title {
  font-size: 1.5rem;
  color: #fff;
  margin-bottom: 12px;
}

.hero-carousel {
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(14, 16, 22, 0.7);
  padding: 14px;
  border-radius: 12px;
}

.carousel-window {
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 320ms ease;
}

.event-card {
  min-width: 100%;
  padding: 18px;
  background: rgba(18, 20, 27, 0.92);
  min-height: 180px;
  
  display: flex;
  flex-direction: row; 
  justify-content: space-between;
  align-items: center; /* Центрирует текст и карту по вертикали */
  gap: 20px; /* Отступ между текстом и картой */

  background-size: cover;     /* Растянуть фото на весь div */
  background-position: center; /* Центрировать фото */
  background-repeat: no-repeat;

  border-radius: 10px;
  box-sizing: border-box;
}

.event-card-content {
  flex: 1; /* Занимает все оставшееся место слева */
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* НОВЫЙ КЛАСС: задает размеры для блока с картой справа */
.event-card-image {
  flex-shrink: 0; /* Запрещает карте сжиматься */
  width: 100%; /* Задайте нужную вам ширину карты */
  max-width: 250px;
  height: 170px; /* Задайте нужную вам высоту карты */
}

/* НОВЫЙ КЛАСС: адаптирует изображение внутри блока */
.event-card-image img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* Сохраняет пропорции карты без обрезки */
}

.event-round {
  font-size: 0.8rem;
  color: #c5ccd8;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.event-card h2 {
  margin-top: 8px;
  color: #fff;
  font-size: 1.3rem;
}

.event-meta,
.event-series {
  margin-top: 10px;
  color: #d8dde8;
}

.carousel-controls {
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.dots {
  display: flex;
  gap: 8px;
}

.dot-btn {
  width: 10px;
  height: 10px;
  border: 1px solid;
  border-radius: 50%;
  background: transparent;
  padding: 0;
}

.dot-btn.active {
  background: #ffffff;
}

.angled-btn {
  border: 1px solid rgba(255, 255, 255, 0.28);
  background: rgba(255, 255, 255, 0.06);
  color: #eceff8;
  border-radius: 8px;
  padding: 8px 14px;
  cursor: pointer;
}
</style>
