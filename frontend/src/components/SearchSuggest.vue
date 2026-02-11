<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { useShopStore } from '../stores/shop'

const router = useRouter()
const store = useShopStore()

const query = ref('')
const open = ref(false)
const rootRef = ref(null)
let debounceTimer

watch(query, (value) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    store.fetchSuggestions(value)
    open.value = value.trim().length >= 2
  }, 240)
})

function closeIfOutside(event) {
  if (rootRef.value && !rootRef.value.contains(event.target)) {
    open.value = false
  }
}

function submitSearch() {
  if (!query.value.trim()) {
    return
  }

  router.push({ name: 'catalog', query: { query: query.value.trim() } })
  open.value = false
}

function chooseSuggestion(item) {
  router.push({ name: 'product', params: { id: item.id } })
  query.value = ''
  open.value = false
}

onMounted(() => {
  document.addEventListener('click', closeIfOutside)
})

onBeforeUnmount(() => {
  clearTimeout(debounceTimer)
  document.removeEventListener('click', closeIfOutside)
})
</script>

<template>
  <div ref="rootRef" class="search-box">
    <form class="search-form" @submit.prevent="submitSearch">
      <label class="visually-hidden" for="site-search">Поиск по каталогу</label>
      <input
        id="site-search"
        v-model="query"
        class="search-input"
        type="text"
        placeholder="Поиск: бренд, цвет, название"
        autocomplete="off"
        @focus="open = query.trim().length >= 2"
      />
      <button type="submit" class="search-submit" aria-label="Искать">⌕</button>
    </form>

    <div v-if="open" class="search-dropdown card">
      <p v-if="store.suggestions.length === 0" class="search-empty">Ничего не найдено</p>
      <button
        v-for="item in store.suggestions"
        :key="item.id"
        type="button"
        class="search-item"
        @click="chooseSuggestion(item)"
      >
        <span>{{ item.name }}</span>
        <small>{{ item.brand }} · {{ item.color }}</small>
      </button>
    </div>
  </div>
</template>

<style scoped>
.search-box {
  position: relative;
  width: min(430px, 100%);
}

.search-form {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
}

.search-input {
  border: 1px solid var(--stroke);
  border-radius: 999px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.82);
  color: var(--text);
  font: inherit;
}

.search-input:focus {
  outline: none;
  border-color: rgba(126, 103, 83, 0.72);
}

.search-submit {
  width: 40px;
  border-radius: 50%;
  border: 1px solid var(--stroke);
  background: rgba(255, 255, 255, 0.85);
  color: var(--text-soft);
  font-size: 1.05rem;
  cursor: pointer;
  transition: transform 0.25s ease;
}

.search-submit:hover {
  transform: translateY(-1px);
}

.search-dropdown {
  position: absolute;
  z-index: 50;
  top: calc(100% + 10px);
  left: 0;
  width: 100%;
  border-radius: 14px;
  padding: 8px;
}

.search-item {
  width: 100%;
  border: 0;
  text-align: left;
  padding: 10px 12px;
  border-radius: 10px;
  background: transparent;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.search-item:hover {
  background: rgba(201, 159, 150, 0.18);
}

.search-item small {
  color: var(--text-soft);
}

.search-empty {
  margin: 6px;
  color: var(--text-soft);
}

@media (max-width: 760px) {
  .search-box {
    width: 100%;
  }
}
</style>
