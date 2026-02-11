<script setup>
import { onMounted } from 'vue'

import ProductCard from '../components/ProductCard.vue'
import { useShopStore } from '../stores/shop'

const store = useShopStore()

onMounted(async () => {
  await store.fetchSpecials()
})
</script>

<template>
  <section class="section">
    <div class="container">
      <div class="specials-hero card">
        <h1 class="title">Специальные разделы</h1>
        <p class="subtitle">
          Подборки для новичков, подарочные наборы и сертификаты для тех, кто любит творчество.
        </p>
      </div>

      <article class="special-block" v-for="section in store.specials" :key="section.slug">
        <div class="special-meta">
          <img :src="section.image" :alt="section.title" />
          <div>
            <h2 class="title">{{ section.title }}</h2>
            <p class="subtitle">{{ section.description }}</p>
          </div>
        </div>

        <div class="special-grid">
          <ProductCard v-for="product in section.products" :key="product.id" :product="product" />
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.specials-hero {
  padding: 30px;
  margin-bottom: 24px;
}

.special-block {
  margin-bottom: 42px;
}

.special-meta {
  margin-bottom: 18px;
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 18px;
  align-items: center;
}

.special-meta img {
  width: 100%;
  height: 170px;
  border-radius: 16px;
  object-fit: cover;
}

.special-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

@media (max-width: 960px) {
  .special-meta {
    grid-template-columns: 1fr;
  }

  .special-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .special-grid {
    grid-template-columns: 1fr;
  }
}
</style>
