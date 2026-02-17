<script setup>
import { RouterView, RouterLink } from 'vue-router'
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
          <button class="hover:text-clay">
            <span class="sr-only">Поиск</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </button>
          <RouterLink to="/cart" class="hover:text-clay relative">
            <span class="sr-only">Корзина</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
            <span class="absolute -top-2 -right-2 bg-clay text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center">0</span>
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
            <a href="#" class="hover:text-clay transition-colors">Политика конфиденциальности</a>
            <a href="#" class="hover:text-clay transition-colors">Оферта</a>
          </div>
        </div>

      </div>
    </footer>

  </div>
</template>