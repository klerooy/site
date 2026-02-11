<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

import { useShopStore } from '../stores/shop'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const store = useShopStore()

const primaryImage = computed(() => props.product.images?.[0] || '')

function addQuick() {
  store.addToCart(props.product.id, 1)
}
</script>

<template>
  <article class="product-card card fade-up">
    <RouterLink :to="`/product/${product.id}`" class="product-image-wrap">
      <img :src="primaryImage" :alt="product.name" class="product-image" />
      <span class="product-tag" v-if="product.tags?.length">{{ product.tags[0] }}</span>
      <button class="quick-btn" type="button" @click.prevent="addQuick">Быстро в корзину</button>
    </RouterLink>

    <div class="product-content">
      <p class="product-brand">{{ product.brand }}</p>
      <RouterLink :to="`/product/${product.id}`" class="product-name">{{ product.name }}</RouterLink>
      <div class="product-meta">
        <span class="price">{{ product.price.toLocaleString('ru-RU') }} ₽</span>
        <span v-if="product.old_price" class="price-old">{{ product.old_price.toLocaleString('ru-RU') }} ₽</span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.product-card {
  overflow: hidden;
}

.product-image-wrap {
  position: relative;
  aspect-ratio: 1 / 1;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.45s ease;
}

.product-card:hover .product-image {
  transform: scale(1.06);
}

.product-tag {
  position: absolute;
  left: 12px;
  top: 12px;
  border-radius: 999px;
  padding: 5px 10px;
  background: rgba(255, 248, 235, 0.88);
  font-size: 0.8rem;
  color: var(--text-soft);
}

.quick-btn {
  position: absolute;
  left: 50%;
  bottom: 12px;
  transform: translateX(-50%) translateY(12px);
  opacity: 0;
  border: 1px solid rgba(255, 255, 255, 0.6);
  background: rgba(63, 57, 51, 0.72);
  color: #fff6e8;
  border-radius: 999px;
  padding: 8px 14px;
  cursor: pointer;
  transition: all 0.35s ease;
}

.product-card:hover .quick-btn {
  transform: translateX(-50%) translateY(0);
  opacity: 1;
}

.product-content {
  padding: 16px;
  display: grid;
  gap: 7px;
}

.product-brand {
  margin: 0;
  color: var(--text-soft);
  font-size: 0.85rem;
}

.product-name {
  font-weight: 600;
  transition: color 0.2s ease;
}

.product-name:hover {
  color: #866f57;
}

.product-meta {
  display: flex;
  gap: 10px;
  align-items: center;
}
</style>
