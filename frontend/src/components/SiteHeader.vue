<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useShopStore } from '../stores/shop'
import SearchSuggest from './SearchSuggest.vue'

const cartStore = useShopStore()
const route = useRoute()

const searchOpen = ref(false)
const menuOpen = ref(false)
const headerRef = ref(null)

const toggleSearch = () => {
  searchOpen.value = !searchOpen.value
  if (searchOpen.value) {
    menuOpen.value = false
    document.body.style.overflow = window.innerWidth < 768 ? 'hidden' : ''
  } else {
    document.body.style.overflow = ''
  }
}

const closeSearch = () => {
  searchOpen.value = false
  document.body.style.overflow = ''
}

const closeIfOutside = (e) => {
  if (searchOpen.value && headerRef.value && !headerRef.value.contains(e.target) && window.innerWidth >= 768) {
    closeSearch()
  }
}

watch(route, () => {
  closeSearch()
  menuOpen.value = false
})

onMounted(() => {
  document.addEventListener('click', closeIfOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeIfOutside)
  document.body.style.overflow = ''
})
</script>

<template>
  <header ref="headerRef" class="sticky top-0 z-50 bg-paper/95 backdrop-blur-md border-b border-stone-200/50 shadow-sm relative">
    <nav class="container mx-auto px-6 h-20 flex items-center justify-between">
      
      <RouterLink to="/" class="text-3xl font-serif italic font-bold tracking-tighter flex-shrink-0 relative z-10">
        art<span class="text-clay">.</span>shop
      </RouterLink>

      <div class="hidden md:flex flex-1 justify-center gap-8 text-sm font-medium tracking-widest uppercase px-4 relative z-10">
        <RouterLink to="/catalog" class="hover:text-clay transition-colors whitespace-nowrap">Каталог</RouterLink>
        <RouterLink to="/blog" class="hover:text-clay transition-colors whitespace-nowrap">Блог</RouterLink>
        <RouterLink to="/contacts" class="hover:text-clay transition-colors whitespace-nowrap">Контакты</RouterLink>
        <RouterLink v-if="cartStore.isAdmin" to="/admin" class="text-clay font-bold hover:text-charcoal transition-colors whitespace-nowrap border-b-2 border-clay/30">
          Админ
        </RouterLink>
      </div>

      <div class="flex items-center justify-end gap-4 md:gap-6 flex-shrink-0 relative z-10">
        
        <button 
          type="button" 
          @click.stop="toggleSearch" 
          class="group flex items-center gap-2 hover:text-clay transition-colors p-1"
          aria-label="Поиск"
        >
          <span class="sr-only">Поиск</span>
          <svg class="w-5 h-5 text-charcoal group-hover:text-clay transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/>
          </svg>
          <span class="hidden md:block text-sm font-medium uppercase tracking-widest text-stone-500 group-hover:text-clay transition-colors">Поиск</span>
        </button>

        <RouterLink to="/cart" class="text-charcoal hover:text-clay transition-transform hover:scale-110 relative p-1 flex-shrink-0">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
          <transition name="scale">
            <span v-if="cartStore.cartCount > 0" class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-clay rounded-full border border-paper"></span>
          </transition>
        </RouterLink>

        <RouterLink to="/account" class="text-charcoal hover:text-clay transition-transform hover:scale-110 p-1 flex-shrink-0">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
        </RouterLink>

        <button @click="menuOpen = !menuOpen" class="md:hidden text-charcoal hover:text-clay transition-colors ml-2 p-1 flex-shrink-0">
          <svg v-if="!menuOpen" class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          <svg v-else class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
    </nav>

    <transition name="search-slide">
      <div v-if="searchOpen" class="absolute left-0 top-full w-full bg-paper border-b border-sand shadow-[0_20px_40px_-15px_rgba(0,0,0,0.1)] z-0">
        <div class="container mx-auto px-6 py-8 md:py-10 relative">
           <button class="md:hidden absolute top-4 right-4 text-stone-400 hover:text-charcoal p-2" @click="closeSearch">
             <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path></svg>
           </button>
           <SearchSuggest @close="closeSearch" />
        </div>
      </div>
    </transition>

    <transition name="slide-down">
      <div v-if="menuOpen" class="md:hidden bg-paper/95 backdrop-blur-md border-b border-sand px-6 py-8 absolute w-full left-0 top-full shadow-lg z-40">
        <nav class="flex flex-col gap-6 text-sm uppercase tracking-widest font-medium text-center">
          <RouterLink to="/catalog" class="text-stone-500 hover:text-clay transition-colors py-2" @click="menuOpen = false">Каталог</RouterLink>
          <RouterLink to="/blog" class="text-stone-500 hover:text-clay transition-colors py-2" @click="menuOpen = false">Блог</RouterLink>
          <RouterLink to="/contacts" class="text-stone-500 hover:text-clay transition-colors py-2" @click="menuOpen = false">Контакты</RouterLink>
          <RouterLink v-if="cartStore.isAdmin" to="/admin" class="text-clay font-bold py-2 border-b border-clay/20 inline-block mx-auto" @click="menuOpen = false">Панель управления</RouterLink>
        </nav>
      </div>
    </transition>
  </header>
</template>

<style scoped>
.search-slide-enter-active,
.search-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 500px;
  opacity: 1;
}

.search-slide-enter-from,
.search-slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

.slide-down-enter-active, .slide-down-leave-active { transition: all 0.3s ease-in-out; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-10px); }
.scale-enter-active, .scale-leave-active { transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); }
.scale-enter-from, .scale-leave-to { opacity: 0; transform: scale(0); }
</style>