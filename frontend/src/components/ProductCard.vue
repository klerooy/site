<script setup>
defineProps({
  product: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="group cursor-pointer">
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

      <button class="absolute bottom-4 right-4 bg-white text-charcoal w-10 h-10 rounded-full shadow-md opacity-0 group-hover:opacity-100 transition-all hover:bg-clay hover:text-white flex items-center justify-center transform translate-y-4 group-hover:translate-y-0 duration-300">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
      </button>
    </div>

    <div>
      <p class="text-xs text-stone-500 uppercase tracking-wider mb-1">{{ product.category }}</p>
      <h4 class="font-serif text-lg text-charcoal leading-tight mb-2 group-hover:text-clay transition-colors">
        {{ product.name }}
      </h4>
      <span class="text-charcoal font-medium">{{ product.price }} ₽</span>
    </div>
  </div>
</template>