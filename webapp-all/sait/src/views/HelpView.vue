<template>
    <div class="faq-page">
      <div class="container">
        <h1 class="title">FAQ — Ответы на частые вопросы</h1>
  
        <div class="faq-list">
          <div
            v-for="(item, index) in faqs"
            :key="index"
            class="faq-item"
          >
            <button
              class="faq-question"
              @click="toggle(index)"
            >
              <span>{{ item.question }}</span>
              <span class="icon" :class="{ open: activeIndex === index }">
                +
              </span>
            </button>
  
            <transition
                @enter="enter"
                @leave="leave"
                >
                <div
                    v-if="activeIndex === index"
                    class="faq-answer"
                >
                    {{ item.answer }}
                </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const activeIndex = ref(null)
  
  const toggle = (index) => {
    activeIndex.value = activeIndex.value === index ? null : index
  }


  const enter = (el) => {
    el.style.height = '0'
    el.style.opacity = '0'

    requestAnimationFrame(() => {
        el.style.transition = 'all 0.25s ease'
        el.style.height = el.scrollHeight + 'px'
        el.style.opacity = '1'
    })
    }

    const leave = (el) => {
    el.style.height = el.scrollHeight + 'px'
    el.style.opacity = '1'

    requestAnimationFrame(() => {
        el.style.transition = 'all 0.2s ease'
        el.style.height = '0'
        el.style.opacity = '0'
    })
    }
  
  const faqs = [
    {
      question: 'Что делать, если меня выбили с трассы?',
      answer:
        'Сохраняйте контроль над машиной и безопасно вернитесь в гонку. После финиша можно подать протест.'
    },
    {
      question: 'Когда нужно возвращать позицию?',
      answer:
        'Если вы получили преимущество через контакт или срез трассы — позицию необходимо вернуть добровольно.'
    },
    {
      question: 'Можно ли защищаться от обгона?',
      answer:
        'Да, но допускается только одно изменение траектории.'
    },
    {
      question: 'Что считается опасным возвращением на трассу?',
      answer:
        'Возврат, при котором вы создаёте помеху или вынуждаете других пилотов резко менять траекторию.'
    },
    {
      question: 'Наказываются ли лёгкие контакты?',
      answer:
        'Зависит от ситуации. Если контакт повлиял на результат — вероятен штраф.'
    },
    {
      question: 'Как работает система штрафов?',
      answer:
        'Судьи анализируют инциденты после гонки и выносят решение: от предупреждения до дисквалификации.'
    },
    {
      question: 'Можно ли оспорить решение судей?',
      answer:
        'Как правило — нет. Решение считается окончательным.'
    },
    {
      question: 'Что делать, если у меня лаги или технические проблемы?',
      answer:
        'Если вы создаёте опасность — лучше покинуть гонку. Безопасность важнее результата.'
    },
    {
      question: 'Как правильно пропускать круговых?',
      answer:
        'Держите стабильную траекторию и не создавайте непредсказуемых движений.'
    },
    {
      question: 'Можно ли использовать всю ширину трассы?',
      answer:
        'Да, но с соблюдением лимитов (минимум два колеса в пределах трассы).'
    },
    {
      question: 'Что считается намеренным столкновением?',
      answer:
        'Любое действие, направленное на выведение соперника из гонки.'
    },
    {
      question: 'Есть ли система накопления штрафов?',
      answer:
        'Да, при повторных нарушениях санкции могут ужесточаться вплоть до бана.'
    }
  ]
  </script>
  
  <style scoped>
  .faq-page {
    min-height: 100vh;
    background: none;
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 40px 20px;
  }
  
  .container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .title {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 40px;
    letter-spacing: 0.5px;
  }
  
  .faq-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .faq-item {
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    overflow: hidden;
    background: #111;
    transition: border 0.2s ease;
  }
  
  .faq-item:hover {
    border-color: #444;
  }
  
  .faq-question {
    width: 100%;
    background: transparent;
    border: none;
    color: #fff;
    padding: 18px 20px;
    text-align: left;
    font-size: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
  }
  
  .faq-question:hover {
    background: #1a1a1a;
  }
  
  .icon {
    font-size: 20px;
    transition: transform 0.2s ease;
  }
  
  .icon.open {
    transform: rotate(45deg);
  }
  
  .faq-answer {
    overflow: hidden;
    padding: 0 20px;
    color: #cfcfcf;
    font-size: 15px;
    line-height: 1.5;
    }

    .faq-answer {
    padding-bottom: 18px;
    }
  
  .fade-enter-active,
  .fade-leave-active {
    transition: all 0.2s ease;
  }
  
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
    transform: translateY(-5px);
  }
  </style>