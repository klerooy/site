<script setup>
import { onMounted, reactive, ref } from 'vue'

import { useShopStore } from '../stores/shop'

const store = useShopStore()

const form = reactive({
  name: '',
  email: '',
  message: ''
})

const sent = ref('')

async function submit() {
  sent.value = ''
  try {
    const response = await store.sendContact(form)
    sent.value = response.message
    form.name = ''
    form.email = ''
    form.message = ''
  } catch {
    sent.value = ''
  }
}

onMounted(async () => {
  await store.fetchContacts()
})
</script>

<template>
  <section class="section">
    <div class="container" v-if="store.contacts">
      <h1 class="title">Контакты</h1>
      <p class="subtitle">Заходите в магазин или напишите нам через форму обратной связи.</p>

      <div class="contact-layout">
        <article class="card contact-card">
          <img :src="store.contacts.photo" alt="Фото магазина" class="shop-photo" />
          <div class="contact-list">
            <p><strong>Адрес:</strong> {{ store.contacts.address }}</p>
            <p><strong>Телефон:</strong> {{ store.contacts.phone }}</p>
            <p><strong>Email:</strong> {{ store.contacts.email }}</p>
            <p><strong>Режим работы:</strong> {{ store.contacts.work_hours }}</p>
          </div>

          <div class="map-wrap">
            <iframe
              :src="store.contacts.map_embed"
              title="Карта магазина"
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            />
          </div>
        </article>

        <article class="card form-card">
          <h2>Форма обратной связи</h2>
          <form class="form-grid" @submit.prevent="submit">
            <input v-model="form.name" class="input" type="text" placeholder="Ваше имя" required />
            <input v-model="form.email" class="input" type="email" placeholder="Email" required />
            <textarea
              v-model="form.message"
              class="textarea"
              rows="6"
              placeholder="Чем можем помочь?"
              required
            />
            <button class="btn btn-primary" type="submit">Отправить</button>
          </form>

          <p v-if="sent" class="success">{{ sent }}</p>
          <p v-if="store.error" class="notice">{{ store.error }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.contact-layout {
  margin-top: 24px;
  display: grid;
  gap: 22px;
  grid-template-columns: 1.2fr 1fr;
}

.contact-card,
.form-card {
  padding: 22px;
}

.shop-photo {
  width: 100%;
  height: 240px;
  object-fit: cover;
  border-radius: 14px;
}

.contact-list {
  margin: 14px 0;
  color: var(--text-soft);
}

.map-wrap iframe {
  width: 100%;
  height: 260px;
  border: 0;
  border-radius: 14px;
}

.form-card h2 {
  margin: 0 0 14px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
}

.form-grid {
  display: grid;
  gap: 10px;
}

@media (max-width: 960px) {
  .contact-layout {
    grid-template-columns: 1fr;
  }
}
</style>
