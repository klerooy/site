import { createRouter, createWebHistory } from 'vue-router'
import { useShopStore } from '../stores/shop'

import HomeView from '../views/HomeView.vue'
import CatalogView from '../views/CatalogView.vue'
import ProductView from '../views/ProductView.vue'
import CartView from '../views/CartView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import AccountView from '../views/AccountView.vue'
import BlogView from '../views/BlogView.vue'
import AdminView from '../views/AdminView.vue'
import ContactsView from '../views/ContactsView.vue'
import PrivacyPolicyView from '../views/PrivacyPolicyView.vue'
import OfferView from '../views/OfferView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/catalog', component: CatalogView },
    { path: '/product/:id', name: 'product', component: ProductView, props: true },
    { path: '/cart', component: CartView },
    { path: '/checkout', component: CheckoutView },
    { path: '/account', component: AccountView },
    { path: '/blog', component: BlogView },
    { path: '/contacts', component: ContactsView },
    { path: '/privacy', component: PrivacyPolicyView },
    { path: '/offer', component: OfferView },
    { 
      path: '/admin', 
      name: 'admin',
      component: AdminView,
      beforeEnter: (to, from, next) => {
        const store = useShopStore()
        if (store.isAdmin) {
          next()
        } else {
          next('/account')
        }
      }
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router