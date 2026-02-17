<script setup>
import { ref, onMounted } from 'vue'
import { useShopStore } from '../stores/shop'

const shopStore = useShopStore()
const isLoading = ref(true)
const promoInput = ref('')
const isUpdating = ref(false)

// Загрузка актуальной корзины при открытии страницы
onMounted(async () => {
  isLoading.value = true
  await shopStore.fetchCart()
  isLoading.value = false
})

// Управление количеством
const updateQty = async (productId, currentQty, delta) => {
  const newQty = currentQty + delta
  if (newQty < 1) return
  
  isUpdating.value = true
  await shopStore.updateCartItem(productId, newQty)
  isUpdating.value = false
}

// Удаление товара
const removeItem = async (productId) => {
  isUpdating.value = true
  await shopStore.removeCartItem(productId)
  isUpdating.value = false
}

// Выбор способа доставки
const changeDelivery = async (method) => {
  isUpdating.value = true
  await shopStore.setDeliveryMethod(method)
  isUpdating.value = false
}

// Применение промокода
const handleApplyPromo = async () => {
  if (!promoInput.value.trim()) return
  
  isUpdating.value = true
  try {
    await shopStore.applyPromo(promoInput.value)
    promoInput.value = '' // Очищаем поле после успешного применения
  } catch (error) {
    alert('Промокод недействителен или устарел.')
  } finally {
    isUpdating.value = false
  }
}

// Отмена промокода
const handleRemovePromo = async () => {
  isUpdating.value = true
  await shopStore.clearPromo()
  isUpdating.value = false
}
</script>

<template>
  <div class="bg-paper min-h-screen pb-24">
    <div class="container mx-auto px-6 py-12 md:py-20">
      
      <nav class="mb-10 text-xs uppercase tracking-widest text-stone-500">
        <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-charcoal">Коллекция</span>
      </nav>

      <div class="mb-12 border-b border-sand pb-8">
        <h1 class="text-4xl md:text-5xl font-serif italic text-charcoal">Ваша коллекция</h1>
      </div>

      <div v-if="isLoading" class="flex justify-center items-center py-32">
        <div class="font-serif italic text-2xl text-clay animate-pulse">Собираем материалы...</div>
      </div>

      <div v-else-if="!shopStore.cart?.detailed_items?.length" class="text-center py-20 bg-stone-50 rounded-sm">
        <h2 class="text-3xl font-serif italic text-charcoal mb-4">Здесь пока пусто</h2>
        <p class="text-stone-500 font-light mb-10">Добавьте краски, кисти или холсты, чтобы начать творить.</p>
        <router-link to="/catalog" class="px-8 py-3 bg-charcoal text-white hover:bg-clay transition-colors uppercase tracking-widest text-sm font-medium rounded-sm shadow-md">
          Перейти в каталог
        </router-link>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-20 items-start" :class="{ 'opacity-60 pointer-events-none transition-opacity': isUpdating }">
        
        <div class="lg:col-span-7 xl:col-span-8 flex flex-col gap-8">
          
          <div v-for="item in shopStore.cart.detailed_items" :key="item.product.id" class="flex flex-col sm:flex-row gap-6 pb-8 border-b border-sand">
            
            <router-link :to="`/product/${item.product.id}`" class="w-32 h-40 shrink-0 bg-stone-100 overflow-hidden rounded-sm relative group">
              <img v-if="item.product.image" :src="item.product.image" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
            </router-link>

            <div class="flex-grow flex flex-col justify-between">
              <div class="flex justify-between items-start gap-4">
                <div>
                  <p class="text-xs text-stone-500 uppercase tracking-wider mb-1">{{ item.product.category }}</p>
                  <router-link :to="`/product/${item.product.id}`" class="font-serif text-xl text-charcoal hover:text-clay transition-colors leading-tight block">
                    {{ item.product.name }}
                  </router-link>
                </div>
                <button @click="removeItem(item.product.id)" class="text-stone-400 hover:text-red-500 transition-colors" title="Удалить">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </div>

              <div class="flex justify-between items-end mt-6">
                <div class="flex items-center border border-sand rounded-sm">
                  <button @click="updateQty(item.product.id, item.qty, -1)" class="w-10 h-10 flex justify-center items-center text-stone-500 hover:text-charcoal hover:bg-stone-50 transition-colors" :disabled="item.qty <= 1">
                    <span class="text-lg leading-none">-</span>
                  </button>
                  <span class="w-10 text-center text-sm font-medium text-charcoal">{{ item.qty }}</span>
                  <button @click="updateQty(item.product.id, item.qty, 1)" class="w-10 h-10 flex justify-center items-center text-stone-500 hover:text-charcoal hover:bg-stone-50 transition-colors">
                    <span class="text-lg leading-none">+</span>
                  </button>
                </div>
                
                <div class="text-right">
                  <p v-if="item.qty > 1" class="text-xs text-stone-400 mb-1">{{ item.product.price }} ₽ / шт</p>
                  <p class="font-medium text-lg text-charcoal">{{ item.line_total }} ₽</p>
                </div>
              </div>
            </div>
          </div>
          
        </div>

        <div class="lg:col-span-5 xl:col-span-4 bg-stone-50 p-8 rounded-sm sticky top-28 border border-sand/50 shadow-sm">
          <h2 class="font-serif text-2xl text-charcoal mb-8">Сумма заказа</h2>
          
          <div class="mb-8">
            <h3 class="text-sm uppercase tracking-widest text-stone-500 mb-4">Способ доставки</h3>
            <div class="space-y-3">
              <label class="flex items-center justify-between p-4 border rounded-sm cursor-pointer transition-colors"
                     :class="shopStore.cart.delivery_method === 'courier' ? 'border-clay bg-white' : 'border-sand hover:border-clay/50 bg-transparent'"
                     @click="changeDelivery('courier')">
                <div class="flex items-center gap-3">
                  <div class="w-4 h-4 rounded-full border flex justify-center items-center" :class="shopStore.cart.delivery_method === 'courier' ? 'border-clay' : 'border-stone-300'">
                    <div v-if="shopStore.cart.delivery_method === 'courier'" class="w-2 h-2 bg-clay rounded-full"></div>
                  </div>
                  <span class="font-light text-charcoal">Курьером</span>
                </div>
                <span class="text-sm text-stone-500 font-medium">350 ₽</span>
              </label>

              <label class="flex items-center justify-between p-4 border rounded-sm cursor-pointer transition-colors"
                     :class="shopStore.cart.delivery_method === 'pickup' ? 'border-clay bg-white' : 'border-sand hover:border-clay/50 bg-transparent'"
                     @click="changeDelivery('pickup')">
                <div class="flex items-center gap-3">
                  <div class="w-4 h-4 rounded-full border flex justify-center items-center" :class="shopStore.cart.delivery_method === 'pickup' ? 'border-clay' : 'border-stone-300'">
                    <div v-if="shopStore.cart.delivery_method === 'pickup'" class="w-2 h-2 bg-clay rounded-full"></div>
                  </div>
                  <span class="font-light text-charcoal">Самовывоз</span>
                </div>
                <span class="text-sm text-stone-500 font-medium">Бесплатно</span>
              </label>
            </div>
          </div>

          <div class="mb-8 border-b border-sand pb-8">
            <h3 class="text-sm uppercase tracking-widest text-stone-500 mb-4">Промокод</h3>
            
            <div v-if="shopStore.cart.promo_code" class="flex justify-between items-center bg-clay/10 text-clay px-4 py-3 rounded-sm border border-clay/20">
              <span class="font-medium uppercase tracking-wider">{{ shopStore.cart.promo_code }}</span>
              <button @click="handleRemovePromo" class="text-sm underline hover:text-charcoal transition-colors">Отменить</button>
            </div>
            
            <form v-else @submit.prevent="handleApplyPromo" class="flex gap-2">
              <input 
                v-model="promoInput" 
                type="text" 
                placeholder="Введите код" 
                class="flex-grow bg-white border border-sand px-4 py-3 text-sm focus:outline-none focus:border-clay transition-colors rounded-sm uppercase placeholder:normal-case font-medium"
              >
              <button type="submit" class="px-6 py-3 bg-charcoal text-white hover:bg-clay transition-colors text-sm font-medium rounded-sm uppercase tracking-wider">
                Применить
              </button>
            </form>
          </div>

          <div class="space-y-4 mb-8 text-sm">
            <div class="flex justify-between">
              <span class="text-stone-500 font-light">Товары ({{ shopStore.cartCount }})</span>
              <span class="font-medium text-charcoal">{{ shopStore.cart.subtotal }} ₽</span>
            </div>
            
            <div v-if="shopStore.cart.discount > 0" class="flex justify-between text-clay">
              <span class="font-light">Скидка по промокоду</span>
              <span class="font-medium">- {{ shopStore.cart.discount }} ₽</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-stone-500 font-light">Доставка</span>
              <span class="font-medium text-charcoal">{{ shopStore.cart.delivery_cost > 0 ? `${shopStore.cart.delivery_cost} ₽` : 'Бесплатно' }}</span>
            </div>
          </div>

          <div class="flex justify-between items-end border-t border-sand pt-6 mb-8">
            <span class="text-lg font-serif italic text-charcoal">Итого</span>
            <span class="text-3xl font-medium text-charcoal">{{ shopStore.cart.total }} ₽</span>
          </div>

          <router-link to="/checkout" class="block w-full text-center py-4 bg-charcoal text-white hover:bg-clay transition-all duration-300 uppercase tracking-widest text-sm font-medium rounded-sm shadow-md hover:shadow-lg hover:-translate-y-0.5">
            Перейти к оформлению
          </router-link>
          
        </div>

      </div>
    </div>
  </div>
</template>