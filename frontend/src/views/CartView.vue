<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import { useShopStore } from '../stores/shop'

const store = useShopStore()
const promo = ref('')

const items = computed(() => store.cart?.detailed_items || [])

async function inc(item) {
  await store.updateCartItem(item.product.id, item.qty + 1)
}

async function dec(item) {
  const next = Math.max(1, item.qty - 1)
  await store.updateCartItem(item.product.id, next)
}

async function remove(item) {
  await store.removeCartItem(item.product.id)
}

async function applyPromo() {
  if (!promo.value.trim()) {
    return
  }
  try {
    await store.applyPromo(promo.value)
    promo.value = ''
  } catch {
    // Error is handled in store.error
  }
}

onMounted(async () => {
  await store.fetchCart()
})
</script>

<template>
  <section class="section">
    <div class="container">
      <h1 class="title">Корзина</h1>
      <p class="subtitle">Проверьте состав заказа, промокод и способ доставки.</p>

      <div class="cart-layout" v-if="items.length">
        <article class="card cart-items">
          <div class="cart-line" v-for="line in items" :key="line.product.id">
            <img :src="line.product.images[0]" :alt="line.product.name" />
            <div>
              <h3>{{ line.product.name }}</h3>
              <p>{{ line.product.brand }}</p>
              <strong>{{ line.line_total.toLocaleString('ru-RU') }} ₽</strong>
            </div>

            <div class="qty-controls">
              <button type="button" @click="dec(line)">−</button>
              <span>{{ line.qty }}</span>
              <button type="button" @click="inc(line)">+</button>
            </div>

            <button type="button" class="remove" @click="remove(line)">Удалить</button>
          </div>
        </article>

        <aside class="card cart-summary">
          <h2>Ваш заказ</h2>

          <div class="promo-row">
            <input v-model="promo" class="input" type="text" placeholder="Промокод" />
            <button class="btn btn-soft" type="button" @click="applyPromo">Применить</button>
          </div>

          <div class="delivery">
            <label>
              <input
                type="radio"
                value="courier"
                :checked="store.cart.delivery_method === 'courier'"
                @change="store.setDeliveryMethod('courier')"
              />
              Курьер
            </label>
            <label>
              <input
                type="radio"
                value="pickup"
                :checked="store.cart.delivery_method === 'pickup'"
                @change="store.setDeliveryMethod('pickup')"
              />
              Самовывоз
            </label>
          </div>

          <div class="summary-line">
            <span>Товары</span>
            <strong>{{ store.cart.subtotal.toLocaleString('ru-RU') }} ₽</strong>
          </div>
          <div class="summary-line">
            <span>Скидка</span>
            <strong>-{{ store.cart.discount.toLocaleString('ru-RU') }} ₽</strong>
          </div>
          <div class="summary-line">
            <span>Доставка</span>
            <strong>{{ store.cart.delivery_cost.toLocaleString('ru-RU') }} ₽</strong>
          </div>
          <div class="summary-line total">
            <span>Итого</span>
            <strong>{{ store.cart.total.toLocaleString('ru-RU') }} ₽</strong>
          </div>

          <RouterLink class="btn btn-primary" to="/checkout">Оформить заказ</RouterLink>
          <p v-if="store.error" class="notice">{{ store.error }}</p>
        </aside>
      </div>

      <div class="card empty" v-else>
        <h3>Корзина пока пустая</h3>
        <p>Добавьте товары из каталога, и они появятся здесь.</p>
        <RouterLink class="btn btn-primary" to="/catalog">Перейти в каталог</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cart-layout {
  margin-top: 24px;
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 22px;
}

.cart-items,
.cart-summary {
  padding: 20px;
}

.cart-line {
  display: grid;
  grid-template-columns: 92px 1fr auto auto;
  gap: 14px;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px dashed var(--stroke);
}

.cart-line img {
  width: 92px;
  height: 92px;
  border-radius: 10px;
  object-fit: cover;
}

.cart-line h3 {
  margin: 0;
  font-size: 1rem;
}

.cart-line p {
  margin: 4px 0;
  color: var(--text-soft);
  font-size: 0.9rem;
}

.qty-controls {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.qty-controls button {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--stroke);
  background: rgba(255, 255, 255, 0.72);
  cursor: pointer;
}

.remove {
  border: 0;
  background: transparent;
  color: var(--danger);
  cursor: pointer;
}

.cart-summary h2 {
  margin-top: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
}

.promo-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
  margin-bottom: 12px;
}

.delivery {
  display: flex;
  gap: 14px;
  margin-bottom: 14px;
}

.delivery label {
  display: inline-flex;
  gap: 5px;
  align-items: center;
  color: var(--text-soft);
}

.summary-line {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.summary-line.total {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--stroke);
  font-size: 1.05rem;
}

.empty {
  margin-top: 24px;
  padding: 26px;
  max-width: 520px;
}

@media (max-width: 980px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 680px) {
  .cart-line {
    grid-template-columns: 1fr;
  }

  .promo-row {
    grid-template-columns: 1fr;
  }

  .delivery {
    flex-direction: column;
  }
}
</style>
