<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const currentSlide = ref(0)

const slides = [
  {
    image: 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=1920&auto=format&fit=crop',
    title: 'Искусство начинается здесь',
    subtitle: 'Вдохновение в каждом мазке'
  },
  {
    image: 'https://images.unsplash.com/photo-1520420097861-e4959843b682?q=80&w=1920&auto=format&fit=crop',
    title: 'Палитра вашей души',
    subtitle: 'Краски лучших мировых брендов'
  },
  {
    image: 'https://images.unsplash.com/photo-1515462277126-2dd0c162007a?q=80&w=1920&auto=format&fit=crop',
    title: 'Творите без границ',
    subtitle: 'Кисти, холсты и бумага премиум класса'
  }
]

let timer = null

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.length
}

onMounted(() => {
  timer = setInterval(nextSlide, 6000)
})

onBeforeUnmount(() => {
  clearInterval(timer)
})
</script>

<template>
  <div class="relative h-[80vh] w-full overflow-hidden bg-stone-200">
    <transition-group name="fade">
      <div 
        v-for="(slide, index) in slides" 
        :key="index"
        v-show="currentSlide === index"
        class="absolute inset-0 w-full h-full"
      >
        <div class="absolute inset-0 bg-black/30 z-10"></div>
        <img 
          :src="slide.image" 
          :alt="slide.title" 
          class="w-full h-full object-cover animate-slow-zoom"
        />
        
        <div class="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-4">
          <h2 class="font-serif text-5xl md:text-7xl text-white italic mb-4 drop-shadow-lg tracking-wide">
            {{ slide.title }}
          </h2>
          <p class="text-xl text-white/90 font-light tracking-widest uppercase mb-10">
            {{ slide.subtitle }}
          </p>
          <router-link 
            to="/catalog" 
            class="px-10 py-4 bg-white/90 text-charcoal hover:bg-white transition-all duration-500 font-serif text-lg rounded-sm uppercase tracking-wider"
          >
            Перейти в каталог
          </router-link>
        </div>
      </div>
    </transition-group>

    <div class="absolute bottom-10 left-0 right-0 z-30 flex justify-center gap-4">
      <button 
        v-for="(_, index) in slides" 
        :key="index"
        @click="currentSlide = index"
        class="w-3 h-3 rounded-full transition-all duration-300 border border-white"
        :class="currentSlide === index ? 'bg-white scale-125' : 'bg-transparent hover:bg-white/50'"
      ></button>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
@keyframes zoom {
  0% { transform: scale(1); }
  100% { transform: scale(1.05); }
}
.animate-slow-zoom {
  animation: zoom 8s infinite alternate ease-in-out;
}
</style>