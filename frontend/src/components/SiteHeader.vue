<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import { useShopStore } from '../stores/shop'
import SearchSuggest from './SearchSuggest.vue'

const route = useRoute()
const store = useShopStore()
const menuOpen = ref(false)

const hasCartItems = computed(() => store.cartCount > 0)

const navItems = [
  { to: '/catalog', label: 'Каталог' },
  { to: '/specials', label: 'Наборы' },
  { to: '/blog', label: 'Блог' },
  { to: '/contacts', label: 'Контакты' }
]

onMounted(async () => {
  await store.fetchCart()
})
</script>

<template>
  <header class="site-header">
    <div class="container header-inner">
      <RouterLink to="/" class="logo-wrap">
        <span class="logo-mark">A</span>
        <span class="logo-text">Artistic Shop</span>
      </RouterLink>

      <button class="menu-btn" type="button" @click="menuOpen = !menuOpen">
        Меню
      </button>

      <nav class="header-nav" :class="{ open: menuOpen }">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="header-link"
          :class="{ active: route.path.startsWith(item.to) }"
          @click="menuOpen = false"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <div class="header-tools">
        <SearchSuggest class="header-search" />

        <RouterLink to="/account" class="icon-btn" aria-label="Личный кабинет">👤</RouterLink>

        <RouterLink to="/cart" class="icon-btn cart-link" aria-label="Корзина">
          🛒
          <span v-if="hasCartItems" class="cart-dot" />
        </RouterLink>
      </div>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid var(--stroke);
  background: rgba(250, 244, 235, 0.9);
  backdrop-filter: blur(7px);
}

.header-inner {
  min-height: 74px;
  display: grid;
  gap: 18px;
  grid-template-columns: auto auto 1fr auto;
  align-items: center;
}

.logo-wrap {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: 'Cormorant Garamond', serif;
  letter-spacing: 0.03em;
}

.logo-mark {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: linear-gradient(145deg, var(--accent-blue), var(--accent-lavender));
  color: #fff;
  font-weight: 700;
}

.logo-text {
  font-size: 1.5rem;
}

.menu-btn {
  display: none;
  border: 1px solid var(--stroke);
  background: rgba(255, 255, 255, 0.64);
  border-radius: 999px;
  padding: 7px 12px;
  font: inherit;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-link {
  color: var(--text-soft);
  font-size: 0.92rem;
  letter-spacing: 0.02em;
  transition: color 0.25s ease;
}

.header-link:hover,
.header-link.active {
  color: var(--text);
}

.header-tools {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-search {
  width: 330px;
}

.icon-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  border: 1px solid var(--stroke);
  background: rgba(255, 255, 255, 0.72);
  transition: transform 0.25s ease;
}

.icon-btn:hover {
  transform: translateY(-2px);
}

.cart-link {
  position: relative;
}

.cart-dot {
  position: absolute;
  top: 7px;
  right: 7px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--accent-rose);
}

@media (max-width: 1120px) {
  .header-inner {
    grid-template-columns: auto auto 1fr;
  }

  .header-search {
    width: 260px;
  }
}

@media (max-width: 960px) {
  .menu-btn {
    display: inline-flex;
    justify-self: start;
  }

  .header-nav {
    position: absolute;
    top: 74px;
    left: 0;
    right: 0;
    padding: 14px 20px;
    border-bottom: 1px solid var(--stroke);
    background: rgba(250, 244, 235, 0.97);
    display: none;
    flex-wrap: wrap;
  }

  .header-nav.open {
    display: flex;
  }

  .header-tools {
    grid-column: 1 / -1;
    width: 100%;
  }

  .header-search {
    flex: 1;
    width: 100%;
  }
}
</style>
