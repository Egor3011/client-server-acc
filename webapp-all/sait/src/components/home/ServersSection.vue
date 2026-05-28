<template>
  <section class="servers-section">
    <div class="servers-head">
      <h3>Доступные сервера</h3>
      <button class="angled-btn" :disabled="loading" @click="$emit('refresh')">
        {{ loading ? 'Loading...' : 'Refresh' }}
      </button>
    </div>
    <p v-if="error" class="error-text">{{ error }}</p>
    <div v-if="servers.length" class="servers-grid">
      <article v-for="server in servers" :key="server.ip" class="server-card">
        <header>
          <strong>{{ server.ip }}</strong>
          <span class="status">Online</span>
        </header>
        <p>Last seen: {{ formatTime(server.last_seen_at) }}</p>
        <button class="open-btn angled-btn">Open control</button>
      </article>
    </div>
    <p v-else-if="!loading" class="muted">Пока нет активных серверов.</p>
  </section>
</template>

<script setup lang="ts">
type ServerItem = {
  ip: string
  last_seen_at: string
}

defineProps<{
  servers: ServerItem[]
  loading: boolean
  error: string
}>()

defineEmits<{
  refresh: []
}>()

function formatTime(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}
</script>

<style scoped>
.servers-section {
  background: rgba(15, 17, 23, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.14);
  padding: 18px;
  border-radius: 12px;
}

.servers-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.servers-head h3 {
  color: #fff;
}

.angled-btn {
  border: 1px solid rgba(255, 255, 255, 0.28);
  background: rgba(255, 255, 255, 0.06);
  color: #eceff8;
  border-radius: 8px;
  padding: 8px 14px;
  cursor: pointer;
}

.servers-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.server-card {
  border: 1px solid rgba(255, 255, 255, 0.14);
  padding: 12px;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.02));
  border-radius: 10px;
}

.server-card header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.server-card strong {
  color: #f4f5f8;
}

.status {
  color: #b0f6be;
  border: 1px solid rgba(176, 246, 190, 0.4);
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 0.75rem;
}

.server-card p,
.muted {
  margin-top: 8px;
  color: #abb3c2;
}

.open-btn {
  margin-top: 10px;
}

.error-text {
  color: #ff9ea0;
}
</style>
