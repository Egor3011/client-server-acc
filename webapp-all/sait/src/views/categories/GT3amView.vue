<template>
    <div class="about">
      <h1>This is an GT3-a page</h1>
    </div>
  </template>
  
  <script setup>
  import { onMounted, onUnmounted } from 'vue';
  
  onMounted(() => {
    document.body.classList.add('special-page-body');
  });
  
  onUnmounted(() => {
    document.body.classList.remove('special-page-body');
  });
  </script>

  <style>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }

  .special-page-body {
    background: linear-gradient(to bottom, #FE202F, #D5030C);

    }
  </style>