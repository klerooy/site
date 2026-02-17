<script setup>
const updatedAt = '17.02.2026'
</script>

<template>
  <div class="bg-paper min-h-screen pb-24">
    <div class="container mx-auto px-6 py-12 md:py-20">
      <nav class="mb-10 text-xs uppercase tracking-widest text-stone-500">
        <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-charcoal">Политика конфиденциальности</span>
      </nav>

      <div class="mb-12 border-b border-sand pb-8">
        <h1 class="text-4xl md:text-6xl font-serif italic text-charcoal">Политика конфиденциальности</h1>
        <p class="text-stone-500 font-light mt-4 text-lg max-w-2xl">
          Мы бережно относимся к вашим данным и используем их только для работы магазина и улучшения сервиса.
        </p>
        <p class="text-xs uppercase tracking-widest text-stone-400 mt-6">Обновлено: {{ updatedAt }}</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        <aside class="lg:col-span-4">
          <div class="bg-white border border-sand rounded-sm shadow-sm p-6 sticky top-28">
            <div class="text-xs uppercase tracking-widest text-stone-500">Навигация</div>
            <div class="mt-4 flex flex-col gap-3 text-sm">
              <a href="#general" class="text-charcoal hover:text-clay transition-colors">1. Общие положения</a>
              <a href="#data" class="text-charcoal hover:text-clay transition-colors">2. Какие данные собираем</a>
              <a href="#purpose" class="text-charcoal hover:text-clay transition-colors">3. Цели обработки</a>
              <a href="#cookies" class="text-charcoal hover:text-clay transition-colors">4. Cookies</a>
              <a href="#rights" class="text-charcoal hover:text-clay transition-colors">5. Права пользователя</a>
              <a href="#contacts" class="text-charcoal hover:text-clay transition-colors">6. Контакты</a>
            </div>
          </div>
        </aside>

        <section class="lg:col-span-8">
          <div class="bg-white border border-sand rounded-sm shadow-sm p-8 space-y-10 leading-relaxed text-stone-700">
            <section id="general" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">1. Общие положения</h2>
              <p class="mt-3">
                Настоящая Политика описывает, какие данные мы можем получать при использовании сайта, и как мы их
                обрабатываем. Используя сайт, вы соглашаетесь с этой Политикой.
              </p>
            </section>

            <section id="data" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">2. Какие данные мы собираем</h2>
              <div class="mt-3 space-y-3">
                <p>Мы можем собирать:</p>
                <ul class="list-disc pl-5 space-y-2">
                  <li>контактные данные (имя, email, телефон), которые вы вводите при заказе или обращении;</li>
                  <li>данные о заказах (состав корзины, доставка, способ оплаты);</li>
                  <li>технические данные (IP-адрес, тип устройства/браузера, страницы переходов) — в обезличенном виде.</li>
                </ul>
              </div>
            </section>

            <section id="purpose" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">3. Цели обработки</h2>
              <div class="mt-3 space-y-3">
                <p>Мы используем данные для:</p>
                <ul class="list-disc pl-5 space-y-2">
                  <li>оформления и исполнения заказов;</li>
                  <li>поддержки пользователей и ответа на обращения;</li>
                  <li>улучшения качества сайта и пользовательского опыта;</li>
                  <li>информирования о статусе заказа и сервисных сообщениях.</li>
                </ul>
              </div>
            </section>

            <section id="cookies" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">4. Cookies</h2>
              <p class="mt-3">
                Cookies помогают сайту запоминать выбор пользователя (например, товары в корзине) и корректно
                функционировать. Вы можете ограничить использование cookies в настройках браузера.
              </p>
            </section>

            <section id="rights" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">5. Права пользователя</h2>
              <div class="mt-3 space-y-3">
                <p>Вы вправе запросить:</p>
                <ul class="list-disc pl-5 space-y-2">
                  <li>уточнение и обновление ваших данных;</li>
                  <li>удаление данных, если это не противоречит требованиям закона;</li>
                  <li>информацию об обработке данных.</li>
                </ul>
              </div>
            </section>

            <section id="contacts" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">6. Контакты</h2>
              <p class="mt-3">
                По вопросам, связанным с обработкой персональных данных, напишите нам через страницу
                <router-link to="/contacts" class="text-charcoal underline decoration-sand hover:decoration-clay transition-colors">Контакты</router-link>.
              </p>
            </section>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
