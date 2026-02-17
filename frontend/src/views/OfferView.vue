<script setup>
const updatedAt = '17.02.2026'
</script>

<template>
  <div class="bg-paper min-h-screen pb-24">
    <div class="container mx-auto px-6 py-12 md:py-20">
      <nav class="mb-10 text-xs uppercase tracking-widest text-stone-500">
        <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-charcoal">Оферта</span>
      </nav>

      <div class="mb-12 border-b border-sand pb-8">
        <h1 class="text-4xl md:text-6xl font-serif italic text-charcoal">Публичная оферта</h1>
        <p class="text-stone-500 font-light mt-4 text-lg max-w-2xl">
          Условия продажи товаров интернет-магазина art.shop. Пожалуйста, ознакомьтесь перед оформлением заказа.
        </p>
        <p class="text-xs uppercase tracking-widest text-stone-400 mt-6">Обновлено: {{ updatedAt }}</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        <aside class="lg:col-span-4">
          <div class="bg-white border border-sand rounded-sm shadow-sm p-6 sticky top-28">
            <div class="text-xs uppercase tracking-widest text-stone-500">Навигация</div>
            <div class="mt-4 flex flex-col gap-3 text-sm">
              <a href="#terms" class="text-charcoal hover:text-clay transition-colors">1. Термины</a>
              <a href="#subject" class="text-charcoal hover:text-clay transition-colors">2. Предмет оферты</a>
              <a href="#order" class="text-charcoal hover:text-clay transition-colors">3. Оформление заказа</a>
              <a href="#payment" class="text-charcoal hover:text-clay transition-colors">4. Оплата</a>
              <a href="#delivery" class="text-charcoal hover:text-clay transition-colors">5. Доставка</a>
              <a href="#returns" class="text-charcoal hover:text-clay transition-colors">6. Возврат</a>
              <a href="#contacts" class="text-charcoal hover:text-clay transition-colors">7. Контакты</a>
            </div>
          </div>
        </aside>

        <section class="lg:col-span-8">
          <div class="bg-white border border-sand rounded-sm shadow-sm p-8 space-y-10 leading-relaxed text-stone-700">
            <section id="terms" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">1. Термины</h2>
              <p class="mt-3">
                «Продавец» — интернет-магазин art.shop. «Покупатель» — лицо, оформившее заказ на сайте.
                «Товар» — позиции, представленные в каталоге.
              </p>
            </section>

            <section id="subject" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">2. Предмет оферты</h2>
              <p class="mt-3">
                Продавец обязуется передать Товар Покупателю, а Покупатель обязуется оплатить и принять Товар
                на условиях настоящей оферты.
              </p>
            </section>

            <section id="order" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">3. Оформление заказа</h2>
              <div class="mt-3 space-y-3">
                <ul class="list-disc pl-5 space-y-2">
                  <li>Заказ оформляется через корзину на сайте.</li>
                  <li>После оформления Покупателю направляется подтверждение (если применимо).</li>
                  <li>Продавец вправе уточнить детали заказа по контактам Покупателя.</li>
                </ul>
              </div>
            </section>

            <section id="payment" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">4. Оплата</h2>
              <p class="mt-3">
                Способы оплаты указываются на странице оформления заказа. Все цены указаны в рублях.
              </p>
            </section>

            <section id="delivery" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">5. Доставка</h2>
              <p class="mt-3">
                Условия и сроки доставки зависят от выбранного способа и региона. Информация отображается при
                оформлении заказа.
              </p>
            </section>

            <section id="returns" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">6. Возврат</h2>
              <p class="mt-3">
                Возврат и обмен возможны в соответствии с законодательством РФ. Для оформления возврата свяжитесь
                с нами через контакты.
              </p>
            </section>

            <section id="contacts" class="scroll-mt-28">
              <h2 class="text-2xl font-serif text-charcoal">7. Контакты</h2>
              <p class="mt-3">
                Свяжитесь с нами на странице
                <router-link to="/contacts" class="text-charcoal underline decoration-sand hover:decoration-clay transition-colors">Контакты</router-link>.
              </p>
            </section>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
