import { createRouter, createWebHistory } from 'vue-router'

const HomeView = () => import('../views/HomeView.vue')
const CatalogView = () => import('../views/CatalogView.vue')
const ProductView = () => import('../views/ProductView.vue')
const SpecialsView = () => import('../views/SpecialsView.vue')
const ContactsView = () => import('../views/ContactsView.vue')
const AccountView = () => import('../views/AccountView.vue')
const CartView = () => import('../views/CartView.vue')
const CheckoutView = () => import('../views/CheckoutView.vue')
const BlogView = () => import('../views/BlogView.vue')

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/catalog', name: 'catalog', component: CatalogView },
  { path: '/product/:id', name: 'product', component: ProductView, props: true },
  { path: '/specials', name: 'specials', component: SpecialsView },
  { path: '/contacts', name: 'contacts', component: ContactsView },
  { path: '/account', name: 'account', component: AccountView },
  { path: '/cart', name: 'cart', component: CartView },
  { path: '/checkout', name: 'checkout', component: CheckoutView },
  { path: '/blog', name: 'blog', component: BlogView }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

export default router
