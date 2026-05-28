<template>
  <section class="promo-section">
    <div class="promo-grid">
      <a
        v-for="category in categories"
        :key="category.name"
        :href="category.href ?? '#'"
        class="promo-card"

      >
        <span class="promo-inner">
          <div class="promo-content">
            <p class="promo-title">{{ category.name.toUpperCase() }}</p>
            <span class="promo-description">{{ category.description }}</span>
          </div>
          <span class="promo-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M8.444 4v2H5v14h14v-3.706h2v3.765c0 1.06-.833 1.941-1.889 1.941H3.001V4z" fill="currentColor" />
              <path d="M19 4c1.103 0 2 .897 2 2v4.969h-2V7.372l-5.335 5.335-1.414-1.414L17.544 6h-3.617V4z" fill="currentColor" />
            </svg>
          </span>
        </span>
      </a>
    </div>
  </section>
</template>

<script setup lang="ts">
type CategoryItem = {
  name: string
  description: string
  href?: string
}

defineProps<{
  categories: CategoryItem[]
}>()
</script>

<style scoped>
.promo-section {
  padding: 2px 0;
}

.promo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 10px;
}

.promo-card {
  text-decoration: none;
  color: #ffffff;
  min-height: 102px;
  display: grid;
  cursor: pointer;
  align-items: stretch;
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(17, 19, 25, 0.9);
  border-radius: 10px;
  transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
}

.promo-card:hover {
  transform: translateY(-1px);
  border-radius: 10px 0px;
  cursor: pointer;
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(141, 13, 13, 0.96);
}

.promo-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px;
}

.promo-title {
  font-size: 1.02rem;
  font-family: 'Formula1', sans-serif;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.promo-icon {
  display: inline-flex;
  width: 22px;
  height: 22px;
  color: rgba(255, 255, 255, 0.9);
}

.promo-icon svg {
  width: 100%;
  height: 100%;
}
</style>
