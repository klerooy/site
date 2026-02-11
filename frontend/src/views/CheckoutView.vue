<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

import { useShopStore } from '../stores/shop'

const store = useShopStore()

const form = reactive({
  full_name: '',
  phone: '',
  delivery_method: 'courier',
  payment_method: 'card',
  address: ''
})

const successMessage = ref('')
const orderId = ref('')

watch(
  () => form.delivery_method,
  async (value) => {
    await store.setDeliveryMethod(value)
  }
)

async function submit() {
  successMessage.value = ''
  orderId.value = ''

  try {
    const result = await store.checkout({ ...form })
    successMessage.value = result.message
    orderId.value = result.order.id
    form.full_name = ''
    form.phone = ''
    form.address = ''
  } catch {
    // Error already stored
  }
}

onMounted(async () => {
  await store.fetchCart()
  form.delivery_method = store.cart.delivery_method || 'courier'
})
</script>

<template>
  <section class="section">
    <div class="container">
      <h1 class="title">Оформление заказа</h1>
      <p class="subtitle">Выберите доставку и оплату, заполните данные получателя.</p>

      <div v-if="store.cart.detailed_items?.length" class="checkout-layout">
        <article class="card form-card">
          <h2>Данные получателя</h2>
          <form class="checkout-form" @submit.prevent="submit">
            <input v-model="form.full_name" class="input" type="text" placeholder="ФИО" required />
            <input v-model="form.phone" class="input" type="tel" placeholder="Телефон" required />

            <label>
              Способ доставки
              <select v-model="form.delivery_method" class="select">
                <option value="courier">Курьер</option>
                <option value="pickup">Самовывоз</option>
              </select>
            </label>

            <label>
              Способ оплаты
              <select v-model="form.payment_method" class="select">
                <option value="card">Банковская карта</option>
                <option value="sbp">СБП</option>
                <option value="cash">Наличными</option>
              </select>
            </label>

            <textarea
              v-if="form.delivery_method === 'courier'"
              v-model="form.address"
              class="textarea"
              rows="4"
              placeholder="Адрес доставки"
              required
            />

            <button class="btn btn-primary" type="submit">Подтвердить заказ</button>
          </form>

          <p v-if="successMessage" class="success">
            {{ successMessage }}
            <br />
            Номер: <strong>{{ orderId }}</strong>
          </p>

          <p v-if="store.error" class="notice">{{ store.error }}</p>
        </article>

        <aside class="card summary-card">
          <h2>Сумма к оплате</h2>
          <div class="summary-line" v-for="line in store.cart.detailed_items" :key="line.product.id">
            <span>{{ line.product.name }} × {{ line.qty }}</span>
            <strong>{{ line.line_total.toLocaleString('ru-RU') }} ₽</strong>
          </div>

          <div class="divider" />
          <div class="summary-line"><span>Товары</span><strong>{{ store.cart.subtotal.toLocaleString('ru-RU') }} ₽</strong></div>
          <div class="summary-line"><span>Скидка</span><strong>-{{ store.cart.discount.toLocaleString('ru-RU') }} ₽</strong></div>
          <div class="summary-line"><span>Доставка</span><strong>{{ store.cart.delivery_cost.toLocaleString('ru-RU') }} ₽</strong></div>
          <div class="summary-line total"><span>Итого</span><strong>{{ store.cart.total.toLocaleString('ru-RU') }} ₽</strong></div>
        </aside>
      </div>

      <div v-else class="card empty">
        <h3>Нечего оформлять</h3>
        <p>Корзина пустая, добавьте товары и вернитесь к оформлению.</p>
        <RouterLink class="btn btn-primary" to="/catalog">В каталог</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.checkout-layout {
  margin-top: 22px;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 20px;
}

.form-card,
.summary-card,
.empty {
  padding: 22px;
}

.form-card h2,
.summary-card h2 {
  margin-top: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
}

.checkout-form {
  display: grid;
  gap: 10px;
}

.checkout-form label {
  display: grid;
  gap: 6px;
  color: var(--text-soft);
}

.summary-line {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 14px;
  margin-bottom: 8px;
}

.divider {
  border-top: 1px solid var(--stroke);
  margin: 12px 0;
}

.summary-line.total {
  font-size: 1.04rem;
}

@media (max-width: 960px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
}
</style>
