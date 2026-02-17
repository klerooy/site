import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useShopStore = defineStore('shop', () => {
  const cartState = ref({
    items: [],
    total_price: 0
  })

  const totalItems = computed(() => {
    return cartState.value.items?.reduce((sum, item) => sum + item.qty, 0) || 0
  })

  const fetchCart = async () => {
    try {
      const res = await fetch('/api/cart')
      if (res.ok) {
        cartState.value = await res.json()
      }
    } catch (error) {
      console.error('Ошибка загрузки корзины:', error)
    }
  }

  const addToCart = async (productId, qty = 1) => {
    try {
      const res = await fetch('/api/cart/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, qty })
      })
      if (res.ok) {
        cartState.value = await res.json()
      }
    } catch (error) {
      console.error('Ошибка добавления в корзину:', error)
    }
  }

  return { cartState, totalItems, fetchCart, addToCart }
})