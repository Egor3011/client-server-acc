<template>
<div class="dashboard-block pattern-backdrop">
        
    <div class="dashboard-header-block">
        <div>
            <h2>Event: Faster on MONZA</h2>
            <p>Set the fastest lap on this week and get cool prizes</p>
        </div>
        <div class="timer-container">
            <h2 id="timer">{{formattedTime}}</h2>
            <p>до конца</p>
        </div>
    </div>
      <!-- Левая часть: Трасса и Карта -->
    <div class="dashboard-main-block">
      <div class="track-section">
        <div class="track-bg"></div>
        <img src="https://racehub.s3.cloud.ru/monza-map2" alt="Track Map" class="track-map" />
      </div>
  
      <!-- Правая часть: Лидерборд ACC -->
      <div class="leaderboard-section">
        <div class="leaderboard-header">
          <span class="col-pos">#</span>
          <span class="col-name">DRIVER</span>
          <span class="col-car">CAR</span>
          <span class="col-gap">GAP</span>
          <span class="col-lap">BEST LAP</span>
        </div>
  
        <div class="leaderboard-list">
          <div 
            v-for="(driver, index) in leaderboard" 
            :key="driver.position" 
            class="driver-row"
            :style="{ '--delay': `${index * 0.1}s` }"
          >
            <div class="number-div">
                <span class="col-pos" :class="{ 'top-three': driver.position <= 3 }">
                {{ driver.position }}
                </span>
            </div>
            <div class="text-col">

                <span class="col-name">{{ driver.name }}</span>
                <span class="col-car">{{ driver.car }}</span>
                <span class="col-gap" :class="{ 'leader-gap': index === 0 }">
                {{ driver.gap }}
                </span>
                <span class="col-lap">{{ driver.best_lap }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
</div>
</template>
  
<script setup>
  import { ref, onMounted, computed, onUnmounted } from 'vue'

  const targetDate = new Date(2026, 5, 6, 23, 59, 59); // 10 секунд для теста
  const diff = ref(targetDate - Date.now());
  const isTimerOver = ref(false);
  let intervalId = null;

  // Форматируем строку времени (С ДНЯМИ)
  const formattedTime = computed(() => {
    if (isTimerOver.value || diff.value <= 0) return "00:00:00";

    const days = Math.floor(diff.value / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff.value % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff.value % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff.value % (1000 * 60)) / 1000);

    const timeArray = [
        String(hours).padStart(2, '0'),
        String(minutes).padStart(2, '0'),
        String(seconds).padStart(2, '0')
    ];

    // Если дни есть, добавляем их в начало строки
    if (days > 0) {
        return String(days).padStart(2, '0') + ':' + timeArray.join(':');
    }

    return timeArray.join(':');
  });

  // Обновление таймера
  const updateTimer = () => {
    const currentDiff = targetDate - Date.now();
    
    if (currentDiff <= 0) {
        diff.value = 0;
        isTimerOver.value = true;
        clearInterval(intervalId);
    } else {
        diff.value = currentDiff;
    }
  };

  onUnmounted(() => {
      if (intervalId) clearInterval(intervalId);
  });

  
  const leaderboard = ref([
  {
            "position": 1,
            "name": "I. Sidorov",
            "car": "Nissan GT-R Nismo GT3",
            "gap": "Leader",
            "best_lap": "1:47.327"
        },
        {
            "position": 2,
            "name": "P. Exe | REVV",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+0.425",
            "best_lap": "1:47.752"
        },
        {
            "position": 3,
            "name": "E. Ljungberg",
            "car": "Mercedes-AMG GT3",
            "gap": "+0.633",
            "best_lap": "1:47.960"
        },
        {
            "position": 4,
            "name": "H. HEAR",
            "car": "Porsche 992 GT3 R",
            "gap": "+0.888",
            "best_lap": "1:48.215"
        },
        {
            "position": 5,
            "name": "A. Giglietti",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+0.903",
            "best_lap": "1:48.230"
        },
        {
            "position": 6,
            "name": "J. GT",
            "car": "AMR V8 Vantage",
            "gap": "+1.005",
            "best_lap": "1:48.332"
        },
        {
            "position": 7,
            "name": "G. Stat1covich",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+1.063",
            "best_lap": "1:48.390"
        },
        {
            "position": 8,
            "name": "O. Sprzeglo",
            "car": "Mercedes-AMG GT3",
            "gap": "+1.108",
            "best_lap": "1:48.435"
        },
        {
            "position": 9,
            "name": "u. siivelt",
            "car": "Lexus RC F GT3",
            "gap": "+1.198",
            "best_lap": "1:48.525"
        },
        {
            "position": 10,
            "name": "C. Clinton",
            "car": "Porsche 992 GT3 R",
            "gap": "+1.208",
            "best_lap": "1:48.535"
        },
        {
            "position": 11,
            "name": "В. Марко",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+1.270",
            "best_lap": "1:48.597"
        },
        {
            "position": 12,
            "name": "J. Sturm",
            "car": "Ferrari 296 GT3",
            "gap": "+1.293",
            "best_lap": "1:48.620"
        },
        {
            "position": 13,
            "name": "D. Dieguez",
            "car": "Lexus RC F GT3",
            "gap": "+1.343",
            "best_lap": "1:48.670"
        },
        {
            "position": 14,
            "name": "M. alexander",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+1.365",
            "best_lap": "1:48.692"
        },
        {
            "position": 15,
            "name": "B. Britva",
            "car": "BMW M4 GT3",
            "gap": "+1.395",
            "best_lap": "1:48.722"
        },
        {
            "position": 16,
            "name": "R. Gallo",
            "car": "Ferrari 296 GT3",
            "gap": "+1.395",
            "best_lap": "1:48.722"
        },
        {
            "position": 17,
            "name": "S. Faiz",
            "car": "Lexus RC F GT3",
            "gap": "+1.425",
            "best_lap": "1:48.752"
        },
        {
            "position": 18,
            "name": "J. Beatton",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+1.465",
            "best_lap": "1:48.792"
        },
        {
            "position": 19,
            "name": "R. Joao",
            "car": "Ferrari 296 GT3",
            "gap": "+1.473",
            "best_lap": "1:48.800"
        },
        {
            "position": 20,
            "name": "B. Omaruly",
            "car": "BMW M4 GT3",
            "gap": "+1.485",
            "best_lap": "1:48.812"
        },
        {
            "position": 21,
            "name": "E. Aksenov",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+1.530",
            "best_lap": "1:48.857"
        },
        {
            "position": 22,
            "name": "E. Kro_31",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+1.623",
            "best_lap": "1:48.950"
        },
        {
            "position": 23,
            "name": "P. Bebroy",
            "car": "Lexus RC F GT3",
            "gap": "+1.648",
            "best_lap": "1:48.975"
        },
        {
            "position": 24,
            "name": "M. Rönnlund",
            "car": "Mercedes-AMG GT3",
            "gap": "+1.658",
            "best_lap": "1:48.985"
        },
        {
            "position": 25,
            "name": "h. criollo",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+1.665",
            "best_lap": "1:48.992"
        },
        {
            "position": 26,
            "name": "I. de Gennaro",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+1.675",
            "best_lap": "1:49.002"
        },
        {
            "position": 27,
            "name": "I. Philips",
            "car": "Jaguar G3",
            "gap": "+1.690",
            "best_lap": "1:49.017"
        },
        {
            "position": 28,
            "name": "R. REVV",
            "car": "Mercedes-AMG GT3",
            "gap": "+1.748",
            "best_lap": "1:49.075"
        },
        {
            "position": 29,
            "name": "J. Klebo",
            "car": "Lexus RC F GT3",
            "gap": "+1.800",
            "best_lap": "1:49.127"
        },
        {
            "position": 30,
            "name": "M. Ocsmall",
            "car": "Ferrari 296 GT3",
            "gap": "+1.805",
            "best_lap": "1:49.132"
        },
        {
            "position": 31,
            "name": "R. Darabant",
            "car": "Ford Mustang GT3",
            "gap": "+1.965",
            "best_lap": "1:49.292"
        },
        {
            "position": 32,
            "name": "A. Chernov",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+2.043",
            "best_lap": "1:49.370"
        },
        {
            "position": 33,
            "name": "A. Sharma",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+2.143",
            "best_lap": "1:49.470"
        },
        {
            "position": 34,
            "name": "M. Pregartner",
            "car": "Lamborghini Huracan Evo2",
            "gap": "+2.168",
            "best_lap": "1:49.495"
        },
        {
            "position": 35,
            "name": "P. Vettel",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+2.183",
            "best_lap": "1:49.510"
        },
        {
            "position": 36,
            "name": "M. Sophie",
            "car": "Ferrari 296 GT3",
            "gap": "+2.290",
            "best_lap": "1:49.617"
        },
        {
            "position": 37,
            "name": "J. Ron",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+2.318",
            "best_lap": "1:49.645"
        },
        {
            "position": 38,
            "name": "E. Martín",
            "car": "Porsche 911II GT3 R",
            "gap": "+2.330",
            "best_lap": "1:49.657"
        },
        {
            "position": 39,
            "name": "A. Ramirez",
            "car": "AMR V8 Vantage",
            "gap": "+2.370",
            "best_lap": "1:49.697"
        },
        {
            "position": 40,
            "name": "V. Morgan",
            "car": "Porsche 992 GT3 R",
            "gap": "+2.380",
            "best_lap": "1:49.707"
        },
        {
            "position": 41,
            "name": "L. Puf",
            "car": "Porsche 992 GT3 R",
            "gap": "+2.505",
            "best_lap": "1:49.832"
        },
        {
            "position": 42,
            "name": "R. Maciel",
            "car": "Porsche 992 GT3 R",
            "gap": "+2.515",
            "best_lap": "1:49.842"
        },
        {
            "position": 43,
            "name": "S. Rush",
            "car": "Ferrari 296 GT3",
            "gap": "+2.530",
            "best_lap": "1:49.857"
        },
        {
            "position": 44,
            "name": "M. Lankin",
            "car": "AMR V8 Vantage",
            "gap": "+2.538",
            "best_lap": "1:49.865"
        },
        {
            "position": 45,
            "name": "J. Palbrach-Mata",
            "car": "Porsche 992 GT3 R",
            "gap": "+2.653",
            "best_lap": "1:49.980"
        },
        {
            "position": 46,
            "name": "D. Ricciardo",
            "car": "BMW M4 GT3",
            "gap": "+2.688",
            "best_lap": "1:50.015"
        },
        {
            "position": 47,
            "name": "M. Praça",
            "car": "BMW M4 GT3",
            "gap": "+2.743",
            "best_lap": "1:50.070"
        },
        {
            "position": 48,
            "name": "М. бублик",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+2.838",
            "best_lap": "1:50.165"
        },
        {
            "position": 49,
            "name": "Tintanic",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+2.908",
            "best_lap": "1:50.235"
        },
        {
            "position": 50,
            "name": "I. Galindo",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+2.960",
            "best_lap": "1:50.287"
        },
        {
            "position": 51,
            "name": "E. M",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+2.960",
            "best_lap": "1:50.287"
        },
        {
            "position": 52,
            "name": "D. PHASE",
            "car": "Lamborghini Huracán SF EVO2",
            "gap": "+2.988",
            "best_lap": "1:50.315"
        },
        {
            "position": 53,
            "name": "J. Moya",
            "car": "BMW M4 GT3",
            "gap": "+3.010",
            "best_lap": "1:50.337"
        },
        {
            "position": 54,
            "name": "i. garimberti",
            "car": "Mercedes-AMG GT3",
            "gap": "+3.068",
            "best_lap": "1:50.395"
        },
        {
            "position": 55,
            "name": "R. Kurwica",
            "car": "Ferrari 296 GT3",
            "gap": "+3.163",
            "best_lap": "1:50.490"
        },
        {
            "position": 56,
            "name": "N. Said",
            "car": "BMW M4 GT3",
            "gap": "+3.175",
            "best_lap": "1:50.502"
        },
        {
            "position": 57,
            "name": "P. Potter",
            "car": "Porsche 911II GT3 R",
            "gap": "+3.293",
            "best_lap": "1:50.620"
        },
        {
            "position": 58,
            "name": "g. Lucca",
            "car": "Ferrari 296 GT3",
            "gap": "+3.298",
            "best_lap": "1:50.625"
        },
        {
            "position": 59,
            "name": "J. Urbanski",
            "car": "BMW M4 GT3",
            "gap": "+3.305",
            "best_lap": "1:50.632"
        },
        {
            "position": 60,
            "name": "y. cruz",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+3.370",
            "best_lap": "1:50.697"
        },
        {
            "position": 61,
            "name": "ç. çç",
            "car": "Ferrari 296 GT3",
            "gap": "+3.383",
            "best_lap": "1:50.710"
        },
        {
            "position": 62,
            "name": "j. d.v.",
            "car": "Porsche 992 GT3 R",
            "gap": "+3.403",
            "best_lap": "1:50.730"
        },
        {
            "position": 63,
            "name": "S. Plettau",
            "car": "Porsche 911II GT3 R",
            "gap": "+3.485",
            "best_lap": "1:50.812"
        },
        {
            "position": 64,
            "name": "V. Sharma",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+3.593",
            "best_lap": "1:50.920"
        },
        {
            "position": 65,
            "name": "R. Marciano",
            "car": "Ferrari 296 GT3",
            "gap": "+3.595",
            "best_lap": "1:50.922"
        },
        {
            "position": 66,
            "name": "J. DESOMB",
            "car": "Ferrari 296 GT3",
            "gap": "+3.613",
            "best_lap": "1:50.940"
        },
        {
            "position": 67,
            "name": "Н. Шахов",
            "car": "Audi R8 LMS GT3 evo II",
            "gap": "+3.678",
            "best_lap": "1:51.005"
        },
        {
            "position": 68,
            "name": "A. West",
            "car": "BMW M4 GT3",
            "gap": "+3.680",
            "best_lap": "1:51.007"
        },
        {
            "position": 69,
            "name": "J. Aristizabal",
            "car": "BMW M4 GT3",
            "gap": "+3.728",
            "best_lap": "1:51.055"
        },
        {
            "position": 70,
            "name": "L. Lopez",
            "car": "AMR V8 Vantage",
            "gap": "+3.770",
            "best_lap": "1:51.097"
        },
        {
            "position": 71,
            "name": "O. GILLES",
            "car": "Ferrari 296 GT3",
            "gap": "+3.805",
            "best_lap": "1:51.132"
        },
        {
            "position": 72,
            "name": "R. Zengin",
            "car": "BMW M4 GT3",
            "gap": "+3.853",
            "best_lap": "1:51.180"
        },
        {
            "position": 73,
            "name": "С. АНДРЮНИН",
            "car": "Ferrari 296 GT3",
            "gap": "+3.883",
            "best_lap": "1:51.210"
        },
        {
            "position": 74,
            "name": "M. Kostylev",
            "car": "BMW M4 GT3",
            "gap": "+3.958",
            "best_lap": "1:51.285"
        },
        {
            "position": 75,
            "name": "H. Berat",
            "car": "BMW M4 GT3",
            "gap": "+4.005",
            "best_lap": "1:51.332"
        },
        {
            "position": 76,
            "name": "P. Henrique",
            "car": "Mercedes-AMG GT3",
            "gap": "+4.073",
            "best_lap": "1:51.400"
        },
        {
            "position": 77,
            "name": "F. Sulzbacher",
            "car": "Mercedes-AMG GT3",
            "gap": "+4.130",
            "best_lap": "1:51.457"
        },
        {
            "position": 78,
            "name": "O. Fast",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+4.153",
            "best_lap": "1:51.480"
        },
        {
            "position": 79,
            "name": "N. Liveranski",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+4.285",
            "best_lap": "1:51.612"
        },
        {
            "position": 80,
            "name": "P. Groot",
            "car": "Lamborghini Huracan Evo2",
            "gap": "+4.418",
            "best_lap": "1:51.745"
        },
        {
            "position": 81,
            "name": "s. 666",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+4.443",
            "best_lap": "1:51.770"
        },
        {
            "position": 82,
            "name": "J. Rycerz",
            "car": "Audi R8 LMS GT3 evo II",
            "gap": "+4.475",
            "best_lap": "1:51.802"
        },
        {
            "position": 83,
            "name": "C. Burtin",
            "car": "BMW M4 GT3",
            "gap": "+4.498",
            "best_lap": "1:51.825"
        },
        {
            "position": 84,
            "name": "e. karpunin",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+4.585",
            "best_lap": "1:51.912"
        },
        {
            "position": 85,
            "name": "D. Trouble",
            "car": "BMW M4 GT3",
            "gap": "+4.793",
            "best_lap": "1:52.120"
        },
        {
            "position": 86,
            "name": "T. Cooper",
            "car": "Ferrari 296 GT3",
            "gap": "+4.855",
            "best_lap": "1:52.182"
        },
        {
            "position": 87,
            "name": "D. Golubev",
            "car": "Honda NSX Evo",
            "gap": "+4.870",
            "best_lap": "1:52.197"
        },
        {
            "position": 88,
            "name": "M. Leitplanke",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+4.873",
            "best_lap": "1:52.200"
        },
        {
            "position": 89,
            "name": "g. baldini",
            "car": "Lamborghini Huracan Evo2",
            "gap": "+4.953",
            "best_lap": "1:52.280"
        },
        {
            "position": 90,
            "name": "O. Shunevych",
            "car": "Ferrari 296 GT3",
            "gap": "+5.113",
            "best_lap": "1:52.440"
        },
        {
            "position": 91,
            "name": "c. baldry",
            "car": "AMR V8 Vantage",
            "gap": "+5.198",
            "best_lap": "1:52.525"
        },
        {
            "position": 92,
            "name": "K. Gordejev",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+5.198",
            "best_lap": "1:52.525"
        },
        {
            "position": 93,
            "name": "H. Jusnes",
            "car": "McLaren 720S GT3",
            "gap": "+5.263",
            "best_lap": "1:52.590"
        },
        {
            "position": 94,
            "name": "B. Nolikovich",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+5.298",
            "best_lap": "1:52.625"
        },
        {
            "position": 95,
            "name": "J. Hill",
            "car": "Mercedes-AMG GT3",
            "gap": "+5.380",
            "best_lap": "1:52.707"
        },
        {
            "position": 96,
            "name": "M. V",
            "car": "BMW M4 GT3",
            "gap": "+5.403",
            "best_lap": "1:52.730"
        },
        {
            "position": 97,
            "name": "Ş. Köse",
            "car": "BMW M4 GT3",
            "gap": "+5.558",
            "best_lap": "1:52.885"
        },
        {
            "position": 98,
            "name": "M. Rehnström",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+5.658",
            "best_lap": "1:52.985"
        },
        {
            "position": 99,
            "name": "F. Brumatti",
            "car": "Mercedes-AMG GT3",
            "gap": "+5.723",
            "best_lap": "1:53.050"
        },
        {
            "position": 100,
            "name": "Y. SHWAYYAT",
            "car": "Lamborghini Huracan Evo",
            "gap": "+5.765",
            "best_lap": "1:53.092"
        },
        {
            "position": 101,
            "name": "U. Dağaşar",
            "car": "BMW M4 GT3",
            "gap": "+5.803",
            "best_lap": "1:53.130"
        },
        {
            "position": 102,
            "name": "S. Kuzyuchela",
            "car": "Porsche 992 GT3 R",
            "gap": "+5.908",
            "best_lap": "1:53.235"
        },
        {
            "position": 103,
            "name": "Е. Михайлов",
            "car": "Ferrari 296 GT3",
            "gap": "+5.958",
            "best_lap": "1:53.285"
        },
        {
            "position": 104,
            "name": "E. Sladkevičius",
            "car": "BMW M4 GT3",
            "gap": "+5.993",
            "best_lap": "1:53.320"
        },
        {
            "position": 105,
            "name": "y. Z",
            "car": "BMW M4 GT3",
            "gap": "+6.003",
            "best_lap": "1:53.330"
        },
        {
            "position": 106,
            "name": "L. Alvarado",
            "car": "McLaren 720S GT3",
            "gap": "+6.033",
            "best_lap": "1:53.360"
        },
        {
            "position": 107,
            "name": "G. de Gennaro",
            "car": "Ferrari 296 GT3",
            "gap": "+6.235",
            "best_lap": "1:53.562"
        },
        {
            "position": 108,
            "name": "L. S",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+6.378",
            "best_lap": "1:53.705"
        },
        {
            "position": 109,
            "name": "H. RÜZGAR",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+6.380",
            "best_lap": "1:53.707"
        },
        {
            "position": 110,
            "name": "A.Penkovsky",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+6.383",
            "best_lap": "1:53.710"
        },
        {
            "position": 111,
            "name": "B. Lmt",
            "car": "Ferrari 488 GT3",
            "gap": "+6.403",
            "best_lap": "1:53.730"
        },
        {
            "position": 112,
            "name": "M. Carrot",
            "car": "Porsche 911II GT3 R",
            "gap": "+6.525",
            "best_lap": "1:53.852"
        },
        {
            "position": 113,
            "name": "D. Anatolii",
            "car": "Nissan GT-R Nismo GT3",
            "gap": "+6.528",
            "best_lap": "1:53.855"
        },
        {
            "position": 114,
            "name": "S. Raub",
            "car": "Mercedes-AMG GT3",
            "gap": "+6.528",
            "best_lap": "1:53.855"
        },
        {
            "position": 115,
            "name": "T. Eagle",
            "car": "Audi R8 LMS GT3 evo II",
            "gap": "+6.545",
            "best_lap": "1:53.872"
        },
        {
            "position": 116,
            "name": "n. ///",
            "car": "Porsche 911II GT3 R",
            "gap": "+6.585",
            "best_lap": "1:53.912"
        },
        {
            "position": 117,
            "name": "R. Marcelino",
            "car": "Ferrari 488 GT3",
            "gap": "+6.623",
            "best_lap": "1:53.950"
        },
        {
            "position": 118,
            "name": "T. Chell",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+7.040",
            "best_lap": "1:54.367"
        },
        {
            "position": 119,
            "name": "B. szalontai",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+7.085",
            "best_lap": "1:54.412"
        },
        {
            "position": 120,
            "name": "K. Bashkirkin",
            "car": "Mercedes-AMG GT3",
            "gap": "+7.088",
            "best_lap": "1:54.415"
        },
        {
            "position": 121,
            "name": "C. Anselmo",
            "car": "Porsche 911II GT3 R",
            "gap": "+7.155",
            "best_lap": "1:54.482"
        },
        {
            "position": 122,
            "name": "L. Cat",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+7.328",
            "best_lap": "1:54.655"
        },
        {
            "position": 123,
            "name": "B. Pugh",
            "car": "Nissan GT-R Nismo GT3",
            "gap": "+7.335",
            "best_lap": "1:54.662"
        },
        {
            "position": 124,
            "name": "G. Vito",
            "car": "Ferrari 296 GT3",
            "gap": "+7.345",
            "best_lap": "1:54.672"
        },
        {
            "position": 125,
            "name": "M. Borovikov",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+7.493",
            "best_lap": "1:54.820"
        },
        {
            "position": 126,
            "name": "D. Lux",
            "car": "Porsche 911II GT3 R",
            "gap": "+7.498",
            "best_lap": "1:54.825"
        },
        {
            "position": 127,
            "name": "M. Feher",
            "car": "Lamborghini Huracan Evo",
            "gap": "+7.498",
            "best_lap": "1:54.825"
        },
        {
            "position": 128,
            "name": "R. Baker",
            "car": "Honda NSX Evo",
            "gap": "+7.505",
            "best_lap": "1:54.832"
        },
        {
            "position": 129,
            "name": "H. B.",
            "car": "Ferrari 296 GT3",
            "gap": "+7.698",
            "best_lap": "1:55.025"
        },
        {
            "position": 130,
            "name": "W. winch",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+7.768",
            "best_lap": "1:55.095"
        },
        {
            "position": 131,
            "name": "S. Karni",
            "car": "Ferrari 296 GT3",
            "gap": "+7.978",
            "best_lap": "1:55.305"
        },
        {
            "position": 132,
            "name": "M. Moraes",
            "car": "Lamborghini Huracan Evo",
            "gap": "+7.980",
            "best_lap": "1:55.307"
        },
        {
            "position": 133,
            "name": "M. Cramer",
            "car": "Audi R8 LMS Evo",
            "gap": "+8.098",
            "best_lap": "1:55.425"
        },
        {
            "position": 134,
            "name": "L. Pedrotti",
            "car": "Porsche 911II GT3 R",
            "gap": "+8.890",
            "best_lap": "1:56.217"
        },
        {
            "position": 135,
            "name": "G. Ruiz",
            "car": "Porsche 911II GT3 R",
            "gap": "+8.895",
            "best_lap": "1:56.222"
        },
        {
            "position": 136,
            "name": "D. Denysevych",
            "car": "Mercedes-AMG GT3",
            "gap": "+8.903",
            "best_lap": "1:56.230"
        },
        {
            "position": 137,
            "name": "h. hant",
            "car": "Ferrari 488 GT3",
            "gap": "+10.868",
            "best_lap": "1:58.195"
        },
        {
            "position": 138,
            "name": "B. Shvets",
            "car": "Ford Mustang GT3",
            "gap": "+10.873",
            "best_lap": "1:58.200"
        },
        {
            "position": 139,
            "name": "B. Zawadzki",
            "car": "Lexus RC F GT3",
            "gap": "+11.663",
            "best_lap": "1:58.990"
        },
        {
            "position": 140,
            "name": "C. Go",
            "car": "McLaren 720S GT3 Evo",
            "gap": "+11.748",
            "best_lap": "1:59.075"
        },
        {
            "position": 141,
            "name": "V. Kovskiy",
            "car": "BMW M4 GT3",
            "gap": "+14.383",
            "best_lap": "2:01.710"
        }
]);

  
    onMounted(async () => {
        // ОБНОВЛЕНО: Изменили интервал на 1000мс (1 секунда), так как МС больше нет
        intervalId = setInterval(updateTimer, 1000);
        
        try {
        const response = await fetch('http://127.0.0') 
        if (response.ok) {
            leaderboard.value = await response.json()
        }
        } catch (error) {
        console.error('Ошибка загрузки лидерборда:', error)
        }
    })
  </script>
  
  <style scoped>

    #timer {
        transition: color 0.2s ease;
    }
    #timer.finished {
        color: #ff3333;
        text-shadow: 0 0 10px rgba(255, 51, 51, 0.6);
    }

  /* Главный контейнер */
  .dashboard-block {
    
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 12px 0;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  }

  .dashboard-main-block {
    display: flex;
    width: 100%;
    max-width: 1200px;
    height: 500px;
    overflow: hidden;
  }
  
  .dashboard-header-block {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    
  }

  /* Левая секция (Трасса) */
  .track-section {
    position: relative;
    width: 40%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    box-sizing: border-box;
  }
  
  /* Затемненный фон на 40% (rgba 0.4) */
  .track-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    clip-path: polygon(
        20px 0,                       /* Срез верхнего левого */
        100% 0,                       /* Верхний правый (острый) */
        100% calc(100% - 20px),       /* Начало среза нижнего правого */
        calc(100% - 20px) 100%,       /* Конец среза нижнего правого */
        0 100%,                       /* Нижний левый (острый) */
        0 20px                        /* Возврат к срезу верхнего левого */
        );

    background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)), 
                      url('https://i.pinimg.com/1200x/d7/84/78/d784789e23bd5705af81c8c0ee90a7f1.jpg');
    background-size: cover;
    background-position: center;
    z-index: 1;
  }
  
  /* Карта поверх фона (Максимальный размер без деформации и выхода за рамки) */
  .track-map {
    position: relative;
    z-index: 2;
    width: 100%;
    height: 100%;
    object-fit: contain; /* Увеличивает карту по максимуму, сохраняя пропорции */
    pointer-events: none;
  }
  
  /* Правая секция (Лидерборд) */
  .leaderboard-section {
    width: 60%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 5px 15px;
    box-sizing: border-box;
    scrollbar-gutter: stable; 
    overflow-x: hidden;
  }
  
  /* Шапка таблицы */
  .leaderboard-header {
    display: flex;
    padding: 10px;
    padding-top: 0;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
    font-family: Formula1;
    color: #64748b;
    border-bottom: 1px solid #232730;
    text-transform: uppercase;
  }
  
  /* Сетка колонок в стиле симуляторов */
  .col-pos { 
    width: 80px; text-align: center; 
    font-family: Formula1;
    font-size: 16px;
    }
  .col-name { 
    flex: 2; padding-left: 10px;
    font-weight: 700;
    font-family: Formula1;
    }
  .col-car { flex: 1.5; color: #94a3b8; }
  .col-gap { width: 90px; text-align: right; }
  .col-lap { width: 100px; text-align: right; }
  
  /* Список */
  .leaderboard-list {
    flex: 1;
    overflow-y: auto;
    margin-top: 5px;
  }

  .number-div {
    display: flex;
    align-items: center;
    padding: 0;
    height: 51px;
    border-radius: 20px 0;
    width: 80px;
    
    border-right: 1px solid rgba(255, 255, 255, 0.16);
  }

  .text-col {
    display: flex;
    align-items: center;
    padding: 12px 10px;
    width: 100%;
    margin-bottom: 4px;
    }
  
  /* Строка гонщика */
  .driver-row {
    display: flex;
    align-items: center;
    padding: 0px;
    margin-bottom: 4px;
    background-color: rgba(17, 19, 25, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.16);
    color: #e2e8f0;
    font-size: 14px;

    border-radius: 20px 0;
    
    /* Анимация появления */
    opacity: 0;
    transform: translateX(-30px);
    animation: slideIn 0.5s ease-out forwards;
    animation-delay: var(--delay);

    transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;

  }
  
  /* Стили элементов ACC */
  .driver-row:hover {

    background-color: #222933;
  }

  .driver-row:hover .number-div {
    background: rgba(141, 13, 13, 0.96);
  }
  
  .top-three {
    color: #ffffff; /* Выделение топ-3 */
    font-weight: bold;
  }
  
  .leader-gap {
    color: #10b981;
    font-weight: bold;
  }
  .timer-container{
    text-align: center;
    }
  /* Анимация выезда слева из прозрачности */
  @keyframes slideIn {
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  </style>
  