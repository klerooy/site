<script setup>
import { computed, onMounted, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import ProductCard from '../components/ProductCard.vue'
import { useShopStore } from '../stores/shop'

const store = useShopStore()
const route = useRoute()
const router = useRouter()

const filters = reactive({
  category: '',
  query: '',
  sort: 'new',
  type: '',
  brand: '',
  color: '',
  shape: '',
  size: '',
  hardness: ''
})

const filterLabels = {
  type: 'Тип',
  brand: 'Бренд',
  color: 'Цвет',
  shape: 'Форма',
  size: 'Размер',
  hardness: 'Твердость'
}

const sortOptions = [
  { value: 'new', label: 'Сначала новые' },
  { value: 'popular', label: 'По популярности' },
  { value: 'price_asc', label: 'Цена по возрастанию' },
  { value: 'price_desc', label: 'Цена по убыванию' }
]

const availableFilterKeys = computed(() => Object.keys(store.catalog.filters || {}))

function setFromRoute() {
  filters.category = String(route.query.category || '')
  filters.query = String(route.query.query || '')
  filters.sort = String(route.query.sort || 'new')
  filters.type = String(route.query.type || '')
  filters.brand = String(route.query.brand || '')
  filters.color = String(route.query.color || '')
  filters.shape = String(route.query.shape || '')
  filters.size = String(route.query.size || '')
  filters.hardness = String(route.query.hardness || '')
}

function createQuery() {
  const query = {}
  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      query[key] = value
    }
  })
  return query
}

async function fetchCatalog() {
  await store.fetchCatalog(createQuery())
}

function applyFilters() {
  router.replace({ name: 'catalog', query: createQuery() })
}

function resetFilters() {
  Object.keys(filters).forEach((key) => {
    filters[key] = key === 'sort' ? 'new' : ''
  })
  applyFilters()
}

onMounted(async () => {
  await store.fetchCategories()
  setFromRoute()
  await fetchCatalog()
})

watch(
  () => route.query,
  async () => {
    setFromRoute()
    await fetchCatalog()
  }
)
</script>

<template>
  <section class="section">
    <div class="container">
      <div class="catalog-head">
        <div>
          <h1 class="title">Каталог художественных материалов</h1>
          <p class="subtitle">Точные фильтры по категориям, брендам и свойствам материалов.</p>
        </div>
        <span class="pill">Найдено: {{ store.catalog.count }}</span>
      </div>

      <div class="catalog-layout">
        <aside class="filters card">
          <div class="filters-top">
            <h2>Фильтры</h2>
            <button type="button" class="btn btn-soft" @click="resetFilters">Сбросить</button>
          </div>

          <div class="filter-group">
            <label for="search">Поиск</label>
            <input id="search" v-model="filters.query" class="input" type="text" placeholder="Название, бренд, цвет" />
          </div>

          <div class="filter-group">
            <label for="category">Категория</label>
            <select id="category" v-model="filters.category" class="select">
              <option value="">Все категории</option>
              <option v-for="cat in store.categories" :key="cat.slug" :value="cat.slug">{{ cat.name }}</option>
            </select>
          </div>

          <div class="filter-group">
            <label for="sort">Сортировка</label>
            <select id="sort" v-model="filters.sort" class="select">
              <option v-for="option in sortOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>

          <div class="filter-group" v-for="key in availableFilterKeys" :key="key">
            <label :for="key">{{ filterLabels[key] || key }}</label>
            <select :id="key" v-model="filters[key]" class="select">
              <option value="">Все</option>
              <option
                v-for="value in store.catalog.filters[key]"
                :key="`${key}-${value}`"
                :value="value"
              >
                {{ value }}
              </option>
            </select>
          </div>

          <button class="btn btn-primary" type="button" @click="applyFilters">Применить фильтры</button>
        </aside>

        <div>
          <p v-if="store.error" class="notice">{{ store.error }}</p>

          <div class="product-grid" v-if="store.catalog.items.length">
            <ProductCard
              v-for="product in store.catalog.items"
              :key="product.id"
              :product="product"
            />
          </div>

          <div class="empty card" v-else>
            <h3>Ничего не найдено</h3>
            <p>Попробуйте изменить фильтры или снять часть ограничений.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.catalog-head {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 18px;
  margin-bottom: 26px;
}

.catalog-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
}

.filters {
  padding: 20px;
  position: sticky;
  top: 90px;
  align-self: start;
  display: grid;
  gap: 12px;
}

.filters-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters-top h2 {
  margin: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.9rem;
}

.filter-group {
  display: grid;
  gap: 6px;
}

.filter-group label {
  color: var(--text-soft);
  font-size: 0.88rem;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.empty {
  padding: 28px;
}

.empty h3 {
  margin: 0;
}

.empty p {
  color: var(--text-soft);
}

@media (max-width: 1100px) {
  .catalog-layout {
    grid-template-columns: 1fr;
  }

  .filters {
    position: static;
  }

  .product-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .catalog-head {
    flex-direction: column;
    align-items: start;
  }

  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
