<script setup>
import { ref, onMounted } from 'vue'
import HeroSlider from '../components/HeroSlider.vue'
import ProductCard from '../components/ProductCard.vue'
// Импортируем функцию API
import { getPopularProducts } from '../api/client.js'

const categories = [
  {
    id: 1,
    title: 'Масляные краски',
    subtitle: 'Классика живописи',
    image: 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?q=80&w=800&auto=format&fit=crop',
    link: { path: '/catalog', query: { category: 'Масло' } }
  },
  {
    id: 2,
    title: 'Акварель',
    subtitle: 'Легкость и прозрачность',
    image: 'https://images.unsplash.com/photo-1629196914375-f7e48f477b6d?q=80&w=800&auto=format&fit=crop',
    link: { path: '/catalog', query: { category: 'Акварель' } }
  },
  {
    id: 3,
    title: 'Кисти',
    subtitle: 'Инструменты мастера',
    image: 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=800&auto=format&fit=crop',
    link: { path: '/catalog', query: { category: 'Кисти' } }
  },
  {
    id: 4,
    title: 'Бумага и Холсты',
    subtitle: 'Основа творчества',
    image: 'https://republica.ru/upload/iblock/a19/58A9332.jpg',
    link: { path: '/catalog', query: { category: 'Бумага' } }
  }
]

// Инициализируем пустым массивом
const popularProducts = ref([])

// Загружаем данные при монтировании компонента
onMounted(async () => {
  popularProducts.value = await getPopularProducts()
})
</script>

<template>
  <div class="bg-paper min-h-screen text-charcoal pb-24">
    <HeroSlider />
    
    <section class="py-24">
      <div class="container mx-auto px-6">
        <div class="text-center mb-16">
          <h2 class="font-serif text-4xl md:text-5xl italic mb-4">Начните свой путь</h2>
          <p class="text-stone-500 font-light text-lg">Всё необходимое для каждого этапа.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <router-link v-for="category in categories" :key="category.id" :to="category.link" class="group relative aspect-[16/9] overflow-hidden rounded-sm block">
            <img :src="category.image" :alt="category.title" class="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-105">
            <div class="absolute inset-0 bg-black/20 group-hover:bg-black/30 transition-colors"></div>
            <div class="absolute inset-0 flex flex-col justify-center items-center text-center p-4 text-white">
              <h3 class="font-serif text-4xl italic drop-shadow-md">{{ category.title }}</h3>
              <p class="font-light mt-2 opacity-80">{{ category.subtitle }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <section class="bg-white py-24 border-y border-stone-100">
      <div class="container mx-auto px-6">
        <div class="flex flex-col md:flex-row justify-between items-end mb-12">
          <h2 class="font-serif text-3xl italic">Выбор художников</h2>
          <router-link to="/catalog" class="text-clay hover:text-charcoal transition-colors border-b border-clay pb-1 text-sm uppercase tracking-wider mt-4 md:mt-0">Смотреть всё</router-link>
        </div>
        
        <div v-if="popularProducts.length === 0" class="text-center py-12 text-stone-400 font-light">
          Загрузка шедевров...
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <ProductCard v-for="product in popularProducts" :key="product.id" :product="product" />
        </div>
      </div>
    </section>

    <section class="py-24 bg-paper">
      <div class="container mx-auto px-6">
        
        <div class="mb-16">
          <h2 class="font-serif text-4xl md:text-5xl italic text-charcoal max-w-xl leading-tight">
            Магазин товаров <br> для художников
          </h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
          
          <div class="flex flex-col gap-8">
            <div class="bg-stone-800 text-white p-8 md:p-10 rounded-[1.5rem] hover:bg-stone-700 transition-colors duration-500 relative overflow-hidden group">
              <img src="https://images.unsplash.com/photo-1515964724036-7c390234a908?q=80&w=400&auto=format&fit=crop" 
                   class="absolute -bottom-10 -right-10 w-48 opacity-10 rotate-12 grayscale pointer-events-none" alt="pencil">
              <h3 class="font-serif text-2xl italic mb-6 leading-snug relative z-10">
                Почему большинство художников выбирает art.shop?
              </h3>
              <div class="font-light leading-relaxed text-stone-200 space-y-4 relative z-10 text-sm md:text-base">
                <p><strong class="text-white font-medium">art.shop</strong> — это пространство для профессиональных художников и творческих людей в Курске.</p>
                <p>Приходите в гости в наш уютный арт-маркет или закажите материалы онлайн.</p>
                <p class="pt-2 text-clay italic">Кисти, краски, маркеры для скетчинга, мольберты и скетчбуки — у нас есть всё!</p>
              </div>
            </div>

            <div class="bg-stone-100 p-8 md:p-10 rounded-[1.5rem] hover:bg-stone-200 transition-colors duration-500">
              <h3 class="font-serif text-2xl italic mb-4 text-charcoal">Редкие и эксклюзивные</h3>
              <div class="text-stone-600 font-light leading-relaxed space-y-4 text-sm md:text-base">
                <p>Материалы из Европы, Америки, Японии, а также проверенные Российские бренды.</p>
                <p>Мы находим то, что сложно достать, чтобы вы могли творить без ограничений и компромиссов.</p>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-8 md:mt-24">
            <div class="bg-stone-100 p-8 md:p-10 rounded-[1.5rem] hover:bg-stone-200 transition-colors duration-500">
              <h3 class="font-serif text-2xl italic mb-4 text-charcoal">Всё для художников</h3>
              <div class="text-stone-600 font-light leading-relaxed space-y-4 text-sm md:text-base">
                <p>Бережная доставка и упаковка. Мы работаем с художественными материалами много лет — ничего не повредится и не помнется.</p>
                <p>Более 60 000 товаров со всего мира — это так много, что не уместить даже на футбольном поле.</p>
              </div>
            </div>

            <div class="bg-stone-100 p-8 md:p-10 rounded-[1.5rem] hover:bg-stone-200 transition-colors duration-500">
              <h3 class="font-serif text-2xl italic mb-4 text-charcoal">Бонусы и подарки</h3>
              <ul class="text-stone-600 font-light leading-relaxed space-y-2 text-sm md:text-base list-disc list-inside marker:text-clay">
                <li>Оплачивайте товары бонусными рублями.</li>
                <li>Получайте подарки и бесплатные образцы материалов при покупке.</li>
                <li>Доступ к закрытым распродажам.</li>
                <li>Клуб привилегий в нашем Telegram-канале.</li>
              </ul>
            </div>
          </div>

        </div>
      </div>
    </section>

  </div>
</template>