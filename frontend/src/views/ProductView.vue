<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useShopStore } from '../stores/shop'
import ProductCard from '../components/ProductCard.vue'

const route = useRoute()
const shopStore = useShopStore()

const product = ref(null)
const activePhoto = ref(0)
const isLoading = ref(true)
const relatedProducts = ref([])

const showToast = ref(false)

const loadProduct = async (id) => {
  isLoading.value = true
  activePhoto.value = 0
  
  try {
    const response = await fetch(`/api/products/${id}`)
    
    if (response.ok) {
      const data = await response.json()
      product.value = {
        ...data,
        brand: data.brand || 'art.shop',
        description: data.description || 'Идеальный выбор для вашего творчества. Мы тщательно проверяем качество каждого материала.',
        photos: data.photos && data.photos.length > 0 ? data.photos : [data.image],
        specs: data.specs || [
          { label: 'Категория', value: data.category },
          { label: 'Артикул', value: data.id }
        ],
        reviews: data.reviews || [
          { id: 1, user: 'Тайный Художник', date: 'Недавно', text: 'Прекрасный материал, полностью оправдал ожидания!', rating: 5 }
        ]
      }
    } else {
      product.value = null
    }

    const relatedRes = await fetch('/api/products/popular')
    if (relatedRes.ok) {
      const allPopular = await relatedRes.json()
      relatedProducts.value = allPopular.filter(p => String(p.id) !== String(id)).slice(0, 2)
    }
  } catch (error) {
    product.value = null
  } finally {
    isLoading.value = false
  }
}

// Новая логика добавления в корзину
const handleAddToCart = async () => {
  if (product.value) {
    // 1. Ждем, пока бэкенд добавит товар
    await shopStore.addToCart(product.value.id, 1)
    
    // 2. Показываем красивое уведомление
    showToast.value = true
    
    // 3. Прячем через 3 секунды
    setTimeout(() => {
      showToast.value = false
    }, 3000)
  }
}

onMounted(() => {
  if (route.params.id) loadProduct(route.params.id)
})

watch(() => route.params.id, (newId) => {
  if (newId) {
    loadProduct(newId)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})
</script>

<template>
  <div v-if="!isLoading && product" class="bg-paper min-h-screen pb-24 relative">
    <div class="container mx-auto px-6 py-12 md:py-20">
      
      <nav class="mb-10 text-xs uppercase tracking-widest text-ink-light">
        <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <router-link to="/catalog" class="hover:text-clay transition-colors">{{ product.category }}</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-ink">{{ product.name }}</span>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 md:gap-24">
        
        <div class="lg:col-span-7">
          <div class="sticky top-24">
            <div class="aspect-[4/5] overflow-hidden bg-stone-100 rounded-sm mb-6 relative">
              <transition name="fade" mode="out-in">
                <img 
                  v-if="product.photos[activePhoto]" 
                  :key="activePhoto" 
                  :src="product.photos[activePhoto]" 
                  class="w-full h-full object-cover" 
                />
                <div v-else class="w-full h-full flex items-center justify-center text-stone-300">
                  Нет фото
                </div>
              </transition>
            </div>
            
            <div v-if="product.photos.length > 1" class="flex gap-4">
              <button 
                v-for="(photo, index) in product.photos" 
                :key="index"
                @click="activePhoto = index"
                class="w-20 h-20 overflow-hidden border transition-all"
                :class="activePhoto === index ? 'border-clay opacity-100' : 'border-transparent opacity-50 hover:opacity-80'"
              >
                <img :src="photo" class="w-full h-full object-cover" />
              </button>
            </div>
          </div>
        </div>

        <div class="lg:col-span-5 flex flex-col">
          <div class="border-b border-sand pb-8 mb-8">
            <p class="text-clay italic font-serif text-lg mb-2">{{ product.brand }}</p>
            <h1 class="text-4xl md:text-5xl mb-6 leading-tight text-charcoal">{{ product.name }}</h1>
            <p class="text-3xl font-light text-charcoal mb-8">{{ product.price }} ₽</p>
            
            <button 
              @click="handleAddToCart"
              class="w-full py-4 bg-charcoal text-white hover:bg-clay transition-all duration-300 uppercase tracking-widest text-sm font-medium rounded-sm shadow-md hover:shadow-lg hover:-translate-y-0.5"
            >
              Добавить в коллекцию
            </button>
          </div>

          <div class="mb-12">
            <h3 class="font-serif text-xl mb-4 italic text-ink-light">О материале</h3>
            <p class="text-ink-light leading-relaxed font-light">
              {{ product.description }}
            </p>
          </div>

          <div class="bg-paper-dark p-8 rounded-sm mb-12 border border-sand/50">
            <h3 class="font-serif text-xl mb-6 text-ink">Технические свойства</h3>
            <div class="space-y-4">
              <div v-for="spec in product.specs" :key="spec.label" class="flex justify-between border-b border-sand/50 pb-2 text-sm">
                <span class="text-ink-light font-light">{{ spec.label }}</span>
                <span class="text-ink font-medium">{{ spec.value }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-32 border-t border-sand pt-20">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-20">
          
          <div class="lg:col-span-7">
            <h2 class="text-3xl font-serif italic mb-12 text-center md:text-left text-ink">Отзывы творцов</h2>
            <div class="space-y-12">
              <div v-for="review in product.reviews" :key="review.id" class="border-b border-sand/30 pb-8">
                <div class="flex justify-between items-center mb-4">
                  <span class="font-serif text-lg italic text-ink">{{ review.user }}</span>
                  <span class="text-xs text-stone-400 uppercase tracking-tighter">{{ review.date }}</span>
                </div>
                <div class="flex text-clay mb-4">
                  <span v-for="i in 5" :key="i">{{ i <= review.rating ? '★' : '☆' }}</span>
                </div>
                <p class="text-ink-light font-light leading-relaxed italic">"{{ review.text }}"</p>
              </div>
            </div>
          </div>

          <div class="lg:col-span-5 lg:pl-10">
            <h2 class="text-3xl font-serif italic mb-12 text-ink">Дополните палитру</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
              <ProductCard 
                v-for="item in relatedProducts" 
                :key="item.id" 
                :product="item" 
              />
            </div>
          </div>

        </div>
      </div>
    </div>
    
    <transition name="toast">
      <div v-if="showToast" class="fixed bottom-10 right-10 bg-charcoal text-white px-8 py-5 rounded-sm shadow-2xl flex items-center gap-4 z-50">
        <svg class="w-6 h-6 text-clay" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        <span class="font-serif text-lg tracking-wide">Добавлено в коллекцию</span>
      </div>
    </transition>

  </div>
  
  <div v-else-if="isLoading" class="h-screen flex items-center justify-center text-clay font-serif italic text-2xl">
    Открываем шедевр...
  </div>

  <div v-else class="h-screen flex flex-col items-center justify-center text-center px-6">
    <h1 class="text-6xl font-serif italic text-ink mb-4">Упс!</h1>
    <p class="text-ink-light mb-8">Кажется, этот материал закончился или был спрятан в архивы.</p>
    <router-link to="/catalog" class="px-8 py-3 bg-charcoal text-white uppercase tracking-widest text-sm hover:bg-clay transition-colors">
      Вернуться в каталог
    </router-link>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Анимация для уведомления */
.toast-enter-active, .toast-leave-active {
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}
</style>