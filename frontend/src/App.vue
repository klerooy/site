<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterView, RouterLink, useRouter } from 'vue-router'
import { useShopStore } from './stores/shop'
import { api } from './api/client'
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'


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
    
    <SiteHeader />

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

    <SiteFooter />

  </div>
</template>