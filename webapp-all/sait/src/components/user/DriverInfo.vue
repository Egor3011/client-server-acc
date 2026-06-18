<template>
    <div class="profile-block pattern-backdrop">
      <h2 class="block-title">Driver info</h2>
      <ul class="info-list">
        <li>
          <span class="info-label">Команда:</span>
          <span class="info-value highlight">Oracle Red Bull Racing</span>
        </li>
        <li>
          <span class="info-label">Страна:</span>
          <span class="info-value">Россия</span>
        </li>
        <li>
          <span class="info-label">Возраст:</span>
          <span class="info-value">26 лет</span>
        </li>
        <li>
          <span class="info-label">Стаж в симрейсинге:</span>
          <span class="info-value">5 лет</span>
        </li>
        <li>
          <span class="info-label">Лицензия:</span>
          <span class="info-value grade-a">Class A</span>
        </li>
      </ul>
    </div>
  </template>
  
  <style scoped>
  .info-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .info-list li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #2d2d2d;
    padding-bottom: 10px;
  }
  .info-list li:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
  .info-label {
    color: #888;
    font-size: 0.95rem;
  }
  .info-value {
    color: #fff;
    font-weight: 600;
  }
  .info-value.highlight {
    color: #e10600;
  }
  .grade-a {
    background: #e10600;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    text-transform: uppercase;
  }
  </style>
  