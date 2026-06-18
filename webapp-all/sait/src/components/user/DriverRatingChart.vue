<template>
    <div class="profile-block">
      <h2 class="block-title">Rating</h2>
      <div class="chart-wrapper">
        <apexchart
          type="area"
          height="180"
          :options="chartOptions"
          :series="chartSeries"
        ></apexchart>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  // Импортируем компонент из установленной библиотеки
  import apexchart from 'vue3-apexcharts';
  
  // Данные для графика (изменения рейтинга пилота по месяцам)
  const chartSeries = ref([
    {
      name: 'Rating',
      data: [38,54,67,52,45,56,72, 78, 81, 80, 86, 89, 92, 94,90,97,99]
    }
  ]);
  
  // Конфигурация внешнего вида графика
  const chartOptions = ref({
    chart: {
      id: 'driver-rating',
      toolbar: { show: false }, // Отключаем лишнее меню скачивания
      sparkline: { enabled: false },
      background: 'transparent'
    },
    colors: ['#888888'], // Изменено: линия графика сделана белой
    stroke: {
      curve: 'smooth', // Сглаженная кривая линия
      width: 3
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.5, // Изменено: полупрозрачная белая подложка под линией
        opacityTo: 0.02,
        stops: [0, 90, 100]
      }
    },
    markers: {
      size: 4,
      colors: ['#000000'],
      strokeColors: '#ffffff', // Изменено: обводка точек сделана белой вместо красной
      strokeWidth: 2,
      hover: { size: 6 }
    },
    theme: {
      mode: 'dark' // Автоматическая темная тема для подсказок
    },
    grid: {
      borderColor: '#2d2d2d',
      strokeDashArray: 4, // Пунктирная сетка
      padding: { left: 10, right: 10, bottom: 0 }
    },
    xaxis: {
      categories: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', "Авг", "Сен", "Окт", "Ноя", "Дек", 'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', "Авг", "Сен", "Окт", "Ноя", "Дек", 'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', "Авг", "Сен", "Окт", "Ноя", "Дек"],
      labels: {
        style: {
          colors: '#888888',
          fontFamily: 'Titillium Web, sans-serif',
          fontSize: '12px'
        }
      },
      axisBorder: { show: false },
      axisTicks: { show: false }
    },
    yaxis: {
      min: 20, // Диапазон рейтинга для наглядности колебаний
      max: 100,
      tickAmount: 5,
      labels: {
        style: {
          colors: '#888888',
          fontFamily: 'Titillium Web, sans-serif'
        }
      }
    },
    tooltip: {
      theme: 'dark',
      x: { show: false },
      y: {
        formatter: (val) => `${val} PTS`
      },
      // Изменено: цвет текста внутри всплывающего окошка (квадратика с рейтингом) сделан черным
      style: {
        fontSize: '12px',
        fontFamily: 'Titillium Web, sans-serif',
        colors: ['#000000'] 
      },
      borderWidth: 0
    }
  });
  </script>
  
  <style scoped>
  .chart-wrapper {
    width: 100%;
    /* Небольшой сдвиг, чтобы компенсировать внутренние отступы самого ApexCharts */
    margin-left: -10px; 
  }
  </style>
  