<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ProductCard from '../components/ProductCard.vue'

const products = ref([])
const isLoading = ref(true)

const activeCategory = ref('Все')
const activeSort = ref('popular')

const route = useRoute()
const router = useRouter()

const categories = ['Все', 'Акварель', 'Масло', 'Кисти', 'Холсты', 'Бумага']

const sortOptions = [
  { value: 'popular', label: 'Сначала популярные' },
  { value: 'new', label: 'Новинки' },
  { value: 'price_asc', label: 'Сначала дешевле' },
  { value: 'price_desc', label: 'Сначала дороже' }
]

const syncCategoryFromRoute = () => {
  const qCategory = String(route.query?.category || '').trim()
  if (!qCategory) {
    activeCategory.value = 'Все'
    return
  }
  activeCategory.value = categories.includes(qCategory) ? qCategory : 'Все'
}

const dynamicFilters = computed(() => {
  if (activeCategory.value === 'Акварель' || activeCategory.value === 'Масло') {
    return [
      { name: 'Бренд', options: ['Невская Палитра', 'Мастер-Класс', 'Van Gogh', 'Schmincke'] },
      { name: 'Форма выпуска', options: ['Кюветы', 'Тубы', 'Наборы'] }
    ]
  }
  if (activeCategory.value === 'Кисти') {
    return [
      { name: 'Ворс', options: ['Белка', 'Колонок', 'Синтетика', 'Щетина'] },
      { name: 'Форма', options: ['Круглая', 'Плоская', 'Флейц', 'Лайнер'] }
    ]
  }
  if (activeCategory.value === 'Бумага') {
    return [
      { name: 'Фактура', options: ['Fin (Мелкое зерно)', 'Torchon (Крупное зерно)', 'Satin (Гладкая)'] },
      { name: 'Плотность', options: ['200 г/м²', '300 г/м²'] }
    ]
  }
  return []
})

const fetchProducts = async () => {
  isLoading.value = true
  try {
    const params = new URLSearchParams()
    if (activeCategory.value !== 'Все') {
      params.append('category', activeCategory.value)
    }
    params.append('sort', activeSort.value)

    const res = await fetch(`/api/products?${params.toString()}`)
    if (res.ok) {
      const data = await res.json()
      products.value = data.items ? data.items : data 
    } else {
      products.value = []
    }
  } catch (error) {
    console.error('Ошибка загрузки каталога:', error)
    products.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  syncCategoryFromRoute()
  fetchProducts()
})

watch(() => route.query?.category, () => {
  syncCategoryFromRoute()
})

watch([activeCategory, activeSort], () => {
  fetchProducts()
})

const setCategory = async (cat) => {
  activeCategory.value = cat
  const nextQuery = { ...route.query }
  if (cat === 'Все') {
    delete nextQuery.category
  } else {
    nextQuery.category = cat
  }
  await router.replace({ path: '/catalog', query: nextQuery })
}

const resetFilters = () => {
  activeCategory.value = 'Все'
  activeSort.value = 'popular'
  router.replace({ path: '/catalog', query: {} })
}
</script>

<template>
  <div class="bg-paper min-h-screen pb-24">
    <div class="container mx-auto px-6 py-12 md:py-20">
      
      <nav class="mb-8 text-xs uppercase tracking-widest text-stone-500">
        <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-charcoal">Каталог</span>
      </nav>

      <div class="mb-12 border-b border-sand pb-8">
        <h1 class="text-4xl md:text-5xl font-serif italic text-charcoal">Коллекция материалов</h1>
        <p class="text-stone-500 font-light mt-4 text-lg">Инструменты, подобранные художниками для художников.</p>
      </div>

      <div class="flex flex-col lg:flex-row gap-12 lg:gap-20 items-start">
        
        <aside class="w-full lg:w-1/4 lg:sticky lg:top-28 flex flex-col gap-10">
          
          <div>
            <h3 class="font-serif text-2xl text-charcoal mb-6">Категории</h3>
            <ul class="space-y-2">
              <li v-for="cat in categories" :key="cat">
                <button 
                  @click="setCategory(cat)"
                  class="w-full text-left py-2 px-4 rounded-sm transition-all duration-300 uppercase tracking-widest text-sm font-medium"
                  :class="activeCategory === cat ? 'bg-charcoal text-white' : 'text-stone-500 hover:bg-stone-100 hover:text-charcoal'"
                >
                  {{ cat }}
                </button>
              </li>
            </ul>
          </div>

          <transition-group name="fade">
            <div v-for="filter in dynamicFilters" :key="filter.name">
              <h4 class="font-serif text-xl text-charcoal mb-4 border-b border-sand/50 pb-2">{{ filter.name }}</h4>
              <ul class="space-y-3">
                <li v-for="opt in filter.options" :key="opt" class="flex items-center gap-3">
                  <input 
                    type="checkbox" 
                    :id="opt" 
                    class="w-4 h-4 text-clay bg-white border-stone-300 rounded-sm focus:ring-clay cursor-pointer accent-clay"
                  >
                  <label :for="opt" class="text-sm font-light text-stone-600 cursor-pointer hover:text-clay transition-colors">
                    {{ opt }}
                  </label>
                </li>
              </ul>
            </div>
          </transition-group>

        </aside>

        <main class="w-full lg:w-3/4">
          
          <div class="flex flex-col sm:flex-row justify-between items-center bg-stone-50 py-4 px-6 rounded-sm mb-10">
            <div class="text-sm text-stone-500 font-light mb-4 sm:mb-0">
              Показано материалов: <span class="font-medium text-charcoal">{{ products.length }}</span>
            </div>
            
            <div class="flex items-center gap-4">
              <span class="text-xs uppercase tracking-widest text-stone-500">Сортировка:</span>
              <select 
                v-model="activeSort" 
                class="bg-transparent text-charcoal font-medium border-b border-stone-300 py-1 pr-6 focus:outline-none focus:border-clay cursor-pointer text-sm"
              >
                <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </div>
          </div>

          <div v-if="isLoading" class="flex justify-center items-center py-32">
            <div class="font-serif italic text-2xl text-clay animate-pulse">Ищем лучшие материалы...</div>
          </div>

          <div v-else-if="products.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
            <ProductCard 
              v-for="product in products" 
              :key="product.id" 
              :product="product" 
            />
          </div>

          <div v-else class="text-center py-32 bg-stone-50 rounded-sm">
            <h2 class="text-3xl font-serif italic text-charcoal mb-4">Материалы не найдены</h2>
            <p class="text-stone-500 font-light mb-8">Попробуйте изменить параметры фильтрации или выбрать другую категорию.</p>
            <button 
              @click="resetFilters"
              class="px-8 py-3 border border-charcoal text-charcoal hover:bg-charcoal hover:text-white transition-all duration-300 uppercase tracking-widest text-sm rounded-sm"
            >
              Сбросить фильтры
            </button>
          </div>

        </main>

      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>