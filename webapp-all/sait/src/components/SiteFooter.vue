<template>
  <footer class="site-footer pattern-backdrop">
    <div class="footer-inner">
      <div class="footer-brand">
        <span class="brand-accent" />
        <div class="brand-text">
          <strong>RACE-hub</strong>
          <small>GT Series</small>
        </div>
      </div>

      <nav class="footer-links" aria-label="Юридические документы">
        <a
          href="https://telegra.ph/Politika-konfidencialnosti-06-21-31"
          target="_blank"
          rel="noopener noreferrer"
        >
          Политика конфиденциальности
        </a>
        <span class="divider" aria-hidden="true" />
        <a
          href="https://telegra.ph/Polzovatelskoe-soglashenie-04-01-19"
          target="_blank"
          rel="noopener noreferrer"
        >
          Пользовательское соглашение
        </a>
      </nav>

      <p class="footer-copy">© {{ year }} RACE-hub</p>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped>
.site-footer {
  margin-top: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-inner {
  max-width: 1220px;
  margin: 0 auto;
  padding: 28px 18px 32px;
  display: grid;
  gap: 20px;
  align-items: center;
}

.footer-brand {
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

.footer-links {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px 16px;
}

.footer-links a {
  color: #c8cfdb;
  text-decoration: none;
  font-size: 0.92rem;
  padding: 6px 0;
  border-bottom: 1px solid transparent;
  transition: color 0.2s ease, border-color 0.2s ease;
}

.footer-links a:hover {
  color: #f5f5f5;
  border-bottom-color: rgba(255, 255, 255, 0.35);
}

.divider {
  width: 1px;
  height: 14px;
  background: rgba(255, 255, 255, 0.18);
}

.footer-copy {
  color: #7f8796;
  font-size: 0.84rem;
}

@media (min-width: 768px) {
  .footer-inner {
    grid-template-columns: auto 1fr auto;
    gap: 24px;
  }

  .footer-links {
    justify-self: center;
  }

  .footer-copy {
    justify-self: end;
    text-align: right;
  }
}
</style>
