<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterView, RouterLink, useRouter } from 'vue-router'
import { useShopStore } from './stores/shop'
import { api } from './api/client'

const cartStore = useShopStore()

const router = useRouter()

const searchOpen = ref(false)
const searchQuery = ref('')
const searchItems = ref([])
const isSearching = ref(false)
const searchError = ref('')
const searchRootRef = ref(null)
const searchInputRef = ref(null)
let searchTimer

const canShowDropdown = computed(() => searchOpen.value && searchQuery.value.trim().length >= 2)

const fetchSearchSuggestions = async (q) => {
  const query = String(q || '').trim()
  if (query.length < 2) {
    searchItems.value = []
    return
  }
  isSearching.value = true
  searchError.value = ''
  try {
    searchItems.value = await api.getSuggestions(query)
  } catch (e) {
    searchItems.value = []
    searchError.value = 'Не удалось выполнить поиск'
  } finally {
    isSearching.value = false
  }
}

const onSearchInput = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    fetchSearchSuggestions(searchQuery.value)
  }, 220)
}

const closeSearch = () => {
  searchOpen.value = false
  searchError.value = ''
  searchItems.value = []
}

const openSearch = () => {
  searchOpen.value = true
  nextTick(() => {
    searchInputRef.value?.focus?.()
  })
}

const toggleSearch = () => {
  if (searchOpen.value) {
    closeSearch()
  } else {
    openSearch()
  }
}

const onSearchSubmit = async () => {
  const q = searchQuery.value.trim()
  if (!q) return

  await fetchSearchSuggestions(q)
  if (searchItems.value.length > 0) {
    const first = searchItems.value[0]
    searchQuery.value = ''
    closeSearch()
    router.push({ name: 'product', params: { id: first.id } })
    return
  }

  searchError.value = 'Товар не найден'
}

const chooseSearchItem = (item) => {
  searchQuery.value = ''
  closeSearch()
  router.push({ name: 'product', params: { id: item.id } })
}

const onGlobalKeydown = (e) => {
  if (e.key === 'Escape') {
    closeSearch()
  }
}

const closeIfOutside = (e) => {
  if (searchRootRef.value && !searchRootRef.value.contains(e.target)) {
    closeSearch()
  }
}

onMounted(() => {
  cartStore.fetchCart()
  document.addEventListener('keydown', onGlobalKeydown)
  document.addEventListener('click', closeIfOutside)
})

onBeforeUnmount(() => {
  clearTimeout(searchTimer)
  document.removeEventListener('keydown', onGlobalKeydown)
  document.removeEventListener('click', closeIfOutside)
})
</script>

<template>
  <div class="flex flex-col min-h-screen bg-paper text-charcoal font-sans selection:bg-clay selection:text-white">
    
    <header class="sticky top-0 z-50 bg-paper/90 backdrop-blur-sm border-b border-stone-100">
      <nav class="container mx-auto px-6 h-20 flex items-center justify-between">
        <RouterLink to="/" class="text-3xl font-serif italic font-bold tracking-tighter">
          art<span class="text-clay">.</span>shop
        </RouterLink>

        <div class="hidden md:flex gap-8 text-sm font-medium tracking-widest uppercase">
          <RouterLink to="/catalog" class="hover:text-clay transition-colors">Каталог</RouterLink>
          <RouterLink to="/blog" class="hover:text-clay transition-colors">Блог</RouterLink>
          <RouterLink to="/contacts" class="hover:text-clay transition-colors">Контакты</RouterLink>
        </div>

        <div class="flex items-center gap-6">
          <div ref="searchRootRef" class="relative">
            <button class="hover:text-clay" type="button" @click="toggleSearch" aria-label="Поиск">
            <span class="sr-only">Поиск</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 0 0114 0z"></path></svg>
            </button>
          </div>
          <RouterLink to="/cart" class="text-ink hover:text-clay transition-transform hover:scale-110 relative">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
            
            <transition name="scale">
              <span 
                v-if="cartStore.cartCount > 0"
                class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-clay rounded-full border border-paper"
              ></span>
            </transition>
          </RouterLink>
          <RouterLink to="/account" class="text-ink hover:text-clay transition-transform hover:scale-110">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
          </RouterLink>
        </div>
      </nav>
    </header>

    <main class="flex-grow">
      <RouterView />
    </main>

    <div v-if="searchOpen" class="fixed inset-0 z-[60] md:hidden">
      <div class="absolute inset-0 bg-charcoal/60" @click="closeSearch"></div>
      <div class="absolute inset-x-0 top-0 bg-paper border-b border-sand">
        <form class="container mx-auto px-6 py-4" @submit.prevent="onSearchSubmit">
          <div class="flex items-center gap-3">
            <input
              ref="searchInputRef"
              v-model="searchQuery"
              type="text"
              autocomplete="off"
              placeholder="Поиск по товарам"
              class="flex-1 bg-white border border-sand rounded-sm py-3 px-3 focus:outline-none focus:border-clay text-sm"
              @input="onSearchInput"
            />
            <button type="button" class="px-4 py-3 border border-sand text-charcoal hover:bg-stone-50 transition-colors uppercase tracking-widest text-xs font-medium rounded-sm" @click="closeSearch">
              Закрыть
            </button>
          </div>
          <div v-if="searchError" class="mt-3 text-sm text-red-600">
            {{ searchError }}
          </div>
        </form>
      </div>

      <div class="absolute inset-x-0 top-[84px] bottom-0 bg-paper">
        <div class="container mx-auto px-6 py-4 h-full overflow-y-auto">
          <div v-if="searchQuery.trim().length < 2" class="text-sm text-stone-500">
            Введите минимум 2 символа
          </div>
          <div v-else-if="isSearching" class="text-sm text-stone-500">
            Поиск...
          </div>
          <div v-else-if="searchItems.length === 0" class="text-sm text-stone-500">
            Ничего не найдено
          </div>
          <div v-else class="divide-y divide-sand/50">
            <button
              v-for="item in searchItems"
              :key="item.id"
              type="button"
              class="w-full text-left py-4"
              @click="chooseSearchItem(item)"
            >
              <div class="text-base text-charcoal font-medium">{{ item.name }}</div>
              <div class="text-xs text-stone-500 mt-1">{{ item.brand }}<span v-if="item.color"> · {{ item.color }}</span></div>
            </button>
          </div>
        </div>
      </div>
    </div>

<footer class="bg-paper-dark pt-20 pb-10 border-t border-sand">
      <div class="container mx-auto px-6">
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-16 mb-16">
          
          <div class="flex flex-col justify-between">
            <div>
              <h3 class="font-serif italic text-3xl mb-6">art.shop</h3>
              <p class="text-ink-light font-light max-w-sm leading-relaxed">
                Вдохновение в каждом инструменте. Мы создаем пространство, где творчество становится образом жизни.
              </p>
            </div>
            <div class="h-px w-24 bg-clay mt-10 md:mt-0"></div>
          </div>

          <div>
            <h4 class="font-serif text-xl mb-6">Оставайтесь на связи</h4>
            <p class="text-sm text-ink-light mb-4">Подпишитесь на новости и получите скидку 10% на первый заказ.</p>
            
            <form class="flex gap-4 mb-10 max-w-md">
              <input 
                type="email" 
                placeholder="Ваш email" 
                class="flex-1 bg-white border border-sand px-4 py-3 text-sm focus:outline-none focus:border-clay transition-colors rounded-sm placeholder:font-light"
              >
              <button 
                type="submit" 
                class="px-6 py-3 bg-ink text-white text-sm uppercase tracking-wider hover:bg-clay transition-colors rounded-sm"
              >
                Подписаться
              </button>
            </form>

            <div class="flex gap-6">
              <a href="#" class="text-ink-light hover:text-clay transition-colors text-sm uppercase tracking-widest border-b border-transparent hover:border-clay pb-0.5">Telegram</a>
              <a href="#" class="text-ink-light hover:text-clay transition-colors text-sm uppercase tracking-widest border-b border-transparent hover:border-clay pb-0.5">VKontakte</a>
              <a href="#" class="text-ink-light hover:text-clay transition-colors text-sm uppercase tracking-widest border-b border-transparent hover:border-clay pb-0.5">Pinterest</a>
            </div>
          </div>
        </div>

        <div class="border-t border-sand pt-8 flex flex-col md:flex-row justify-between items-center text-xs text-ink-light font-light uppercase tracking-widest">
          <p>&copy; 2026 art.shop. Все права защищены.</p>
          <div class="flex gap-8 mt-4 md:mt-0">
            <RouterLink to="/privacy" class="hover:text-clay transition-colors">Политика конфиденциальности</RouterLink>
            <RouterLink to="/offer" class="hover:text-clay transition-colors">Оферта</RouterLink>
          </div>
        </div>

      </div>
    </footer>

  </div>
</template>