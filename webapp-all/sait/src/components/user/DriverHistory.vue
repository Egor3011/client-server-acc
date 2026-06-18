<template>
    <div class="profile-block pattern-backdrop full-width">
      <h2 class="block-title">History tournaments</h2>
      <div class="history-list">
        <div v-for="(race, index) in races" :key="index" class="race-card">
          <div class="race-position" :class="'pos-' + race.position">
            {{ race.position }}
          </div>
          <div class="race-details">
            <h4 class="important-text">{{ race.title }}</h4>
            <p class="race-meta">{{ race.split }} • {{ race.car }}</p>
          </div>
          <div class="race-date">{{ race.date }}</div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const races = ref([
    { position: 1, title: 'Porsche Cup Sprint Series', split: 'Split 1', car: 'Porsche 911 GT3', date: 'Июнь 2026' },
    { position: 2, title: 'GT3 Endurance Championship', split: 'Split 2', car: 'Ferrari 296 GT3', date: 'Май 2026' },
    { position: 1, title: 'SimRacing Russia Pro League', split: 'Split 1', car: 'BMW M4 GT3', date: 'Апрель 2026' },
    { position: 5, title: '24 Hours of Spa Virtual', split: 'Top Split', car: 'Audi R8 LMS', date: 'Март 2026' }
  ]);
  </script>
  
  <style scoped>
  .history-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .race-card {
    display: flex;
    align-items: center;
    background: rgba(0, 0, 0, 0.4);
    
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 12px 0;
    padding: 12px 16px;
  }
  .race-position {
    width: 36px;
    height: 36px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Formula1', sans-serif;
    font-weight: 700;
    font-size: 1.2rem;
    margin-right: 16px;
    background: #333;
    color: #fff;
  }
  .race-position.pos-1 {
    background: #ffd700;
    color: #000;
  }
  .race-position.pos-2 {
    background: #c0c0c0;
    color: #000;
  }
  .race-details {
    flex-grow: 1;
  }
  .race-meta {
    margin: 2px 0 0 0;
    font-size: 0.85rem;
    color: #888;
  }
  .race-date {
    font-size: 0.9rem;
    color: #666;
  }
  </style>
  