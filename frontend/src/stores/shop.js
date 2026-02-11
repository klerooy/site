import { defineStore } from 'pinia'
import { api } from '../api/client'

function defaultCart() {
  return {
    items: [],
    detailed_items: [],
    subtotal: 0,
    discount: 0,
    delivery_cost: 0,
    total: 0,
    delivery_method: 'courier',
    promo_code: null
  }
}

export const useShopStore = defineStore('shop', {
  state: () => ({
    home: null,
    categories: [],
    catalog: {
      items: [],
      filters: {},
      count: 0
    },
    currentProduct: null,
    specials: [],
    contacts: null,
    account: null,
    cart: defaultCart(),
    suggestions: [],
    busy: false,
    error: ''
  }),

  getters: {
    cartCount: (state) =>
      state.cart?.detailed_items?.reduce((acc, item) => acc + item.qty, 0) || 0
  },

  actions: {
    setError(error) {
      this.error = error?.message || 'Неизвестная ошибка'
    },

    clearError() {
      this.error = ''
    },

    async fetchHome() {
      this.clearError()
      try {
        this.home = await api.getHome()
      } catch (error) {
        this.setError(error)
      }
    },

    async fetchCategories() {
      this.clearError()
      try {
        this.categories = await api.getCategories()
      } catch (error) {
        this.setError(error)
      }
    },

    async fetchCatalog(params = {}) {
      this.clearError()
      this.busy = true
      try {
        this.catalog = await api.getProducts(params)
      } catch (error) {
        this.setError(error)
      } finally {
        this.busy = false
      }
    },

    async fetchProduct(id) {
      this.clearError()
      this.busy = true
      try {
        this.currentProduct = await api.getProductById(id)
      } catch (error) {
        this.setError(error)
      } finally {
        this.busy = false
      }
    },

    async fetchSpecials() {
      this.clearError()
      try {
        this.specials = await api.getSpecials()
      } catch (error) {
        this.setError(error)
      }
    },

    async fetchContacts() {
      this.clearError()
      try {
        this.contacts = await api.getContacts()
      } catch (error) {
        this.setError(error)
      }
    },

    async fetchAccount() {
      this.clearError()
      try {
        this.account = await api.getAccount()
      } catch (error) {
        this.setError(error)
      }
    },

    async fetchSuggestions(query) {
      if (!query || query.trim().length < 2) {
        this.suggestions = []
        return
      }

      try {
        this.suggestions = await api.getSuggestions(query)
      } catch {
        this.suggestions = []
      }
    },

    async fetchCart() {
      try {
        this.cart = await api.getCart()
      } catch (error) {
        this.setError(error)
      }
    },

    async addToCart(productId, qty = 1) {
      this.clearError()
      try {
        this.cart = await api.addToCart(productId, qty)
      } catch (error) {
        this.setError(error)
      }
    },

    async updateCartItem(productId, qty) {
      this.clearError()
      try {
        this.cart = await api.updateCartItem(productId, qty)
      } catch (error) {
        this.setError(error)
      }
    },

    async removeCartItem(productId) {
      this.clearError()
      try {
        this.cart = await api.removeCartItem(productId)
      } catch (error) {
        this.setError(error)
      }
    },

    async applyPromo(code) {
      this.clearError()
      try {
        this.cart = await api.applyPromo(code)
      } catch (error) {
        this.setError(error)
        throw error
      }
    },

    async clearPromo() {
      this.clearError()
      try {
        this.cart = await api.clearPromo()
      } catch (error) {
        this.setError(error)
      }
    },

    async setDeliveryMethod(method) {
      this.clearError()
      try {
        this.cart = await api.setDelivery(method)
      } catch (error) {
        this.setError(error)
      }
    },

    async checkout(payload) {
      this.clearError()
      try {
        const result = await api.checkout(payload)
        await this.fetchCart()
        return result
      } catch (error) {
        this.setError(error)
        throw error
      }
    },

    async sendContact(payload) {
      this.clearError()
      try {
        return await api.sendContact(payload)
      } catch (error) {
        this.setError(error)
        throw error
      }
    }
  }
})
