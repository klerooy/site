<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'

import ProductCard from '../components/ProductCard.vue'
import { useShopStore } from '../stores/shop'

const store = useShopStore()

onMounted(async () => {
  await store.fetchAccount()
})
</script>

<template>
  <section class="section" v-if="store.account">
    <div class="container">
      <h1 class="title">Личный кабинет</h1>
      <p class="subtitle">История заказов, избранное и накопленные бонусы.</p>

      <div class="account-grid">
        <article class="card profile-card">
          <h2>Профиль</h2>
          <p><strong>{{ store.account.profile.name }}</strong></p>
          <p>{{ store.account.profile.email }}</p>
          <p class="pill">Бонусы: {{ store.account.profile.bonuses }} баллов</p>
          <RouterLink class="btn btn-soft" to="/contacts">Связаться с менеджером</RouterLink>
        </article>

        <article class="card orders-card">
          <h2>История заказов</h2>
          <div class="order-list">
            <div v-for="order in store.account.orders" :key="order.id" class="order-item">
              <div>
                <strong>{{ order.id }}</strong>
                <p>{{ order.date }} · {{ order.status }}</p>
              </div>
              <div class="order-right">
                <span>{{ order.items.length }} поз.</span>
                <strong>{{ order.total.toLocaleString('ru-RU') }} ₽</strong>
              </div>
            </div>
          </div>
        </article>
      </div>

      <section class="section-tight">
        <div class="fav-head">
          <h2 class="title">Избранное</h2>
          <RouterLink to="/catalog" class="btn btn-soft">Перейти в каталог</RouterLink>
        </div>
        <div class="favorites-grid">
          <ProductCard v-for="item in store.account.favorites" :key="item.id" :product="item" />
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.account-grid {
  margin-top: 20px;
  display: grid;
  gap: 20px;
  grid-template-columns: 0.9fr 1.1fr;
}

.profile-card,
.orders-card {
  padding: 22px;
}

.profile-card h2,
.orders-card h2 {
  margin-top: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.9rem;
}

.order-list {
  display: grid;
  gap: 10px;
}

.order-item {
  border: 1px solid var(--stroke);
  border-radius: 12px;
  padding: 11px 12px;
  display: flex;
  justify-content: space-between;
  gap: 14px;
  background: rgba(255, 255, 255, 0.5);
}

.order-item p {
  margin: 3px 0 0;
  color: var(--text-soft);
}

.order-right {
  display: grid;
  justify-items: end;
  align-content: center;
  color: var(--text-soft);
}

.fav-head {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 18px;
}

.favorites-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

@media (max-width: 1080px) {
  .account-grid {
    grid-template-columns: 1fr;
  }

  .favorites-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .fav-head {
    flex-direction: column;
    align-items: start;
    gap: 8px;
  }

  .favorites-grid {
    grid-template-columns: 1fr;
  }
}
</style>
