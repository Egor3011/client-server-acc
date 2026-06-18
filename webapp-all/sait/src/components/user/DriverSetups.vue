<template>
    <div class="profile-block full-width">
      <h2 class="block-title">Setups</h2>
      <div class="table-responsive">
        <table class="setups-table">
          <thead>
            <tr>
              <th>Автомобиль</th>
              <th>Трасса</th>
              <th>Время круга</th>
              <th>Опубликован</th>
              <th class="text-right">Действие</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(setup, index) in setups" :key="index">
              <td class="important-text">{{ setup.car }}</td>
              <td>{{ setup.track }}</td>
              <td class="time-highlight">{{ setup.lapTime }}</td>
              <td>{{ setup.date }}</td>
              <td class="text-right">
                <button class="download-btn">Download</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const setups = ref([
    { car: 'Ferrari 296 GT3', track: 'Monza', lapTime: '1:46.231', date: '14.06.2026' },
    { car: 'Porsche 911 GT3 R', track: 'Spa-Francorchamps', lapTime: '2:16.854', date: '10.05.2026' },
    { car: 'BMW M4 GT3', track: 'Nürburgring GP', lapTime: '1:54.012', date: '22.04.2026' }
  ]);
  </script>
  
  <style scoped>
  .table-responsive {
    width: 100%;
    overflow-x: auto;
  }
  .setups-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }
  .setups-table th {
    color: #888;
    font-size: 0.85rem;
    text-transform: uppercase;
    padding: 12px 16px;
    border-bottom: 2px solid #333;
  }
  .setups-table td {
    padding: 16px;
    border-bottom: 1px solid #2d2d2d;
    font-size: 0.95rem;
  }
  .time-highlight {
    color: #e10600;
    font-weight: 700;
  }
  .text-right {
    text-align: right;
  }
  .download-btn {
    background-color: #ffffff;
    color: #000000;
    border: none;
    padding: 6px 18px;
    font-family: 'Titillium Web', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    border-radius: 20px; /* Белая закругленная кнопка */
    cursor: pointer;
    transition: opacity 0.2s;
  }
  .download-btn:hover {
    opacity: 0.85;
  }
  </style>
  