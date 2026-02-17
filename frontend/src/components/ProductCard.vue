<script setup>
import { ref } from 'vue'
import { useShopStore } from '../stores/shop'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const shopStore = useShopStore()
const showToast = ref(false)

const handleAddToCart = async () => {
  await shopStore.addToCart(props.product.id, 1)
  
  showToast.value = true
  
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}
</script>

<template>
  <router-link :to="`/product/${product.id}`" class="group cursor-pointer block relative">
    
    <div class="aspect-[3/4] bg-stone-100 mb-4 overflow-hidden rounded-sm relative">
      <img 
        v-if="product.image"
        :src="product.image" 
        :alt="product.name" 
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        loading="lazy"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-stone-300">
        Нет фото
      </div>

      <button 
        @click.prevent="handleAddToCart"
        class="absolute bottom-4 right-4 bg-charcoal text-white w-11 h-11 rounded-full shadow-lg transition-all duration-300 hover:bg-clay flex items-center justify-center hover:scale-110 z-10"
        title="Добавить в коллекцию"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
      </button>
    </div>

    <div>
      <p class="text-xs text-stone-500 uppercase tracking-wider mb-1">{{ product.category }}</p>
      <h4 class="font-serif text-lg text-charcoal leading-tight mb-2 group-hover:text-clay transition-colors">
        {{ product.name }}
      </h4>
      <span class="text-charcoal font-medium">{{ product.price }} ₽</span>
    </div>
    
  </router-link>

  <transition name="toast">
    <div v-if="showToast" class="fixed bottom-10 right-10 bg-charcoal text-white px-8 py-5 rounded-sm shadow-2xl flex items-center gap-4 z-50 pointer-events-none">
      <svg class="w-6 h-6 text-clay" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      <span class="font-serif text-lg tracking-wide">Добавлено в коллекцию</span>
    </div>
  </transition>
</template>

<style scoped>
.toast-enter-active, .toast-leave-active {
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}
</style>