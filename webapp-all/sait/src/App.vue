<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? '/api'
const steamId = ref<string | null>(null)

const steamLoginUrl = computed(() => {
  if (typeof window === 'undefined') return '#'
  const next = `${window.location.origin}${window.location.pathname}`
  return `${apiBaseUrl}/auth/steam/login?next=${encodeURIComponent(next)}`
})

function clearSteamAuth() {
  steamId.value = null
  if (typeof window !== 'undefined') {
    window.localStorage.removeItem('acc_steam_id')
  }
}

onMounted(() => {
  const saved = window.localStorage.getItem('acc_steam_id')
  if (saved) steamId.value = saved

  const params = new URLSearchParams(window.location.search)
  const steamIdFromCallback = params.get('steam_id')
  if (steamIdFromCallback) {
    steamId.value = steamIdFromCallback
    window.localStorage.setItem('acc_steam_id', steamIdFromCallback)
    params.delete('steam_id')
    const cleanUrl = `${window.location.pathname}${params.toString() ? `?${params.toString()}` : ''}`
    window.history.replaceState({}, '', cleanUrl)
  }
})
</script>

<template>
  <div class="app-shell">
    <header class="top-header">
      <div class="brand">
        <span class="brand-accent" />
        <div class="brand-text">
          <strong>RACE-hub</strong>
          <small>GT Series</small>
        </div>
      </div>

      <nav class="main-nav">
        <RouterLink to="/" active-class="active">Home</RouterLink>
        <RouterLink to="/news" active-class="active">News</RouterLink>
      </nav>

      <div class="auth-panel">
        <a v-if="!steamId" class="auth-button" :href="steamLoginUrl">Sign in with Steam</a>
        <template v-else>
          <span class="steam-id">Steam ID: {{ steamId }}</span>
          <button class="auth-button ghost" @click="clearSteamAuth">Logout</button>
        </template>
      </div>
    </header>

    <main class="page-content">
      <RouterView v-slot="{ Component, route }">
        <Transition name="route" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.top-header {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(14, 16, 22, 0.88);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 24px;
  padding: 14px 22px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-accent {
  width: 4px;
  height: 36px;
  border-radius: 4px;
  background: #d9dee9;
}

.brand-text {
  display: grid;
  line-height: 1.1;
}

.brand-text strong {
  color: #f5f5f5;
  letter-spacing: 0.04em;
}

.brand-text small {
  color: #b6bcc6;
}

.main-nav {
  display: flex;
  gap: 8px;
  justify-self: center;
}

.main-nav a {
  text-decoration: none;
  color: #e4e8ef;
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid transparent;
}

.main-nav a.active {
  border-color: rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.04);
}

.auth-panel {
  justify-self: end;
  display: flex;
  align-items: center;
  gap: 10px;
}

.steam-id {
  color: #c8cfdb;
  font-size: 0.86rem;
}

.auth-button {
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.22);
  background: rgba(255, 255, 255, 0.04);
  color: #e6ebf5;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

.auth-button.ghost {
  background: transparent;
}

.page-content {
  max-width: 1220px;
  margin: 0 auto;
  padding: 24px 18px 40px;
}

.route-enter-active,
.route-leave-active {
  transition: opacity 240ms ease, transform 240ms ease, filter 240ms ease;
}

.route-enter-from {
  opacity: 0;
  transform: translateY(8px) scale(0.995);
  filter: blur(2px);
}

.route-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.995);
  filter: blur(2px);
}
</style>
