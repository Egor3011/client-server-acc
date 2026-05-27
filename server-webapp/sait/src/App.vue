<template>
  <div class="app-shell">
    <header class="topbar">
      <router-link class="brand" to="/">ACC Servers Control</router-link>
    </header>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid #1f2937;
  background: rgba(2, 6, 23, 0.82);
  backdrop-filter: blur(8px);
}

.brand {
  display: inline-block;
  padding: 16px 20px;
  color: #e2e8f0;
  font-weight: 700;
  text-decoration: none;
  letter-spacing: 0.02em;
}

.content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 28px 20px 40px;
}
</style>
