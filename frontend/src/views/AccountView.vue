<script setup>
import { ref, onMounted } from 'vue'
import { useShopStore } from '../stores/shop'
import ProductCard from '../components/ProductCard.vue'

const shopStore = useShopStore()

const isLoading = ref(false)
const authMode = ref('login') 
const errorMessage = ref('')
const activeTab = ref('orders') 

const form = ref({
  name: '',
  email: '',
  password: ''
})

const handleAuth = async () => {
  errorMessage.value = ''
  isLoading.value = true
  
  try {
    if (authMode.value === 'login') {
      await shopStore.login(form.value.email, form.value.password)
    } else {
      await shopStore.register(form.value.name, form.value.email, form.value.password)
    }
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isLoading.value = false
  }
}

const handleLogout = () => {
  shopStore.logout()
  authMode.value = 'login'
}

onMounted(async () => {
  if (shopStore.user) {
    await shopStore.fetchAccount()
  }
})
</script>

<template>
  <div class="bg-paper min-h-screen pb-24 relative">
    <div class="container mx-auto px-6 py-12 md:py-20">

      <nav class="mb-10 text-xs uppercase tracking-widest text-stone-500">
        <router-link to="/" class="hover:text-clay transition-colors">Главная</router-link>
        <span class="mx-3 text-sand">/</span>
        <span class="text-charcoal">Кабинет</span>
      </nav>

      <transition name="fade" mode="out-in">
        <div v-if="!shopStore.user" class="flex justify-center items-center py-10">
          <div class="bg-white border border-sand p-10 md:p-12 rounded-sm shadow-sm w-full max-w-md relative overflow-hidden">
            
            <div v-if="isLoading" class="absolute inset-0 bg-white/80 backdrop-blur-sm z-10 flex items-center justify-center">
              <div class="w-8 h-8 border-2 border-clay border-t-transparent rounded-full animate-spin"></div>
            </div>

            <div class="text-center mb-8">
              <h1 class="text-3xl font-serif italic text-charcoal mb-2">
                {{ authMode === 'login' ? 'С возвращением' : 'Новый творец' }}
              </h1>
              <p class="text-stone-500 font-light text-sm">
                {{ authMode === 'login' ? 'Войдите, чтобы продолжить покупки' : 'Присоединяйтесь к нашей творческой студии' }}
              </p>
            </div>

            <form @submit.prevent="handleAuth" class="space-y-5">
            <div v-if="errorMessage" class="p-3 bg-red-50 text-red-600 text-xs rounded-sm border border-red-100 mb-4">
              {{ errorMessage }}
            </div>
              <transition name="slide-down">
                <div v-if="authMode === 'register'">
                  <label class="block text-xs uppercase tracking-widest text-stone-500 mb-2">Ваше имя</label>
                  <input v-model="form.name" type="text" required class="w-full bg-stone-50 border border-sand px-4 py-3 text-sm focus:outline-none focus:border-clay focus:bg-white transition-colors rounded-sm text-charcoal">
                </div>
              </transition>

              <div>
                <label class="block text-xs uppercase tracking-widest text-stone-500 mb-2">E-mail</label>
                <input v-model="form.email" type="email" required class="w-full bg-stone-50 border border-sand px-4 py-3 text-sm focus:outline-none focus:border-clay focus:bg-white transition-colors rounded-sm text-charcoal">
              </div>

              <div>
                <label class="block text-xs uppercase tracking-widest text-stone-500 mb-2">Пароль</label>
                <input v-model="form.password" type="password" required class="w-full bg-stone-50 border border-sand px-4 py-3 text-sm focus:outline-none focus:border-clay focus:bg-white transition-colors rounded-sm text-charcoal">
              </div>

              <button type="submit" class="w-full py-4 bg-charcoal text-white hover:bg-clay transition-all duration-300 uppercase tracking-widest text-sm font-medium rounded-sm shadow-md mt-4">
                {{ authMode === 'login' ? 'Войти' : 'Зарегистрироваться' }}
              </button>
            </form>

            <div class="mt-8 text-center text-sm font-light text-stone-500 border-t border-sand pt-6">
              <span v-if="authMode === 'login'">
                Нет аккаунта? 
                <button @click="authMode = 'register'" class="text-charcoal font-medium hover:text-clay transition-colors ml-1">Создать</button>
              </span>
              <span v-else>
                Уже есть аккаунт? 
                <button @click="authMode = 'login'" class="text-charcoal font-medium hover:text-clay transition-colors ml-1">Войти</button>
              </span>
            </div>

          </div>
        </div>

        <div v-else-if="shopStore.account">
          
          <div class="mb-12 border-b border-sand pb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
            <div>
              <h1 class="text-4xl md:text-5xl font-serif italic text-charcoal mb-3">Личный кабинет</h1>
              <p class="text-stone-500 font-light text-lg">Здравствуйте, {{ shopStore.account.profile.name }}!</p>
            </div>
            
            <div class="bg-clay/10 border border-clay/20 px-6 py-4 rounded-sm flex items-center gap-4">
              <div>
                <p class="text-xs uppercase tracking-widest text-clay font-medium mb-1">Ваши бонусы</p>
                <p class="text-2xl font-serif text-charcoal">{{ shopStore.account.profile.bonuses }} ₽</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-20 items-start">
            
            <aside class="lg:col-span-3 flex flex-col gap-2 sticky top-28">
              <button @click="activeTab = 'orders'" class="text-left px-5 py-3 rounded-sm transition-colors text-sm uppercase tracking-widest font-medium" :class="activeTab === 'orders' ? 'bg-charcoal text-white' : 'text-stone-500 hover:bg-stone-100 hover:text-charcoal'">История заказов</button>
              <button @click="activeTab = 'favorites'" class="text-left px-5 py-3 rounded-sm transition-colors text-sm uppercase tracking-widest font-medium" :class="activeTab === 'favorites' ? 'bg-charcoal text-white' : 'text-stone-500 hover:bg-stone-100 hover:text-charcoal'">Избранное</button>
                <router-link v-if="shopStore.isAdmin" to="/admin" class="inline-block px-8 py-3 bg-clay text-white uppercase tracking-widest text-xs font-medium rounded-sm hover:bg-charcoal transition-colors">
                  Перейти в панель управления
                </router-link>
              <button @click="handleLogout" class="text-left px-5 py-3 rounded-sm transition-colors text-sm uppercase tracking-widest font-medium text-red-400 hover:bg-red-50 hover:text-red-500 mt-6">Выйти</button>
            </aside>

            <main class="lg:col-span-9">
              <transition name="fade" mode="out-in">
                <div v-if="activeTab === 'orders'">
                  <h2 class="text-2xl font-serif text-charcoal mb-8">История заказов</h2>
                  <div v-if="shopStore.account.orders.length > 0" class="space-y-6">
                    <div v-for="order in shopStore.account.orders" :key="order.id" class="bg-white border border-sand p-6 rounded-sm hover:shadow-md transition-shadow">
                      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-sand/50 pb-4 mb-4">
                        <div>
                          <p class="font-medium text-charcoal">Заказ №{{ order.id }}</p>
                          <p class="text-xs text-stone-500 mt-1">от {{ order.date }}</p>
                        </div>
                        <div class="flex items-center gap-4">
                          <span class="text-sm font-medium text-charcoal">{{ order.total }} ₽</span>
                          <span class="px-3 py-1 bg-stone-100 text-stone-600 text-xs uppercase tracking-wider rounded-sm">{{ order.status }}</span>
                        </div>
                      </div>
                      <div class="text-sm text-stone-500 font-light flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
                        Позиций в заказе: {{ order.items.length }}
                      </div>
                    </div>
                  </div>
                  <div v-else class="text-center py-16 bg-stone-50 rounded-sm">
                    <p class="text-stone-500 font-light mb-4">У вас пока нет заказов.</p>
                    <router-link to="/catalog" class="text-charcoal underline hover:text-clay transition-colors">Перейти в каталог</router-link>
                  </div>
                </div>
                

                <div v-else-if="activeTab === 'favorites'">
                  <h2 class="text-2xl font-serif text-charcoal mb-8">Избранные материалы</h2>
                  <div v-if="shopStore.account.favorites.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                    <ProductCard v-for="product in shopStore.account.favorites" :key="product.id" :product="product" />
                  </div>
                  <div v-else class="text-center py-16 bg-stone-50 rounded-sm">
                    <p class="text-stone-500 font-light mb-4">Ваша коллекция избранного пуста.</p>
                    <router-link to="/catalog" class="text-charcoal underline hover:text-clay transition-colors">Перейти в каталог</router-link>
                  </div>
                </div>
              </transition>
            </main>
          </div>

        </div>
      </transition>

    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-down-enter-active, .slide-down-leave-active { transition: all 0.3s ease; overflow: hidden; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-10px); max-height: 0; }
.slide-down-enter-to, .slide-down-leave-from { max-height: 100px; }
</style>