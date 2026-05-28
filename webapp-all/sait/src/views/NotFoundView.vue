<template>
  <section class="not-found">
    <p class="code">404</p>
    <h1>Страница не найдена</h1>
    <p class="desc">Похоже, что этот заезд еще не внесли в календарь. Вернись на главную.</p>
    <RouterLink class="back-link" to="/">На главную</RouterLink>
  </section>
</template>

<style scoped>
.not-found {
  min-height: 55vh;
  display: grid;
  place-content: center;
  gap: 10px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.16);
  padding: 24px;
  clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 18px 100%, 0 calc(100% - 18px));
  background: linear-gradient(140deg, rgba(128, 0, 0, 0.5), rgba(10, 11, 16, 0.9));
}

.code {
  font-size: clamp(3rem, 8vw, 5rem);
  font-weight: 700;
  color: #fff;
}

h1 {
  color: #f5f8ff;
}

.desc {
  color: #c4ccd9;
}

.back-link {
  margin: 8px auto 0;
  text-decoration: none;
  color: #f0f4ff;
  border: 1px solid rgba(255, 255, 255, 0.26);
  padding: 10px 14px;
  border-radius: 0 12px 0 12px;
}
</style>
