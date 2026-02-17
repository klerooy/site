<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const emit = defineEmits(['close'])
const router = useRouter()
const query = ref('')
const suggestions = ref([])
const isLoading = ref(false)
let debounceTimer = null

// Функция для получения подсказок (ИСПРАВЛЕН URL)
const fetchSuggestions = async (val) => {
  if (!val || val.trim().length < 2) {
    suggestions.value = []
    return
  }
  isLoading.value = true
  try {
    // ИСПРАВЛЕНИЕ: Используем правильный эндпоинт /api/search/suggest
    const res = await fetch(`/api/search/suggest?q=${encodeURIComponent(val)}`)
    if (res.ok) {
      suggestions.value = await res.json()
    } else {
      suggestions.value = []
    }
  } catch (e) {
    console.error('Ошибка поиска:', e)
    suggestions.value = []
  } finally {
    isLoading.value = false
  }
}

// Задержка ввода, чтобы не отправлять запрос на каждую букву
watch(query, (newVal) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    fetchSuggestions(newVal)
  }, 300)
})

// Переход к товару при клике на результат
const handleSelect = (item) => {
  router.push(`/product/${item.id}`)
  emit('close')
}

// Переход при нажатии Enter (открываем первый товар, если он есть)
const handleSubmit = () => {
  if (suggestions.value.length > 0) {
    handleSelect(suggestions.value[0])
  }
}
</script>

<template>
  <div class="w-full max-w-3xl mx-auto">
    <h2 class="hidden md:block text-charcoal font-serif italic text-2xl mb-6 text-center">Что вы ищете сегодня?</h2>
    
    <form @submit.prevent="handleSubmit" class="relative group">

      <input
        v-model="query"
        type="text"
        placeholder="Название материала, цвет или бренд..."
        class="w-full bg-transparent border-b-2 border-stone-200 py-4 pl-10 pr-4 text-xl md:text-2xl font-serif text-charcoal placeholder:text-stone-300 placeholder:font-sans placeholder:text-lg placeholder:font-light focus:outline-none focus:border-clay transition-all duration-300"
        autofocus
      />
       
      <div v-if="isLoading" class="absolute right-0 top-1/2 -translate-y-1/2 text-clay">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    </form>

    <transition name="fade">
      <ul v-if="suggestions.length > 0" class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <li v-for="item in suggestions" :key="item.id">
          <button 
            @click="handleSelect(item)"
            class="w-full text-left p-4 flex items-center gap-4 rounded-sm border border-transparent hover:border-sand hover:bg-white transition-all group"
          >
            <div class="w-12 h-12 bg-stone-100 rounded-sm flex-shrink-0 overflow-hidden border border-sand group-hover:border-clay/30 transition-all relative">
              <img v-if="item.image" :src="item.image" class="w-full h-full object-cover">
              <div v-else class="w-full h-full flex justify-center items-center text-stone-300 text-xs">Нет</div>
            </div>
            
            <div class="overflow-hidden">
                <div class="font-serif text-lg text-charcoal group-hover:text-clay transition-colors leading-tight mb-1 truncate">
                  {{ item.name }}
                </div>
                <div class="text-xs uppercase tracking-widest text-stone-400 flex gap-2 truncate">
                    <span v-if="item.brand">{{ item.brand }}</span>
                    <span v-if="item.brand && item.color">•</span>
                    <span v-if="item.color">{{ item.color }}</span>
                </div>
            </div>
          </button>
        </li>
      </ul>
    </transition>
    
    <div v-if="query && query.length >= 2 && suggestions.length === 0 && !isLoading" class="mt-8 text-center text-stone-500 font-light">
        К сожалению, ничего не найдено по запросу "{{ query }}".
    </div>
  </div>
</template>

<style scoped>
input[type="search"]::-webkit-search-decoration,
input[type="search"]::-webkit-search-cancel-button,
input[type="search"]::-webkit-search-results-button,
input[type="search"]::-webkit-search-results-decoration { display: none; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>