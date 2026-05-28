<template>
  <section class="hero-carousel">
    <div class="carousel-window">
      <div class="carousel-track" :style="trackStyle">
        <article v-for="event in events" :key="event.id" class="event-card">
          <p class="event-round">{{ event.round }}</p>
          <h2>{{ event.title }}</h2>
          <p class="event-meta">{{ event.date }} - {{ event.location }}</p>
          <p class="event-series">{{ event.series }}</p>
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
  round: string
  title: string
  date: string
  location: string
  series: string
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
  border: 1px solid rgba(255, 255, 255, 0.16);
  min-height: 180px;
  border-radius: 10px;
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
