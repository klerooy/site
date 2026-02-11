<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'

import HeroSlider from '../components/HeroSlider.vue'
import ProductCard from '../components/ProductCard.vue'
import { useShopStore } from '../stores/shop'

const store = useShopStore()

onMounted(async () => {
  if (!store.home) {
    await store.fetchHome()
  }
})
</script>

<template>
  <div>
    <section class="container page-hero section-tight" v-if="store.home">
      <HeroSlider :slides="store.home.slider" />
    </section>

    <section class="section" v-if="store.home">
      <div class="container">
        <div class="section-heading">
          <h2 class="title">Категории с настроением мастерской</h2>
          <p class="subtitle">Крупные подборки для быстрого старта и вдумчивого выбора.</p>
        </div>

        <div class="categories-grid">
          <RouterLink
            v-for="cat in store.home.categories"
            :key="cat.slug"
            class="category-card card"
            :to="`/catalog?category=${cat.slug}`"
          >
            <img :src="cat.image" :alt="cat.name" />
            <div class="category-overlay">
              <h3>{{ cat.name }}</h3>
              <p>{{ cat.description }}</p>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="section" v-if="store.home">
      <div class="container">
        <div class="section-heading">
          <h2 class="title">Хиты продаж</h2>
          <RouterLink class="btn btn-soft" to="/catalog?sort=popular">Смотреть всё</RouterLink>
        </div>

        <div class="products-grid">
          <ProductCard v-for="product in store.home.popular" :key="product.id" :product="product" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container help-grid card">
        <div>
          <span class="pill">Помощь в выборе</span>
          <h2 class="title">Не знаете, с чего начать?</h2>
          <p>
            Сервис подберет набор под ваш уровень: от первых скетчей до материалов для мастерской.
            Отдельно собрали подарочные решения и сертификаты.
          </p>
          <div class="help-actions">
            <RouterLink class="btn btn-primary" to="/specials">Наборы для новичков</RouterLink>
            <RouterLink class="btn btn-soft" to="/contacts">Получить консультацию</RouterLink>
          </div>
        </div>
        <img
          src="https://images.unsplash.com/photo-1453738773917-9c3eff1db985?auto=format&fit=crop&w=1400&q=80"
          alt="Творческий набор"
        />
      </div>
    </section>

    <section class="section" v-if="store.home">
      <div class="container">
        <div class="section-heading">
          <h2 class="title">Акции</h2>
          <p class="subtitle">Сезонные предложения и мягкие скидки на любимые материалы.</p>
        </div>
        <div class="products-grid">
          <ProductCard v-for="product in store.home.promotions" :key="product.id" :product="product" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container benefits-grid" v-if="store.home">
        <article v-for="item in store.home.benefits" :key="item.title" class="benefit card">
          <div class="benefit-icon">{{ item.icon }}</div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 20px;
  margin-bottom: 28px;
}

.categories-grid {
  display: grid;
  gap: 22px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.category-card {
  position: relative;
  overflow: hidden;
  min-height: 300px;
}

.category-card img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.category-card:hover img {
  transform: scale(1.05);
}

.category-overlay {
  position: absolute;
  inset: auto 0 0;
  padding: 20px;
  background: linear-gradient(to top, rgba(45, 37, 31, 0.78), rgba(45, 37, 31, 0.12));
  color: #fff6ec;
}

.category-overlay h3 {
  margin: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.8rem;
}

.category-overlay p {
  margin: 4px 0 0;
  color: rgba(255, 246, 236, 0.85);
}

.products-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.help-grid {
  padding: 36px;
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 24px;
  align-items: center;
}

.help-grid p {
  color: var(--text-soft);
  margin: 16px 0 24px;
}

.help-grid img {
  border-radius: 18px;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.help-actions {
  display: flex;
  gap: 12px;
}

.benefits-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.benefit {
  padding: 20px;
}

.benefit-icon {
  font-size: 1.5rem;
}

.benefit h3 {
  margin: 10px 0 8px;
}

.benefit p {
  margin: 0;
  color: var(--text-soft);
}

@media (max-width: 1100px) {
  .categories-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .products-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .benefits-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .section-heading {
    flex-direction: column;
    align-items: start;
  }

  .categories-grid,
  .products-grid,
  .benefits-grid {
    grid-template-columns: 1fr;
  }

  .help-grid {
    grid-template-columns: 1fr;
    padding: 22px;
  }

  .help-actions {
    flex-direction: column;
  }
}
</style>
