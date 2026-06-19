<template>
    <div v-if="!currentUserSteamId" class="auth-alert-banner">
      <span style="font-weight: 500;">Вы не авторизованы! Форма не отправится, пока вы не войдете в систему.</span>
      <a 
        :href="steamLoginUrl"
        style="background-color: #1b2838; color: #ffffff; border: 1px solid #c7d5e0; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; transition: background 0.2s;"
        onmouseover="this.style.background='#2a475e'"
        onmouseout="this.style.background='#1b2838'"
      >
        Login
      </a>
    </div>

    <div class="form-wrapper pattern-backdrop" v-if="formConfig">
      <h2 style="margin-bottom: 30px;">{{ formConfig.formTitle }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <!-- Добавлен динамический класс для чекбокса -->
        <div 
          v-for="field in formConfig.fields" 
          :key="field.id" 
          class="form-group"
          :class="{ 'is-checkbox': field.type === 'checkbox' }"
        >
          
          <!-- Стандартный лейбл для текстовых полей и селектов (сверху) -->
          <label v-if="field.type !== 'checkbox'" :for="field.id">
            {{ field.label }} <span v-if="field.required" class="required">*</span>
          </label>
          
          <!-- Текстовые поля и числа -->
          <input 
            v-if="['text', 'number', 'email'].includes(field.type)"
            :type="field.type"
            :id="field.id"
            :placeholder="field.placeholder"
            :required="field.required"
            v-model="formData[field.id]"
          />
  
          <!-- Выпадающий список -->
          <select 
            v-else-if="field.type === 'select'"
            :id="field.id"
            :required="field.required"
            v-model="formData[field.id]"
          >
            <option value="" disabled selected>Выберите вариант...</option>
            <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
          </select>
  
          <!-- Чекбокс и его лейбл в одну строку (исправлено) -->
          <template v-else-if="field.type === 'checkbox'">
            <input 
              type="checkbox"
              :id="field.id"
              :required="field.required"
              v-model="formData[field.id]"
            />
            <label :for="field.id">
              {{ field.label }} <span v-if="field.required" class="required">*</span>
            </label>
          </template>
  
        </div>
  
        <button type="submit" :disabled="submitting" class="send-button">
          {{ submitting ? 'Send...' : 'Send' }}
        </button>
      </form>
      
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
    <div v-else>Загрузка формы...</div>
  </template>
  
  <script setup>
  import { ref, onMounted, inject, computed } from 'vue';
  import { useRoute } from 'vue-router';

  const currentUserSteamId = inject('currentUserSteamId', ref(null))

  const steamLoginUrl = inject('steamLoginUrl')
  
  const route = useRoute();
  const formConfig = ref(null);
  const formData = ref({});
  const submitting = ref(false);
  const successMessage = ref('');
  
  const S3_BUCKET_URL = 'https://racehub.s3.cloud.ru/forms';
  
  onMounted(async () => {
    console.log('Текущий Steam ID:', currentUserSteamId.value)
  
    if (currentUserSteamId.value == null) {
      console.log('Пользователь не авторизован, вызываем steamLoginUrl...')
      window.open(steamLoginUrl.value)
      
    }
    const formId = route.params.id;
    try {
      const response = await fetch(`${S3_BUCKET_URL}/${formId}.json`);
      const config = await response.json();
      formConfig.value = config;
      
      config.fields.forEach(field => {
        formData.value[field.id] = field.type === 'checkbox' ? false : '';
      });
    } catch (e) {
      console.error("Ошибка загрузки конфига формы:", e);
    }
  });
  
  const handleSubmit = async () => {
    submitting.value = true;
    successMessage.value = '';
    
    const payload = {
      form_id: formConfig.value.formId,
      submitted_at: new Date().toISOString(),
      data: formData.value,
      steamId: currentUserSteamId.value
    };
  
    try {
      const response = await fetch(formConfig.value.submitUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
  
      if (response.ok) {
        successMessage.value = 'Форма успешно отправлена!';
        Object.keys(formData.value).forEach(key => {
          formData.value[key] = typeof formData.value[key] === 'boolean' ? false : '';
        });
      } else {
        alert('Ошибка при отправке на бэкенд');
      }
    } catch (error) {
      console.error(error);
    } finally {
      submitting.value = false;
    }
  };
  </script>
  
  <style scoped>
  .form-wrapper { 
    max-width: 500px; 
    margin: 0 auto; 
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 12px;
    }
  .form-group { margin-bottom: 15px; display: flex; flex-direction: column;}
  
  /* Стили для строки с чекбоксом */
  .form-group.is-checkbox {
    flex-direction: row;      /* Элементы встают в одну строку */
    align-items: center;      /* Выравнивание по центру по вертикали */
    gap: 10px;                /* Отступ между чекбоксом и текстом */
  }
  
  /* Убираем верхний отступ у лейбла и инпута внутри строки чекбокса */
  .form-group.is-checkbox label,
  .form-group.is-checkbox input {
    margin: 0;
    cursor: pointer;
  }
  
  .required { color: rgb(255, 255, 255);  }
  .success { color: green; font-weight: bold; margin-top: 15px; }
  
  input, select { 
    padding: 8px; 
    margin-top: 5px; 
    border: 1px solid rgba(255, 255, 255, 0.25); 
    background: rgb(20, 20, 20);
    border-radius: 12px;
    padding: 5px 15px;
    font-size: 16px;  
    font-weight: 400;
    font-family: "Titillium Web", Arial, Helvetica, sans-serif;
  }
  
  button { padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 4px; }
  button:disabled { background: #ccc; }
  .send-button {
    font-weight: 700;
  }


  .auth-alert-banner {
  max-width: 500px;         /* Точно такая же ширина, как у .form-wrapper */
  margin: 0 auto 20px auto; /* Центрирование и отступ 20px снизу до формы */
  padding: 15px 20px;
  background-color: #ff4757;
  color: #ffffff;
  border-radius: 12px;      /* Скругление как у вашей формы */
  font-family: "Titillium Web", Arial, sans-serif;
  display: flex;
  flex-direction: column;   /* На мобильных элементы встанут друг под друга */
  gap: 12px;
  align-items: center;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Кнопка внутри плашки */
.auth-alert-button {
  background-color: #1b2838;
  color: #ffffff;
  border: 1px solid #c7d5e0;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  width: 100%;             /* Кнопка на всю ширину на мобильных */
  max-width: 180px;        /* Ограничение ширины на десктопе */
}

.auth-alert-button:hover {
  background-color: #2a475e;
}

.auth-alert-button:active {
  transform: scale(0.98);
}

/* Медиа-запрос для красивого отображения на больших экранах */
@media (min-width: 480px) {
  .auth-alert-banner {
    flex-direction: row;    /* Текст и кнопка встают в одну строку */
    justify-content: space-between;
    text-align: left;
  }
  .auth-alert-button {
    width: auto;            /* Кнопка сжимается под свой контент */
  }
}

  </style>
  