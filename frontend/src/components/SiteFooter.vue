<script setup>
import { ref } from 'vue'

const email = ref('')
const done = ref(false)

function subscribe() {
  if (!email.value.trim()) {
    return
  }
  done.value = true
  email.value = ''
}
</script>

<template>
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
            <RouterLink to="/privacy" class="hover:text-clay transition-colors">Политика конфиденциальности</RouterLink>
            <RouterLink to="/offer" class="hover:text-clay transition-colors">Оферта</RouterLink>
          </div>
        </div>

      </div>
    </footer>
</template>
