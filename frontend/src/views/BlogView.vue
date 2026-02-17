<script setup>
import { ref, computed, onMounted } from 'vue'

const activeCategory = ref('Все статьи')
const isLoading = ref(true)
const loadError = ref('')

const allPosts = ref([])

const categories = computed(() => {
  const base = ['Все статьи']
  const cats = Array.from(new Set(allPosts.value.map(p => String(p?.category || '').trim()).filter(Boolean)))
  return base.concat(cats)
})

const fetchBlog = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    const res = await fetch('/api/blog')
    if (!res.ok) {
      loadError.value = 'Не удалось загрузить журнал'
      allPosts.value = []
      return
    }
    const data = await res.json()
    allPosts.value = Array.isArray(data) ? data : []
  } catch (e) {
    loadError.value = 'Ошибка сети при загрузке журнала'
    allPosts.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchBlog()
})

const featuredPost = computed(() => {
  return allPosts.value.find(post => post.featured) || allPosts.value[0]
})

const filteredPosts = computed(() => {
  if (!featuredPost.value) return []

  let posts = allPosts.value.filter(post => post.id !== featuredPost.value.id)
  
  if (activeCategory.value !== 'Все статьи') {
    posts = posts.filter(post => post.category === activeCategory.value)
  }
  
  return posts
})
</script>

<template>
  <div class="bg-paper min-h-screen pb-24">
    <div class="container mx-auto px-6 py-12 md:py-20">
      
      <nav class="mb-10 text-xs uppercase tracking-widest text-stone-500">
        <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-charcoal">Журнал</span>
      </nav>

      <div class="mb-16 border-b border-sand pb-8">
        <h1 class="text-4xl md:text-6xl font-serif italic text-charcoal">Журнал об искусстве</h1>
        <p class="text-stone-500 font-light mt-4 text-lg max-w-2xl">
          Обзоры материалов, советы профессионалов и порция вдохновения для ваших будущих шедевров.
        </p>
      </div>

      <div v-if="isLoading" class="text-center py-20 text-stone-500 font-serif italic text-2xl">
        Загрузка журнала...
      </div>

      <div v-else-if="loadError" class="text-center py-20 text-stone-500 font-serif italic text-2xl">
        {{ loadError }}
      </div>

      <div v-else-if="!featuredPost" class="text-center py-20 text-stone-500 font-serif italic text-2xl">
        В журнале пока нет записей.
      </div>

      <router-link v-else :to="`/blog/${featuredPost.id}`" class="group block mb-20 relative bg-white border border-sand rounded-sm overflow-hidden hover:shadow-lg transition-all duration-500 hover:-translate-y-1">
        <div class="grid grid-cols-1 lg:grid-cols-2">
          <div class="aspect-video lg:aspect-auto h-full overflow-hidden bg-stone-100">
            <img :src="featuredPost.image" :alt="featuredPost.title" class="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-105">
          </div>
          <div class="p-8 lg:p-16 flex flex-col justify-center">
            <div class="flex items-center gap-4 text-xs uppercase tracking-widest text-stone-500 mb-6">
              <span class="text-clay font-medium">{{ featuredPost.category }}</span>
              <span>•</span>
              <span>{{ featuredPost.date }}</span>
            </div>
            <h2 class="text-3xl lg:text-4xl font-serif text-charcoal mb-6 leading-tight group-hover:text-clay transition-colors">
              {{ featuredPost.title }}
            </h2>
            <p class="text-stone-600 font-light leading-relaxed mb-10">
              {{ featuredPost.excerpt }}
            </p>
            <div class="flex items-center gap-2 text-charcoal text-sm uppercase tracking-widest font-medium group-hover:text-clay transition-colors">
              Читать статью 
              <svg class="w-4 h-4 transform group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
            </div>
          </div>
        </div>
      </router-link>

      <div class="flex flex-wrap gap-4 mb-12 border-b border-sand pb-6">
        <button 
          v-for="cat in categories" 
          :key="cat"
          @click="activeCategory = cat"
          class="px-5 py-2 rounded-full text-sm transition-all duration-300 border"
          :class="activeCategory === cat ? 'bg-charcoal text-white border-charcoal' : 'text-stone-500 border-sand hover:border-clay hover:text-charcoal'"
        >
          {{ cat }}
        </button>
      </div>

      <transition-group name="fade" tag="div" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-16">
        <router-link 
          v-for="post in filteredPosts" 
          :key="post.id" 
          :to="`/blog/${post.id}`" 
          class="group flex flex-col"
        >
          <div class="aspect-[4/3] overflow-hidden bg-stone-100 rounded-sm mb-6">
            <img :src="post.image" :alt="post.title" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
          </div>
          
          <div class="flex items-center justify-between text-xs uppercase tracking-widest text-stone-500 mb-4">
            <span class="text-clay">{{ post.category }}</span>
            <div class="flex items-center gap-3">
              <span>{{ post.date }}</span>
              <span>{{ post.readTime }}</span>
            </div>
          </div>
          
          <h3 class="text-2xl font-serif text-charcoal mb-4 leading-snug group-hover:text-clay transition-colors">
            {{ post.title }}
          </h3>
          <p class="text-stone-600 font-light text-sm leading-relaxed mb-6 line-clamp-3">
            {{ post.excerpt }}
          </p>
          
          <div class="mt-auto pt-4 border-t border-sand text-xs uppercase tracking-widest font-medium text-charcoal flex items-center gap-2 group-hover:text-clay transition-colors w-fit">
            Читать <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
          </div>
        </router-link>
      </transition-group>

      <div v-if="filteredPosts.length === 0" class="text-center py-20 text-stone-500 font-serif italic text-2xl">
        В этой рубрике пока нет записей.
      </div>

    </div>
  </div>
</template>

<style scoped>
.fade-move,
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
.fade-leave-active {
  position: absolute;
}
</style>