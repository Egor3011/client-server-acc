<template>
    <div class="news-container" v-if="news">
      <!-- Метаданные из Frontmatter -->
      <h1 class="news-title">{{ news.title }}</h1>
      <p class="news-date">{{ news.date }}</p>
      
      <!-- Сюда рендерится готовый HTML из S3 -->
      <div class="news-content" v-html="newsHtml"></div>
    </div>
    <div v-else-if="loading">Загрузка новости...</div>
    <div v-else>Ошибка загрузки или новость не найдена.</div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useRoute } from 'vue-router';
  import { marked } from 'marked';
  
  const route = useRoute();
  const news = ref(null);
  const loading = ref(true);
  
  // Базовый URL вашего S3 бакета
  const S3_BUCKET_URL = 'https://racehub.s3.cloud.ru';
  
  const parseMarkdown = (text) => {
    // Заменяем Windows-переносы строк \r\n на стандартные \n
    const cleanText = text.replace(/\r\n/g, '\n');
    
    // Более надежное регулярное выражение для поиска блоков ---
    const match = cleanText.match(/^---([\s\S]*?)---\n([\s\S]*)$/);
    
    if (!match) {
      // Если разметки метаданных нет, берем весь текст как контент
      return { meta: {}, content: cleanText };
    }
    
    const yamlBlock = match[1];
    const content = match[2];
    const meta = {};
    
    yamlBlock.split('\n').forEach(line => {
      const colonIndex = line.indexOf(':');
      if (colonIndex !== -1) {
        const key = line.slice(0, colonIndex).trim();
        const val = line.slice(colonIndex + 1).trim().replace(/['"]/g, '');
        if (key) meta[key] = val;
      }
    });
    
    return { meta, content };
  };
  
  
  // Превращаем чистый текст Markdown в HTML
  const newsHtml = computed(() => {
    if (!news.value) return '';
    return marked(news.value.content, {
      gfm: true, // Включает поддержку GitHub-разметки (таблицы, автоссылки)
      breaks: true // Переносы строк как в оригинале
    });
  });


  onMounted(async () => {
    const newsId = route.params.id;
    try {
        // Сброс кэша браузера (добавляем уникальный таймштамп к ссылке)
        const cacheBuster = `?t=${new Date().getTime()}`;
        const url = `${S3_BUCKET_URL}/${newsId}.txt${cacheBuster}`;

        const response = await fetch(url, {
        method: 'GET',
        mode: 'cors' // Браузер обязан проверить новые правила CORS от Cloud.ru
        });

        if (!response.ok) throw new Error('Новость не найдена на S3');

        const rawText = await response.text();
        const parsed = parseMarkdown(rawText); // Ваша функция парсинга
        
        news.value = {
        title: parsed.meta.title || 'Без названия',
        date: parsed.meta.date || '',
        content: parsed.content
        };
    } catch (error) {
        console.error('Ошибка при получении новости:', error);
    } finally {
        loading.value = false;
    }
    });
  </script>
  
  <style scoped>
  /* Стили для красивого отображения медиафайлов */
  .news-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  .news-content :deep(img), 
  .news-content :deep(video) {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 15px 0;
  }
  .news-content :deep(p) {
    line-height: 1.6;
    font-size: 18px;
  }
  </style>
  
  