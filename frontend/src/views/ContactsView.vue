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
const isSending = ref(false)

async function submit() {
  sent.value = ''
  try {
    isSending.value = true
    const response = await store.sendContact(form)
    sent.value = response.message
    form.name = ''
    form.email = ''
    form.message = ''
  } catch {
    sent.value = ''
  } finally {
    isSending.value = false
  }
}

onMounted(async () => {
  await store.fetchContacts()
})
</script>

<template>
  <div class="bg-paper min-h-screen pb-24">
    <div class="container mx-auto px-6 py-12 md:py-20">

      <nav class="mb-10 text-xs uppercase tracking-widest text-stone-500">
        <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-charcoal">Контакты</span>
      </nav>

      <div class="mb-16 border-b border-sand pb-8">
        <h1 class="text-4xl md:text-6xl font-serif italic text-charcoal">Контакты</h1>
        <p class="text-stone-500 font-light mt-4 text-lg max-w-2xl">
          Заходите в мастерскую или напишите нам — ответим в течение дня.
        </p>
      </div>

      <div v-if="!store.contacts" class="text-center py-20 text-stone-500 font-serif italic text-2xl">
        Загрузка контактов...
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">

        <section class="lg:col-span-7 space-y-8">
          <div class="bg-white border border-sand rounded-sm shadow-sm overflow-hidden">
            <div class="aspect-[16/9] bg-stone-100 overflow-hidden">
              <img :src="store.contacts.photo" alt="Фото магазина" class="w-full h-full object-cover" />
            </div>

            <div class="p-8">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <div class="text-xs uppercase tracking-widest text-stone-500">Адрес</div>
                  <div class="text-charcoal mt-2 leading-relaxed">{{ store.contacts.address }}</div>
                </div>
                <div>
                  <div class="text-xs uppercase tracking-widest text-stone-500">Режим работы</div>
                  <div class="text-charcoal mt-2 leading-relaxed">{{ store.contacts.work_hours }}</div>
                </div>
                <div>
                  <div class="text-xs uppercase tracking-widest text-stone-500">Телефон</div>
                  <a :href="`tel:${String(store.contacts.phone || '').replace(/\s/g, '')}`" class="text-charcoal mt-2 inline-block hover:text-clay transition-colors">
                    {{ store.contacts.phone }}
                  </a>
                </div>
                <div>
                  <div class="text-xs uppercase tracking-widest text-stone-500">Email</div>
                  <a :href="`mailto:${store.contacts.email}`" class="text-charcoal mt-2 inline-block hover:text-clay transition-colors">
                    {{ store.contacts.email }}
                  </a>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white border border-sand rounded-sm shadow-sm overflow-hidden">
            <div class="px-8 py-6 border-b border-sand">
              <h2 class="text-2xl font-serif text-charcoal">Как нас найти</h2>
              <p class="text-stone-500 font-light mt-2">Постройте маршрут — вход со двора, рядом есть парковка.</p>
            </div>
            <div class="aspect-[16/10] bg-stone-100">
              <iframe
                :src="store.contacts.map_embed"
                title="Карта магазина"
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
                class="w-full h-full border-0"
              />
            </div>
          </div>
        </section>

        <aside class="lg:col-span-5">
          <div class="bg-white border border-sand rounded-sm shadow-sm overflow-hidden sticky top-28">
            <div class="px-8 py-6 border-b border-sand">
              <h2 class="text-2xl font-serif text-charcoal">Написать нам</h2>
              <p class="text-stone-500 font-light mt-2">Расскажите, что нужно — подберём материалы и ответим на вопросы.</p>
            </div>

            <form class="p-8 space-y-5" @submit.prevent="submit">
              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Имя</label>
                <input v-model="form.name" type="text" required class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Email</label>
                <input v-model="form.email" type="email" required class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Сообщение</label>
                <textarea v-model="form.message" rows="6" required class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm"></textarea>
              </div>

              <button type="submit" :disabled="isSending" class="w-full px-6 py-3 bg-charcoal text-white hover:bg-clay transition-colors uppercase tracking-widest text-xs font-medium rounded-sm disabled:opacity-60 disabled:cursor-not-allowed">
                {{ isSending ? 'Отправка...' : 'Отправить' }}
              </button>

              <div v-if="sent" class="border border-green-200 bg-green-50 text-green-700 px-4 py-3 rounded-sm text-sm">
                {{ sent }}
              </div>
              <div v-if="store.error" class="border border-red-200 bg-red-50 text-red-700 px-4 py-3 rounded-sm text-sm">
                {{ store.error }}
              </div>
            </form>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>
