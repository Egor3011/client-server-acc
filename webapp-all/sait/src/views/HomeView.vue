<template>
  <section class="home-layout">
    <UpcomingEventsCarousel :events="upcomingEvents" />
    <CategoriesLine :categories="categories" />
    <HomeNewsSection />
    <LeaderBoard/>
    <ServersSection :servers="servers" :loading="loading" :error="error" @refresh="loadServers" />

  </section>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import CategoriesLine from '../components/home/CategoriesLine.vue'
import HomeNewsSection from '../components/home/HomeNewsSection.vue'
import ServersSection from '../components/home/ServersSection.vue'

// @ts-ignore
import LeaderBoard from '../components/home/LeaderBoard.vue'
import UpcomingEventsCarousel from '../components/home/UpcomingEventsCarousel.vue'

type ServerItem = {
  ip: string
  last_seen_at: string
}

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? '/api'
const servers = ref<ServerItem[]>([])
const loading = ref(false)
const error = ref('')

const upcomingEvents = [
  { id: 1, round: 'ROUND 1', 
  image: 'https://coachdaveacademy.com/wp-content/uploads/2023/06/iRacing-Motorsport-Simulator-Screenshot-2024.06.14-12.58.53.26-scaled.jpg',
  imagemap: 'https://racehub.s3.cloud.ru/spa-map',
  title: 'GT3 AM Summer', 
  date: '19 JUN - 4 JUL 2026', 
  location: '8 TRACKS', 
  series: 'Tournament',
  href: "http://race-hub.ru/new/gt3-am"},
  { id: 2, image: 'https://i.pinimg.com/1200x/4b/e5/5a/4be55a994de3744883a15138a217fc15.jpg',
  imagemap: 'https://racehub.s3.cloud.ru/spa-map',
   round: 'ROUND 2', title: 'Event. FASTER ON Spa', date: '7 - 13 JUN 2026', location: 'Spa-Francorchamps', series: 'Event',
   href: "" },
]

const categories = [
  { name: 'Porsche Cup', description: 'One-make sprint races', href: "/porsche-cup", is_unactive: true },
  { name: 'GT3 Pro', description: 'Top split competition', href: "/gt3-pro", is_unactive: true  },
  { name: 'GT3 AM', description: 'Gentleman drivers', href: "/gt3-am", is_unactive: false  },
  { name: 'Endurance', description: 'Multi-hour team format', href: "/endurance", is_unactive: true  },
]

let refreshTimer: number | undefined

async function loadServers() {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch(`${apiBaseUrl}/servers`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const payload = await response.json()
    servers.value = Array.isArray(payload.servers) ? payload.servers : []
  } catch (err) {
    error.value = `Не удалось загрузить сервера: ${(err as Error).message}`
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadServers()
  refreshTimer = window.setInterval(loadServers, 7000)
})

onUnmounted(() => {
  if (refreshTimer) window.clearInterval(refreshTimer)
})
</script>

<style scoped>
.home-layout {
  display: grid;
  gap: 24px;
}
</style>
