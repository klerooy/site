<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ProductCard from '../components/ProductCard.vue'

const route = useRoute()
const product = ref(null)
const activePhoto = ref(0)
const isLoading = ref(true)

// Имитация загрузки детальных данных о товаре
onMounted(async () => {
  // В реальности здесь будет fetch(`/api/products/${route.params.id}`)
  setTimeout(() => {
    product.value = {
      id: 101,
      name: 'Набор акварели "Белые ночи"',
      brand: 'Невская Палитра',
      price: 2400,
      category: 'Акварель',
      description: 'Профессиональные художественные акварельные краски серии «Белые ночи» представляют собой тонкодисперсные суспензии пигментов и связующих, в состав которых входит гуммиарабик — признанный лучшим растительным клеем для приготовления художественных водных красок.',
      photos: [
        'https://images.unsplash.com/photo-1629196914375-f7e48f477b6d?auto=format&fit=crop&w=1000&q=80',
        'https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=1000&q=80',
        'https://images.unsplash.com/photo-1520420097861-e4959843b682?auto=format&fit=crop&w=1000&q=80'
      ],
      specs: [
        { label: 'Светостойкость', value: 'Высокая (***)' },
        { label: 'Количество цветов', value: '24 кюветы' },
        { label: 'Состав', value: 'Натуральный гуммиарабик' },
        { label: 'Производитель', value: 'Россия' }
      ],
      reviews: [
        { id: 1, user: 'Марина В.', date: '12.01.2026', text: 'Потрясающая пигментация. Цвета чистые, отлично смешиваются. Доставка в Курск за 2 дня!', rating: 5 },
        { id: 2, user: 'Алексей', date: '05.02.2026', text: 'Классика, которая не подводит. Упаковано было очень бережно.', rating: 5 }
      ],
      related: [
        { id: 103, name: 'Набор кистей белка', price: 1200, category: 'Кисти', image: 'https://images.unsplash.com/photo-1515462277126-2dd0c162007a?auto=format&fit=crop&w=500&q=80' },
        { id: 105, name: 'Бумага для акварели 300г', price: 600, category: 'Бумага', image: 'https://images.unsplash.com/photo-1544253907-7359992e2709?auto=format&fit=crop&w=500&q=80' }
      ]
    }
    isLoading.value = false
  }, 500)
})
</script>

<template>
  <div v-if="!isLoading && product" class="bg-paper min-h-screen pb-24">
    <div class="container mx-auto px-6 py-12 md:py-20">
      
      <nav class="mb-10 text-xs uppercase tracking-widest text-ink-light">
        <router-link to="/" class="hover:text-clay">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <router-link to="/catalog" class="hover:text-clay">{{ product.category }}</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-ink">{{ product.name }}</span>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 md:gap-24">
        
        <div class="lg:col-span-7">
          <div class="sticky top-24">
            <div class="aspect-[4/5] overflow-hidden bg-stone-100 rounded-sm mb-6">
              <transition name="fade" mode="out-in">
                <img :key="activePhoto" :src="product.photos[activePhoto]" class="w-full h-full object-cover" />
              </transition>
            </div>
            <div class="flex gap-4">
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
            <h1 class="text-4xl md:text-5xl mb-6 leading-tight">{{ product.name }}</h1>
            <p class="text-3xl font-light text-ink mb-8">{{ product.price }} ₽</p>
            
            <button class="w-full py-4 bg-ink text-white hover:bg-clay transition-colors uppercase tracking-widest text-sm font-medium">
              Добавить в корзину
            </button>
          </div>

          <div class="mb-12">
            <h3 class="font-serif text-xl mb-4 italic text-ink-light">О материале</h3>
            <p class="text-ink-light leading-relaxed font-light">
              {{ product.description }}
            </p>
          </div>

          <div class="bg-stone-50 p-8 rounded-sm mb-12">
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
            <h2 class="text-3xl font-serif italic mb-12 text-center md:text-left">Отзывы творцов</h2>
            <div class="space-y-12">
              <div v-for="review in product.reviews" :key="review.id" class="border-b border-sand/30 pb-8">
                <div class="flex justify-between items-center mb-4">
                  <span class="font-serif text-lg italic">{{ review.user }}</span>
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
            <h2 class="text-3xl font-serif italic mb-12">Дополните палитру</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
              <ProductCard 
                v-for="item in product.related" 
                :key="item.id" 
                :product="item" 
              />
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
  
  <div v-else class="h-screen flex items-center justify-center text-clay font-serif italic text-2xl">
    Открываем галерею...
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>