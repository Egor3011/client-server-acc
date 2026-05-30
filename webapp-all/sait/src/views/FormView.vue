<template>
    <div class="form-wrapper" v-if="formConfig">
      <h2>{{ formConfig.formTitle }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <div v-for="field in formConfig.fields" :key="field.id" class="form-group">
          <label :for="field.id">{{ field.label }} <span v-if="field.required" class="required">*</span></label>
          
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
  
          <!-- Чекбокс -->
          <div v-else-if="field.type === 'checkbox'" class="checkbox-group">
            <input 
              type="checkbox"
              :id="field.id"
              :required="field.required"
              v-model="formData[field.id]"
            />
          </div>
        </div>
  
        <button type="submit" :disabled="submitting">
          {{ submitting ? 'Отправка...' : 'Отправить' }}
        </button>
      </form>
      
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
    <div v-else>Загрузка формы...</div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  const formConfig = ref(null);
  const formData = ref({});
  const submitting = ref(false);
  const successMessage = ref('');
  
  const S3_BUCKET_URL = 'https://racehub.s3.cloud.ru/forms';
  
  onMounted(async () => {
    const formId = route.params.id; // Получаем имя файла из URL, например 'feedback_form'
    try {
      const response = await fetch(`${S3_BUCKET_URL}/${formId}.json`);
      const config = await response.json();
      formConfig.value = config;
      
      // Инициализируем пустые значения для реактивности vue
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
    
    // Формируем полезную нагрузку (payload) для бэкенда
    const payload = {
      form_id: formConfig.value.formId, // Чтобы бэкенд знал, какая это форма
      submitted_at: new Date().toISOString(),
      data: formData.value // Объект со всеми ответами пользователя
    };
  
    try {
      const response = await fetch(formConfig.value.submitUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
  
      if (response.ok) {
        successMessage.value = 'Форма успешно отправлена!';
        // Сброс формы
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
  .form-wrapper { max-width: 500px; margin: 0 auto; padding: 20px; }
  .form-group { margin-bottom: 15px; display: flex; flex-direction: column; }
  .checkbox-group { flex-direction: row; align-items: center; }
  .required { color: red; }
  .success { color: green; font-weight: bold; margin-top: 15px; }
  input, select { padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; }
  button { padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 4px; }
  button:disabled { background: #ccc; }
  </style>
  