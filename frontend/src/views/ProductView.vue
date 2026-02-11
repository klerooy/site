<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'

import ProductCard from '../components/ProductCard.vue'
import { useShopStore } from '../stores/shop'

const store = useShopStore()
const route = useRoute()
const qty = ref(1)
const selectedImage = ref('')

const product = computed(() => store.currentProduct)
const techEntries = computed(() => Object.entries(product.value?.technical || {}))

async function loadProduct() {
  await store.fetchProduct(route.params.id)
  qty.value = 1
  selectedImage.value = product.value?.images?.[0] || ''
}

function changeImage(url) {
  selectedImage.value = url
}

function addToCart() {
  if (product.value) {
    store.addToCart(product.value.id, qty.value)
  }
}

onMounted(loadProduct)

watch(
  () => route.params.id,
  () => {
    loadProduct()
  }
)
</script>

<template>
  <section class="section" v-if="product">
    <div class="container">
      <RouterLink class="pill" to="/catalog">← Назад в каталог</RouterLink>

      <div class="product-layout">
        <div class="gallery card">
          <img :src="selectedImage || product.images[0]" :alt="product.name" class="main-image" />
          <div class="thumbs">
            <button
              v-for="img in product.images"
              :key="img"
              type="button"
              class="thumb"
              :class="{ active: (selectedImage || product.images[0]) === img }"
              @click="changeImage(img)"
            >
              <img :src="img" :alt="product.name" />
            </button>
          </div>
        </div>

        <div class="product-info card">
          <span class="pill">{{ product.brand }}</span>
          <h1 class="title">{{ product.name }}</h1>
          <p class="subtitle">{{ product.description }}</p>

          <div class="price-row">
            <span class="price">{{ product.price.toLocaleString('ru-RU') }} ₽</span>
            <span class="price-old" v-if="product.old_price">{{ product.old_price.toLocaleString('ru-RU') }} ₽</span>
          </div>

          <ul class="details-list">
            <li v-for="point in product.details" :key="point">{{ point }}</li>
          </ul>

          <div class="actions">
            <input v-model.number="qty" class="input qty" type="number" min="1" max="20" />
            <button class="btn btn-primary" type="button" @click="addToCart">Добавить в корзину</button>
          </div>

          <p v-if="store.error" class="notice">{{ store.error }}</p>
        </div>
      </div>

      <div class="product-extra">
        <article class="card spec-card">
          <h2>Технические детали</h2>
          <div class="spec-grid">
            <div v-for="([key, value]) in techEntries" :key="key">
              <dt>{{ key }}</dt>
              <dd>{{ value }}</dd>
            </div>
          </div>
        </article>

        <article class="card review-card">
          <h2>Отзывы покупателей</h2>
          <div class="reviews">
            <div v-for="review in product.reviews" :key="review.author + review.date" class="review-item">
              <strong>{{ review.author }}</strong>
              <small>{{ review.date }} · {{ review.rating }}/5</small>
              <p>{{ review.text }}</p>
            </div>
          </div>
        </article>
      </div>

      <section class="section-tight">
        <div class="related-head">
          <h2 class="title">Сопутствующие товары</h2>
          <RouterLink to="/catalog" class="btn btn-soft">Перейти в каталог</RouterLink>
        </div>
        <div class="related-grid">
          <ProductCard v-for="item in product.related" :key="item.id" :product="item" />
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.product-layout {
  margin-top: 18px;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 24px;
}

.gallery {
  padding: 16px;
}

.main-image {
  width: 100%;
  height: 460px;
  border-radius: 14px;
  object-fit: cover;
}

.thumbs {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.thumb {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 0;
  overflow: hidden;
  background: transparent;
  cursor: pointer;
}

.thumb.active {
  border-color: rgba(134, 111, 87, 0.65);
}

.thumb img {
  width: 100%;
  height: 85px;
  object-fit: cover;
}

.product-info {
  padding: 26px;
}

.price-row {
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.details-list {
  margin: 18px 0;
  padding-left: 18px;
  color: var(--text-soft);
}

.actions {
  display: grid;
  grid-template-columns: 110px 1fr;
  gap: 10px;
}

.qty {
  text-align: center;
}

.product-extra {
  margin-top: 26px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.spec-card,
.review-card {
  padding: 20px;
}

.spec-card h2,
.review-card h2 {
  margin-top: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.9rem;
}

.spec-grid {
  display: grid;
  gap: 10px;
}

.spec-grid div {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-bottom: 1px dashed var(--stroke);
  padding-bottom: 8px;
}

.spec-grid dt {
  color: var(--text-soft);
}

.spec-grid dd {
  margin: 0;
}

.reviews {
  display: grid;
  gap: 12px;
}

.review-item {
  border: 1px solid var(--stroke);
  border-radius: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.5);
}

.review-item small {
  color: var(--text-soft);
}

.review-item p {
  margin: 6px 0 0;
}

.related-head {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 20px;
}

.related-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

@media (max-width: 1100px) {
  .product-layout,
  .product-extra {
    grid-template-columns: 1fr;
  }

  .related-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .related-head {
    flex-direction: column;
    align-items: start;
    gap: 10px;
  }

  .related-grid {
    grid-template-columns: 1fr;
  }

  .actions {
    grid-template-columns: 1fr;
  }
}
</style>
