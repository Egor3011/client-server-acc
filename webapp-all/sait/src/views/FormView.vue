<template>
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
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';

  const currentUserSteamId = inject('currentUserSteamId', ref(null))
  
  const route = useRoute();
  const formConfig = ref(null);
  const formData = ref({});
  const submitting = ref(false);
  const successMessage = ref('');
  
  const S3_BUCKET_URL = 'https://racehub.s3.cloud.ru/forms';
  
  onMounted(async () => {
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
  </style>
  