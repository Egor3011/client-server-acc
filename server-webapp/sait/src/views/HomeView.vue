<template>
  <section class="servers-page">
    <div class="page-header">
      <h1>Доступные серверы</h1>
      <button class="refresh" :disabled="loading" @click="loadServers">
        {{ loading ? 'Обновление...' : 'Обновить' }}
      </button>
    </div>

    <p class="hint">Список обновляется каждые 5 секунд</p>
    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="servers.length" class="servers-grid">
      <router-link
        v-for="server in servers"
        :key="server.ip"
        class="server-card"
        :to="{ name: 'server-details', params: { ip: server.ip } }"
      >
        <span class="server-ip">{{ server.ip }}</span>
        <span class="server-time">last seen: {{ formatTime(server.last_seen_at) }}</span>
      </router-link>
    </div>

    <div v-else-if="!loading" class="empty-state">Пока нет зарегистрированных серверов</div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

type ServerItem = {
  ip: string
  last_seen_at: string
}

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? '/api'

const servers = ref<ServerItem[]>([])
const loading = ref(false)
const error = ref('')

let refreshTimer: number | undefined

function formatTime(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}

async function loadServers() {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch(`${apiBaseUrl}/servers`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    const payload = await response.json()
    servers.value = Array.isArray(payload.servers) ? payload.servers : []
  } catch (err) {
    error.value = `Не удалось получить список серверов: ${(err as Error).message}`
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadServers()
  refreshTimer = window.setInterval(loadServers, 5000)
})

onUnmounted(() => {
  if (refreshTimer) {
    window.clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.servers-page {
  display: grid;
  gap: 10px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

h1 {
  color: #f8fafc;
  font-size: clamp(1.5rem, 3vw, 2rem);
}

.hint {
  color: #94a3b8;
}

.error {
  color: #fca5a5;
}

.refresh {
  border: 1px solid #334155;
  background: #111827;
  color: #e2e8f0;
  padding: 8px 14px;
  border-radius: 10px;
  cursor: pointer;
}

.refresh:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.servers-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.server-card {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border: 1px solid #334155;
  border-radius: 14px;
  padding: 14px;
  text-decoration: none;
  display: grid;
  gap: 8px;
  transition: transform 0.15s ease, border-color 0.15s ease;
}

.server-card:hover {
  transform: translateY(-2px);
  border-color: #38bdf8;
}

.server-ip {
  color: #e2e8f0;
  font-weight: 700;
}

.server-time {
  color: #94a3b8;
  font-size: 0.9rem;
}

.empty-state {
  margin-top: 16px;
  color: #94a3b8;
}
</style>
