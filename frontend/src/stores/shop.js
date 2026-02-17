import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useShopStore = defineStore('shop', () => {
  // ==========================================
  // 1. СОСТОЯНИЕ КОРЗИНЫ
  // ==========================================
  const cart = ref({
    items: [], detailed_items: [], subtotal: 0, discount: 0, delivery_cost: 0, total: 0, delivery_method: 'courier', promo_code: null
  })

  const cartCount = computed(() => cart.value.items?.reduce((sum, item) => sum + item.qty, 0) || 0)

  const fetchCart = async () => {
    try {
      const res = await fetch('/api/cart')
      if (res.ok) cart.value = await res.json()
    } catch (error) { console.error('Ошибка загрузки корзины:', error) }
  }

  const addToCart = async (productId, qty = 1) => {
    try {
      const res = await fetch('/api/cart/items', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ product_id: productId, qty })
      })
      if (res.ok) cart.value = await res.json()
    } catch (error) { console.error('Ошибка добавления в корзину:', error) }
  }

  const updateCartItem = async (productId, qty) => {
    try {
      const res = await fetch(`/api/cart/items/${productId}`, {
        method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ qty })
      })
      if (res.ok) cart.value = await res.json()
    } catch (error) { console.error('Ошибка обновления:', error) }
  }

  const removeCartItem = async (productId) => {
    try {
      const res = await fetch(`/api/cart/items/${productId}`, { method: 'DELETE' })
      if (res.ok) cart.value = await res.json()
    } catch (error) { console.error('Ошибка удаления:', error) }
  }

  const setDeliveryMethod = async (method) => {
    try {
      const res = await fetch('/api/cart/delivery', {
        method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ delivery_method: method })
      })
      if (res.ok) cart.value = await res.json()
    } catch (error) { console.error('Ошибка доставки:', error) }
  }

  const applyPromo = async (code) => {
    const res = await fetch('/api/cart/promo', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code })
    })
    if (res.ok) {
      cart.value = await res.json()
    } else {
      throw new Error('Неверный промокод')
    }
  }

  const clearPromo = async () => {
    try {
      const res = await fetch('/api/cart/promo', { method: 'DELETE' })
      if (res.ok) cart.value = await res.json()
    } catch (error) { console.error('Ошибка отмены промокода:', error) }
  }

  // ==========================================
  // 1.1 КОНТАКТЫ
  // ==========================================
  const contacts = ref(null)
  const error = ref('')

  const fetchContacts = async () => {
    error.value = ''
    try {
      const res = await fetch('/api/contacts')
      if (res.ok) {
        contacts.value = await res.json()
      } else {
        error.value = 'Не удалось загрузить контакты'
      }
    } catch (e) {
      error.value = 'Ошибка сети при загрузке контактов'
    }
  }

  const sendContact = async (payload) => {
    error.value = ''
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (!res.ok) {
      error.value = 'Не удалось отправить сообщение'
      throw new Error(error.value)
    }
    return await res.json()
  }

  // ==========================================
  // 2. СОСТОЯНИЕ АККАУНТА И АВТОРИЗАЦИЯ
  // ==========================================
  const account = ref(null)
  
  // Восстанавливаем пользователя из памяти при перезагрузке страницы
  const storedUser = localStorage.getItem('artshop_user')
  const user = ref(storedUser ? JSON.parse(storedUser) : null)

  const isAdmin = computed(() => user.value && user.value.email === 'admin@art.shop')

  const login = async (email, password) => {
    const db = JSON.parse(localStorage.getItem('artshop_users_db') || '{}')
    const foundUser = db[email]

    if (foundUser && foundUser.password === password) {
      user.value = { name: foundUser.name, email: email }
      localStorage.setItem('artshop_user', JSON.stringify(user.value))
      await fetchAccount()
    } else {
      throw new Error('Неверный адрес почты или пароль')
    }
  }

  const register = async (name, email, password) => {
    const db = JSON.parse(localStorage.getItem('artshop_users_db') || '{}')
    
    if (db[email]) {
      throw new Error('Пользователь с такой почтой уже существует')
    }

    db[email] = { name, password }
    localStorage.setItem('artshop_users_db', JSON.stringify(db))

    user.value = { name, email }
    localStorage.setItem('artshop_user', JSON.stringify(user.value))
    await fetchAccount()
  }

  const logout = () => {
    user.value = null
    account.value = null
    localStorage.removeItem('artshop_user')
  }

  const fetchAccount = async () => {
    if (!user.value) return
    try {
      const res = await fetch('/api/account')
      if (res.ok) {
        const data = await res.json()
        account.value = {
          ...data,
          profile: { ...data.profile, name: user.value.name, email: user.value.email }
        }
      }
    } catch (e) { console.error(e) }
  }

  return { 
    cart, cartCount, fetchCart, addToCart, updateCartItem, removeCartItem, setDeliveryMethod, applyPromo, clearPromo,
    contacts, error, fetchContacts, sendContact,
    account, user, isAdmin, login, register, logout, fetchAccount 
  }
})