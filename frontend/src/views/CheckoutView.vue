<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useShopStore } from '../stores/shop'

const shopStore = useShopStore()
const router = useRouter()

const isLoading = ref(true)
const isSubmitting = ref(false)
const orderSuccess = ref(false)
const orderNumber = ref('')
const errorMessage = ref('')

const form = ref({
  fullName: '',
  phone: '',
  address: '',
  paymentMethod: 'card' 
})

const deliveryMethod = computed({
  get: () => shopStore.cart.delivery_method || 'courier',
  set: async (val) => { await shopStore.setDeliveryMethod(val) }
})

onMounted(async () => {
  await shopStore.fetchCart()
  
  if (shopStore.cartCount === 0) {
    router.push('/catalog')
  } else {
    // Подставляем имя, если пользователь авторизован
    if (shopStore.user) {
      form.value.fullName = shopStore.user.name
    }
    isLoading.value = false
  }
})

const submitOrder = async () => {
  errorMessage.value = ''
  
  if (deliveryMethod.value === 'courier' && !form.value.address.trim()) {
    errorMessage.value = 'Пожалуйста, укажите адрес для курьерской доставки.'
    return
  }

  isSubmitting.value = true

  try {
    const payload = {
      full_name: form.value.fullName,
      phone: form.value.phone,
      delivery_method: deliveryMethod.value,
      payment_method: form.value.paymentMethod,
      address: deliveryMethod.value === 'courier' ? form.value.address : null
    }

    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      const err = await response.json()
      let errMsg = 'Произошла ошибка при оформлении заказа.'
      
      // Расшифровываем Pydantic ошибку (ту самую [object Object])
      if (err.detail) {
        if (Array.isArray(err.detail)) {
          errMsg = err.detail.map(e => {
            if (e.loc.includes('phone')) return 'Укажите корректный телефон (минимум 6 символов).'
            if (e.loc.includes('full_name')) return 'Слишком короткое имя.'
            return e.msg
          }).join(' ')
        } else if (typeof err.detail === 'string') {
          errMsg = err.detail
        }
      }
      throw new Error(errMsg)
    }

    const data = await response.json()
    orderNumber.value = data.order.id
    orderSuccess.value = true
    
    await shopStore.fetchCart()
    window.scrollTo({ top: 0, behavior: 'smooth' })

  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="bg-paper min-h-screen pb-24">
    <div class="container mx-auto px-6 py-12 md:py-20">
      
      <transition name="fade" mode="out-in">
        <div v-if="orderSuccess" class="py-20 flex flex-col items-center justify-center text-center">
          <div class="w-24 h-24 bg-stone-100 rounded-full flex items-center justify-center mb-8 text-clay">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 13l4 4L19 7"></path></svg>
          </div>
          <h1 class="text-5xl font-serif italic text-charcoal mb-4">Спасибо за заказ!</h1>
          <p class="text-stone-500 font-light text-lg mb-2">Ваш заказ <span class="font-medium text-charcoal">#{{ orderNumber }}</span> успешно оформлен.</p>
          <p class="text-stone-500 font-light mb-12">Мы уже собираем материалы и скоро свяжемся с вами.</p>
          <router-link to="/account" class="px-10 py-4 bg-charcoal text-white hover:bg-clay transition-colors uppercase tracking-widest text-sm font-medium rounded-sm shadow-md hover:-translate-y-0.5">
            Перейти в профиль
          </router-link>
        </div>

        <div v-else-if="!isLoading">
          <nav class="mb-10 text-xs uppercase tracking-widest text-stone-500">
            <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
            <span class="mx-3 text-sand">/</span>
            <router-link to="/cart" class="hover:text-clay transition-colors">Коллекция</router-link>
            <span class="mx-3 text-sand">/</span>
            <span class="text-charcoal">Оформление</span>
          </nav>

          <h1 class="text-4xl md:text-5xl font-serif italic text-charcoal mb-12 border-b border-sand pb-8">Оформление заказа</h1>

          <form @submit.prevent="submitOrder" class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-20 items-start">
            
            <div class="lg:col-span-7 xl:col-span-8 flex flex-col gap-12">
              <section>
                <h2 class="font-serif text-2xl text-charcoal mb-6">Контактные данные</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-xs uppercase tracking-widest text-stone-500 mb-2">Имя и Фамилия</label>
                    <input v-model="form.fullName" type="text" required placeholder="Анна Морозова" class="w-full bg-white border border-sand px-4 py-3 text-sm focus:outline-none focus:border-clay transition-colors rounded-sm text-charcoal placeholder:text-stone-300">
                  </div>
                  <div>
                    <label class="block text-xs uppercase tracking-widest text-stone-500 mb-2">Телефон</label>
                    <input v-model="form.phone" type="tel" required placeholder="+7 (999) 000-00-00" class="w-full bg-white border border-sand px-4 py-3 text-sm focus:outline-none focus:border-clay transition-colors rounded-sm text-charcoal placeholder:text-stone-300">
                  </div>
                </div>
              </section>

              <section>
                <h2 class="font-serif text-2xl text-charcoal mb-6">Способ доставки</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
                  <label class="flex flex-col p-4 border rounded-sm cursor-pointer transition-all" :class="deliveryMethod === 'courier' ? 'border-clay bg-white shadow-sm' : 'border-sand hover:border-clay/50 bg-transparent'">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-4 h-4 rounded-full border flex justify-center items-center" :class="deliveryMethod === 'courier' ? 'border-clay' : 'border-stone-300'"><div v-if="deliveryMethod === 'courier'" class="w-2 h-2 bg-clay rounded-full"></div></div>
                      <span class="font-medium text-charcoal">Курьером до двери</span>
                    </div>
                    <span class="text-sm text-stone-500 pl-7 font-light">Доставка 350 ₽</span>
                  </label>

                  <label class="flex flex-col p-4 border rounded-sm cursor-pointer transition-all" :class="deliveryMethod === 'pickup' ? 'border-clay bg-white shadow-sm' : 'border-sand hover:border-clay/50 bg-transparent'">
                    <div class="flex items-center gap-3 mb-2">
                      <div class="w-4 h-4 rounded-full border flex justify-center items-center" :class="deliveryMethod === 'pickup' ? 'border-clay' : 'border-stone-300'"><div v-if="deliveryMethod === 'pickup'" class="w-2 h-2 bg-clay rounded-full"></div></div>
                      <span class="font-medium text-charcoal">Самовывоз</span>
                    </div>
                    <span class="text-sm text-stone-500 pl-7 font-light">Бесплатно из студии</span>
                  </label>
                </div>

                <transition name="fade">
                  <div v-if="deliveryMethod === 'courier'">
                    <label class="block text-xs uppercase tracking-widest text-stone-500 mb-2">Адрес доставки</label>
                    <input v-model="form.address" type="text" placeholder="Город, улица, дом, квартира" class="w-full bg-white border border-sand px-4 py-3 text-sm focus:outline-none focus:border-clay transition-colors rounded-sm text-charcoal placeholder:text-stone-300">
                  </div>
                </transition>
              </section>

              <section>
                <h2 class="font-serif text-2xl text-charcoal mb-6">Способ оплаты</h2>
                <div class="flex flex-col gap-3">
                  <label class="flex items-center gap-3 p-4 border rounded-sm cursor-pointer transition-all" :class="form.paymentMethod === 'card' ? 'border-clay bg-white shadow-sm' : 'border-sand hover:border-clay/50 bg-transparent'">
                    <input type="radio" v-model="form.paymentMethod" value="card" class="hidden">
                    <div class="w-4 h-4 rounded-full border flex justify-center items-center" :class="form.paymentMethod === 'card' ? 'border-clay' : 'border-stone-300'"><div v-if="form.paymentMethod === 'card'" class="w-2 h-2 bg-clay rounded-full"></div></div>
                    <span class="text-charcoal">Картой на сайте</span>
                  </label>
                  <label class="flex items-center gap-3 p-4 border rounded-sm cursor-pointer transition-all" :class="form.paymentMethod === 'cash' ? 'border-clay bg-white shadow-sm' : 'border-sand hover:border-clay/50 bg-transparent'">
                    <input type="radio" v-model="form.paymentMethod" value="cash" class="hidden">
                    <div class="w-4 h-4 rounded-full border flex justify-center items-center" :class="form.paymentMethod === 'cash' ? 'border-clay' : 'border-stone-300'"><div v-if="form.paymentMethod === 'cash'" class="w-2 h-2 bg-clay rounded-full"></div></div>
                    <span class="text-charcoal">При получении</span>
                  </label>
                </div>
              </section>
            </div>

            <div class="lg:col-span-5 xl:col-span-4 bg-stone-50 p-8 rounded-sm sticky top-28 border border-sand/50 shadow-sm">
              <h2 class="font-serif text-2xl text-charcoal mb-6">Ваш заказ</h2>
              
              <div class="space-y-4 mb-8 border-b border-sand pb-8 max-h-64 overflow-y-auto pr-2 custom-scrollbar">
                <div v-for="item in shopStore.cart.detailed_items" :key="item.product.id" class="flex gap-4 items-center">
                  <img v-if="item.product.image" :src="item.product.image" class="w-12 h-16 object-cover rounded-sm border border-sand">
                  <div class="flex-grow">
                    <div class="text-sm font-medium text-charcoal leading-tight mb-1 truncate max-w-[180px]">{{ item.product.name }}</div>
                    <div class="text-xs text-stone-500 font-light">{{ item.qty }} шт.</div>
                  </div>
                  <div class="text-sm font-medium text-charcoal whitespace-nowrap">{{ item.line_total }} ₽</div>
                </div>
              </div>

              <div class="space-y-3 mb-8 text-sm">
                <div class="flex justify-between">
                  <span class="text-stone-500 font-light">Товары ({{ shopStore.cartCount }})</span>
                  <span class="font-medium text-charcoal">{{ shopStore.cart.subtotal }} ₽</span>
                </div>
                <div v-if="shopStore.cart.discount > 0" class="flex justify-between text-clay">
                  <span class="font-light">Скидка</span>
                  <span class="font-medium">- {{ shopStore.cart.discount }} ₽</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-stone-500 font-light">Доставка</span>
                  <span class="font-medium text-charcoal">{{ shopStore.cart.delivery_cost > 0 ? `${shopStore.cart.delivery_cost} ₽` : 'Бесплатно' }}</span>
                </div>
              </div>

              <div class="flex justify-between items-end border-t border-sand pt-6 mb-8">
                <span class="text-lg font-serif italic text-charcoal">К оплате</span>
                <span class="text-3xl font-medium text-charcoal">{{ shopStore.cart.total }} ₽</span>
              </div>

              <div v-if="errorMessage" class="mb-6 p-3 bg-red-50 text-red-600 text-sm rounded-sm border border-red-100">
                {{ errorMessage }}
              </div>

              <button type="submit" :disabled="isSubmitting" class="w-full py-4 bg-charcoal text-white hover:bg-clay transition-all duration-300 uppercase tracking-widest text-sm font-medium rounded-sm shadow-md flex justify-center items-center gap-2" :class="{ 'opacity-70 pointer-events-none': isSubmitting }">
                <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                <span>{{ isSubmitting ? 'Оформляем...' : 'Подтвердить заказ' }}</span>
              </button>
            </div>
          </form>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease, transform 0.4s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(10px); }
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: var(--color-sand); border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: var(--color-clay); }
</style>