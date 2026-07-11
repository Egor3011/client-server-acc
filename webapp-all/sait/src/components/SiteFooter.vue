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

      <nav class="footer-links" aria-label="Подвал сайта">
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
        <span class="divider" aria-hidden="true" />
        <a
          class="support-btn"
          href="https://t.me/zavoz_contenta"
          target="_blank"
          rel="noopener noreferrer"
        >
          <svg class="support-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path
              fill="currentColor"
              d="M21.95 4.57a1.5 1.5 0 0 0-1.53-.2L2.5 11.41c-1.12.49-1.1 2.08.03 2.54l4.77 1.86 1.86 4.77c.46 1.13 2.05 1.15 2.54.03l7.04-17.92a1.5 1.5 0 0 0-.79-1.92ZM8.5 13.5l7.73-5.2-5.2 7.73-1.4-1.53-1.13-1z"
            />
          </svg>
          Поддержка
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

.support-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid rgba(41, 182, 246, 0.45);
  background: rgba(41, 182, 246, 0.12);
  color: #e8f6ff;
  font-size: 0.9rem;
  border-bottom: 1px solid rgba(41, 182, 246, 0.45);
  transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease, transform 0.2s ease;
}

.support-btn:hover {
  color: #ffffff;
  background: rgba(41, 182, 246, 0.22);
  border-color: rgba(41, 182, 246, 0.7);
  border-bottom-color: rgba(41, 182, 246, 0.7);
  transform: translateY(-1px);
}

.support-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
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
