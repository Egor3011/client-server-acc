<template>
    <div class="container">
      <!-- Текст на заднем плане -->
      <h1 class="background-text">EVENT ON MONZA</h1>
      
      <!-- Картинка машины поверх текста -->
      <img 
        src="https://www.pngarts.com/files/4/Porsche-PNG-Photo.png" 
        alt="Car" 
        class="car-image"
      />
    </div>
  </template>
  
  <script setup>
  // Скрипт готов к работе
  </script>
  
  <style scoped>
  .container {
    position: relative;
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: none;
    /* Цвет фона удален, контейнер прозрачный */
  }
  
  .background-text {
    position: absolute;
    font-size: 8vw;
    font-weight: 900;
    color: rgb(255, 255, 255);
    text-transform: uppercase;
    transform: scaleY(2);
    user-select: none;
    z-index: 1;
    margin: 0;
    white-space: nowrap;
    
    /* Смещаем текст чуть выше центра */
    transform: translateY(-25%);
  }
  
  .car-image {
    position: relative;
    max-width: 80%;
    height: auto;
    z-index: 2;
    filter: drop-shadow(0px 10px 20px rgba(0,0,0,0.3));
  }
  </style>
  