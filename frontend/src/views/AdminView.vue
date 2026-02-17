<script setup>
import { ref, onMounted, computed, watch } from 'vue'

const activeTab = ref('dashboard')
const isLoading = ref(true)

const stats = ref({ revenue: 0, ordersCount: 0 })
const orders = ref([])
const products = ref([])
const blogPosts = ref([])

const productsQuery = ref('')
const blogQuery = ref('')

const isProductModalOpen = ref(false)
const productModalMode = ref('create') // create | edit
const isSavingProduct = ref(false)
const productSaveError = ref('')

const productDraft = ref({
  id: null,
  name: '',
  category: '',
  price: 0,
  image: '',
  description: '',
  in_stock: true
})

const isBlogModalOpen = ref(false)
const blogModalMode = ref('create') // create | edit
const isSavingBlogPost = ref(false)
const blogSaveError = ref('')

const blogDraft = ref({
  id: null,
  title: '',
  excerpt: '',
  category: '',
  date: '',
  readTime: '',
  image: '',
  featured: false,
  content: ''
})

const filteredProducts = computed(() => {
  const q = productsQuery.value.trim().toLowerCase()
  if (!q) return products.value
  return products.value.filter(p => {
    const name = String(p?.name || '').toLowerCase()
    const category = String(p?.category || '').toLowerCase()
    return name.includes(q) || category.includes(q) || String(p?.id || '').includes(q)
  })
})

const filteredBlogPosts = computed(() => {
  const q = blogQuery.value.trim().toLowerCase()
  if (!q) return blogPosts.value
  return blogPosts.value.filter(p => {
    const title = String(p?.title || '').toLowerCase()
    const category = String(p?.category || '').toLowerCase()
    return title.includes(q) || category.includes(q) || String(p?.id || '').includes(q)
  })
})

const availableStatuses = ['Принят', 'Оплачен', 'Собирается', 'В доставке', 'Доставлен', 'Отменен']

const fetchOrdersAndStats = async () => {
  try {
    const [statsRes, ordersRes] = await Promise.all([
      fetch('/api/admin/stats'),
      fetch('/api/admin/orders')
    ])
    if (statsRes.ok) stats.value = await statsRes.json()
    if (ordersRes.ok) orders.value = await ordersRes.json()
  } catch (error) {
    console.error('Ошибка загрузки заказов:', error)
  }
}

// Загрузка всех реальных данных с бэкенда
const fetchAdminData = async () => {
  isLoading.value = true
  try {
    const [statsRes, ordersRes, productsRes, blogRes] = await Promise.all([
      fetch('/api/admin/stats'),
      fetch('/api/admin/orders'),
      fetch('/api/products'),
      fetch('/api/blog')
    ])

    if (statsRes.ok) stats.value = await statsRes.json()
    if (ordersRes.ok) orders.value = await ordersRes.json()
    if (productsRes.ok) {
      const pData = await productsRes.json()
      products.value = pData.items ? pData.items : pData
    }

    if (blogRes.ok) {
      blogPosts.value = await blogRes.json()
    }
  } catch (error) {
    console.error('Ошибка загрузки админ-панели:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchAdminData()
})

watch(activeTab, (tab) => {
  if (tab === 'orders') {
    fetchOrdersAndStats()
  }
})

// Обновление статуса заказа
const updateOrderStatus = async (orderId, newStatus) => {
  try {
    await fetch(`/api/admin/orders/${orderId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    })
    // Перезагружаем статистику (если отменили заказ, выручка должна упасть)
    const statsRes = await fetch('/api/admin/stats')
    if (statsRes.ok) stats.value = await statsRes.json()
  } catch (error) {
    alert('Ошибка при обновлении статуса')
  }
}

// Удаление товара
const deleteProduct = async (productId) => {
  if (!confirm('Вы уверены, что хотите удалить этот материал навсегда?')) return

  try {
    const res = await fetch(`/api/admin/products/${productId}`, { method: 'DELETE' })
    if (res.ok) {
      products.value = products.value.filter(p => p.id !== productId)
    } else {
      alert('Ошибка при удалении товара')
    }
  } catch (error) {
    console.error(error)
  }
}

const openCreateProduct = () => {
  productSaveError.value = ''
  productModalMode.value = 'create'
  productDraft.value = {
    id: null,
    name: '',
    category: '',
    price: 0,
    image: '',
    description: '',
    in_stock: true
  }
  isProductModalOpen.value = true
}

const openEditProduct = (product) => {
  productSaveError.value = ''
  productModalMode.value = 'edit'
  productDraft.value = {
    id: product.id,
    name: product.name || '',
    category: product.category || '',
    price: Number(product.price || 0),
    image: product.image || '',
    description: product.description || '',
    in_stock: product.in_stock ?? true
  }
  isProductModalOpen.value = true
}

const closeProductModal = () => {
  if (isSavingProduct.value) return
  isProductModalOpen.value = false
}

const saveProduct = async () => {
  productSaveError.value = ''
  const payload = {
    name: String(productDraft.value.name || '').trim(),
    category: String(productDraft.value.category || '').trim(),
    price: Number(productDraft.value.price),
    image: String(productDraft.value.image || '').trim() || null,
    description: String(productDraft.value.description || '').trim() || null,
    in_stock: Boolean(productDraft.value.in_stock)
  }

  if (!payload.name) {
    productSaveError.value = 'Укажите название товара'
    return
  }
  if (!payload.category) {
    productSaveError.value = 'Укажите категорию'
    return
  }
  if (Number.isNaN(payload.price) || payload.price < 0) {
    productSaveError.value = 'Цена должна быть числом больше или равным 0'
    return
  }

  isSavingProduct.value = true
  try {
    const isEdit = productModalMode.value === 'edit'
    const url = isEdit ? `/api/admin/products/${productDraft.value.id}` : '/api/admin/products'
    const method = isEdit ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      let detail = ''
      try {
        const data = await res.json()
        detail = data?.detail ? String(data.detail) : ''
      } catch {
        detail = ''
      }
      productSaveError.value = detail || 'Не удалось сохранить товар'
      return
    }

    const saved = await res.json()
    if (isEdit) {
      const idx = products.value.findIndex(p => p.id === saved.id)
      if (idx !== -1) products.value[idx] = saved
    } else {
      products.value.unshift(saved)
    }

    isProductModalOpen.value = false
  } catch (error) {
    productSaveError.value = 'Ошибка сети при сохранении'
  } finally {
    isSavingProduct.value = false
  }
}

const openCreateBlogPost = () => {
  blogSaveError.value = ''
  blogModalMode.value = 'create'
  const today = new Date()
  const dd = String(today.getDate()).padStart(2, '0')
  const mm = String(today.getMonth() + 1).padStart(2, '0')
  const yyyy = String(today.getFullYear())
  blogDraft.value = {
    id: null,
    title: '',
    excerpt: '',
    category: '',
    date: `${dd}.${mm}.${yyyy}`,
    readTime: '5 мин',
    image: '',
    featured: false,
    content: ''
  }
  isBlogModalOpen.value = true
}

const openEditBlogPost = (post) => {
  blogSaveError.value = ''
  blogModalMode.value = 'edit'
  blogDraft.value = {
    id: post.id,
    title: post.title || '',
    excerpt: post.excerpt || '',
    category: post.category || '',
    date: post.date || '',
    readTime: post.readTime || '',
    image: post.image || '',
    featured: Boolean(post.featured),
    content: post.content || ''
  }
  isBlogModalOpen.value = true
}

const closeBlogModal = () => {
  if (isSavingBlogPost.value) return
  isBlogModalOpen.value = false
}

const saveBlogPost = async () => {
  blogSaveError.value = ''
  const payload = {
    title: String(blogDraft.value.title || '').trim(),
    excerpt: String(blogDraft.value.excerpt || '').trim(),
    category: String(blogDraft.value.category || '').trim(),
    date: String(blogDraft.value.date || '').trim(),
    readTime: String(blogDraft.value.readTime || '').trim(),
    image: String(blogDraft.value.image || '').trim() || null,
    featured: Boolean(blogDraft.value.featured),
    content: String(blogDraft.value.content || '').trim() || null
  }

  if (!payload.title) {
    blogSaveError.value = 'Укажите заголовок'
    return
  }
  if (!payload.excerpt) {
    blogSaveError.value = 'Укажите краткое описание'
    return
  }
  if (!payload.category) {
    blogSaveError.value = 'Укажите рубрику'
    return
  }
  if (!payload.date) {
    blogSaveError.value = 'Укажите дату'
    return
  }
  if (!payload.readTime) {
    blogSaveError.value = 'Укажите время чтения'
    return
  }

  isSavingBlogPost.value = true
  try {
    const isEdit = blogModalMode.value === 'edit'
    const url = isEdit ? `/api/admin/blog/${blogDraft.value.id}` : '/api/admin/blog'
    const method = isEdit ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      let detail = ''
      try {
        const data = await res.json()
        detail = data?.detail ? String(data.detail) : ''
      } catch {
        detail = ''
      }
      blogSaveError.value = detail || 'Не удалось сохранить пост'
      return
    }

    const saved = await res.json()
    if (isEdit) {
      const idx = blogPosts.value.findIndex(p => p.id === saved.id)
      if (idx !== -1) blogPosts.value[idx] = saved
    } else {
      blogPosts.value.unshift(saved)
    }

    if (saved.featured) {
      blogPosts.value = blogPosts.value.map(p => ({ ...p, featured: p.id === saved.id }))
    }

    isBlogModalOpen.value = false
  } catch (error) {
    blogSaveError.value = 'Ошибка сети при сохранении'
  } finally {
    isSavingBlogPost.value = false
  }
}

const deleteBlogPost = async (postId) => {
  if (!confirm('Удалить пост из журнала?')) return
  try {
    const res = await fetch(`/api/admin/blog/${postId}`, { method: 'DELETE' })
    if (res.ok) {
      blogPosts.value = blogPosts.value.filter(p => p.id !== postId)
    } else {
      alert('Ошибка при удалении поста')
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <div class="bg-paper min-h-screen pb-24">

    <div v-if="isLoading" class="h-screen flex items-center justify-center text-clay font-serif italic text-2xl">
      Синхронизация данных...
    </div>

    <div v-else class="container mx-auto px-6 py-10">
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-10 items-start">
        
        <aside class="xl:col-span-2 bg-white border border-sand rounded-sm p-4 sticky top-28 shadow-sm">
          <nav class="flex flex-col gap-2">
            <button @click="activeTab = 'dashboard'" class="flex items-center gap-3 px-4 py-3 rounded-sm transition-colors text-sm uppercase tracking-widest font-medium text-left" :class="activeTab === 'dashboard' ? 'bg-charcoal text-white' : 'text-stone-500 hover:bg-stone-50 hover:text-charcoal'">
              Дашборд
            </button>
            <button @click="activeTab = 'orders'" class="flex items-center gap-3 px-4 py-3 rounded-sm transition-colors text-sm uppercase tracking-widest font-medium text-left" :class="activeTab === 'orders' ? 'bg-charcoal text-white' : 'text-stone-500 hover:bg-stone-50 hover:text-charcoal'">
              Заказы
            </button>
            <button @click="activeTab = 'products'" class="flex items-center gap-3 px-4 py-3 rounded-sm transition-colors text-sm uppercase tracking-widest font-medium text-left" :class="activeTab === 'products' ? 'bg-charcoal text-white' : 'text-stone-500 hover:bg-stone-50 hover:text-charcoal'">
              Товары
            </button>
            <button @click="activeTab = 'blog'" class="flex items-center gap-3 px-4 py-3 rounded-sm transition-colors text-sm uppercase tracking-widest font-medium text-left" :class="activeTab === 'blog' ? 'bg-charcoal text-white' : 'text-stone-500 hover:bg-stone-50 hover:text-charcoal'">
              Журнал
            </button>
          </nav>
        </aside>

        <main class="xl:col-span-10">
          <transition name="fade" mode="out-in">
            
            <div v-if="activeTab === 'dashboard'">
              <h1 class="text-3xl font-serif text-charcoal mb-8">Обзор мастерской</h1>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                <div class="bg-white border border-sand p-8 rounded-sm shadow-sm">
                  <h3 class="text-xs uppercase tracking-widest text-stone-500 mb-2">Выручка (завершено)</h3>
                  <p class="text-4xl font-serif text-charcoal">{{ stats.revenue }} ₽</p>
                </div>
                <div class="bg-white border border-sand p-8 rounded-sm shadow-sm">
                  <h3 class="text-xs uppercase tracking-widest text-stone-500 mb-2">Всего заказов</h3>
                  <p class="text-4xl font-serif text-charcoal">{{ stats.ordersCount }}</p>
                </div>
              </div>
            </div>

            <div v-else-if="activeTab === 'orders'">
              <div class="flex justify-between items-center mb-8">
                <h1 class="text-3xl font-serif text-charcoal">Управление заказами</h1>
                <button @click="fetchOrdersAndStats" class="px-5 py-2 border border-sand text-charcoal hover:bg-stone-50 transition-colors uppercase tracking-widest text-xs font-medium rounded-sm">
                  Обновить
                </button>
              </div>
              
              <div class="bg-white border border-sand rounded-sm shadow-sm overflow-x-auto">
                <table class="w-full text-left min-w-[800px]">
                  <thead>
                    <tr class="bg-stone-50 border-b border-sand text-stone-500 text-xs uppercase tracking-widest">
                      <th class="py-4 px-6 font-medium">Заказ</th>
                      <th class="py-4 px-6 font-medium">Покупатель</th>
                      <th class="py-4 px-6 font-medium">Доставка</th>
                      <th class="py-4 px-6 font-medium">Сумма</th>
                      <th class="py-4 px-6 font-medium">Статус</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="order in orders" :key="order.id" class="border-b border-sand/30 hover:bg-stone-50 transition-colors">
                      <td class="py-4 px-6">
                        <div class="font-medium text-charcoal">{{ order.id }}</div>
                        <div class="text-xs text-stone-400 mt-1">{{ order.date }}</div>
                      </td>
                      <td class="py-4 px-6">
                        <div class="text-charcoal">{{ order.recipient || 'Без имени' }}</div>
                        <div class="text-xs text-stone-500">{{ order.phone }}</div>
                      </td>
                      <td class="py-4 px-6 text-sm text-stone-600">
                        {{ order.delivery_method === 'courier' ? 'Курьер' : 'Самовывоз' }}
                      </td>
                      <td class="py-4 px-6 text-charcoal font-medium">{{ order.total }} ₽</td>
                      <td class="py-4 px-6">
                        <select 
                          v-model="order.status" 
                          @change="updateOrderStatus(order.id, order.status)"
                          class="bg-transparent border border-stone-300 rounded-sm py-1.5 px-3 focus:outline-none focus:border-clay cursor-pointer text-sm font-medium"
                          :class="order.status === 'Отменен' ? 'text-red-600 border-red-200' : 'text-charcoal'"
                        >
                          <option v-for="st in availableStatuses" :key="st" :value="st">{{ st }}</option>
                        </select>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div v-else-if="activeTab === 'products'">
              <div class="flex justify-between items-center mb-8">
                <h1 class="text-3xl font-serif text-charcoal">Каталог материалов</h1>
                <button @click="openCreateProduct" class="px-6 py-2 bg-charcoal text-white hover:bg-clay transition-colors uppercase tracking-widest text-xs font-medium rounded-sm">
                  + Добавить товар
                </button>
              </div>

              <div class="bg-white border border-sand rounded-sm shadow-sm p-4 mb-6">
                <div class="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
                  <div class="flex-1">
                    <label class="text-xs uppercase tracking-widest text-stone-500">Поиск</label>
                    <input v-model="productsQuery" type="text" placeholder="Название, категория или ID" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
                  </div>
                  <div class="text-xs uppercase tracking-widest text-stone-500 whitespace-nowrap md:pt-6">
                    Показано: <span class="text-charcoal font-medium">{{ filteredProducts.length }}</span>
                  </div>
                </div>
              </div>
              
              <div class="bg-white border border-sand rounded-sm shadow-sm overflow-x-auto">
                <table class="w-full text-left min-w-[800px]">
                  <thead>
                    <tr class="bg-stone-50 border-b border-sand text-stone-500 text-xs uppercase tracking-widest">
                      <th class="py-4 px-6 font-medium w-16">Фото</th>
                      <th class="py-4 px-6 font-medium">Название</th>
                      <th class="py-4 px-6 font-medium">Категория</th>
                      <th class="py-4 px-6 font-medium">Цена</th>
                      <th class="py-4 px-6 font-medium text-right">Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="filteredProducts.length === 0">
                      <td colspan="5" class="py-10 px-6 text-center text-stone-500">
                        Ничего не найдено
                      </td>
                    </tr>
                    <tr v-for="product in filteredProducts" :key="product.id" class="border-b border-sand/30 hover:bg-stone-50 transition-colors">
                      <td class="py-3 px-6">
                        <div class="w-12 h-16 bg-stone-100 rounded-sm overflow-hidden border border-sand">
                          <img v-if="product.image" :src="product.image" class="w-full h-full object-cover">
                        </div>
                      </td>
                      <td class="py-4 px-6">
                        <div class="font-medium text-charcoal leading-tight">{{ product.name }}</div>
                        <div class="text-xs text-stone-400 mt-1">ID: {{ product.id }}</div>
                      </td>
                      <td class="py-4 px-6 text-sm text-stone-600">{{ product.category }}</td>
                      <td class="py-4 px-6 text-charcoal font-medium whitespace-nowrap">{{ product.price }} ₽</td>
                      <td class="py-4 px-6 text-right space-x-4">
                        <button @click="openEditProduct(product)" class="text-stone-400 hover:text-clay transition-colors text-sm">Изменить</button>
                        <button @click="deleteProduct(product.id)" class="text-stone-400 hover:text-red-500 transition-colors text-sm">Удалить</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div v-else-if="activeTab === 'blog'">
              <div class="flex justify-between items-center mb-8">
                <h1 class="text-3xl font-serif text-charcoal">Журнал</h1>
                <button @click="openCreateBlogPost" class="px-6 py-2 bg-charcoal text-white hover:bg-clay transition-colors uppercase tracking-widest text-xs font-medium rounded-sm">
                  + Добавить пост
                </button>
              </div>

              <div class="bg-white border border-sand rounded-sm shadow-sm p-4 mb-6">
                <div class="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
                  <div class="flex-1">
                    <label class="text-xs uppercase tracking-widest text-stone-500">Поиск</label>
                    <input v-model="blogQuery" type="text" placeholder="Заголовок, рубрика или ID" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
                  </div>
                  <div class="text-xs uppercase tracking-widest text-stone-500 whitespace-nowrap md:pt-6">
                    Показано: <span class="text-charcoal font-medium">{{ filteredBlogPosts.length }}</span>
                  </div>
                </div>
              </div>

              <div class="bg-white border border-sand rounded-sm shadow-sm overflow-x-auto">
                <table class="w-full text-left min-w-[900px]">
                  <thead>
                    <tr class="bg-stone-50 border-b border-sand text-stone-500 text-xs uppercase tracking-widest">
                      <th class="py-4 px-6 font-medium w-16">Обложка</th>
                      <th class="py-4 px-6 font-medium">Заголовок</th>
                      <th class="py-4 px-6 font-medium">Рубрика</th>
                      <th class="py-4 px-6 font-medium">Дата</th>
                      <th class="py-4 px-6 font-medium">Время</th>
                      <th class="py-4 px-6 font-medium">Флаг</th>
                      <th class="py-4 px-6 font-medium text-right">Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="filteredBlogPosts.length === 0">
                      <td colspan="7" class="py-10 px-6 text-center text-stone-500">
                        Ничего не найдено
                      </td>
                    </tr>
                    <tr v-for="post in filteredBlogPosts" :key="post.id" class="border-b border-sand/30 hover:bg-stone-50 transition-colors">
                      <td class="py-3 px-6">
                        <div class="w-12 h-16 bg-stone-100 rounded-sm overflow-hidden border border-sand">
                          <img v-if="post.image" :src="post.image" class="w-full h-full object-cover">
                        </div>
                      </td>
                      <td class="py-4 px-6">
                        <div class="font-medium text-charcoal leading-tight">{{ post.title }}</div>
                        <div class="text-xs text-stone-400 mt-1">ID: {{ post.id }}</div>
                      </td>
                      <td class="py-4 px-6 text-sm text-stone-600">{{ post.category }}</td>
                      <td class="py-4 px-6 text-sm text-stone-600 whitespace-nowrap">{{ post.date }}</td>
                      <td class="py-4 px-6 text-sm text-stone-600 whitespace-nowrap">{{ post.readTime }}</td>
                      <td class="py-4 px-6">
                        <span v-if="post.featured" class="text-xs uppercase tracking-widest text-clay border border-clay/40 px-2 py-1 rounded-sm">featured</span>
                        <span v-else class="text-xs uppercase tracking-widest text-stone-400">—</span>
                      </td>
                      <td class="py-4 px-6 text-right space-x-4">
                        <button @click="openEditBlogPost(post)" class="text-stone-400 hover:text-clay transition-colors text-sm">Изменить</button>
                        <button @click="deleteBlogPost(post.id)" class="text-stone-400 hover:text-red-500 transition-colors text-sm">Удалить</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

          </transition>
        </main>
      </div>
    </div>

    <div v-if="isProductModalOpen" class="fixed inset-0 z-50">
      <div class="absolute inset-0 bg-charcoal/60" @click="closeProductModal"></div>
      <div class="absolute inset-x-0 top-10 md:top-16 mx-auto w-[92%] max-w-2xl">
        <div class="bg-white border border-sand rounded-sm shadow-xl overflow-hidden">
          <div class="px-6 py-5 border-b border-sand flex items-start justify-between gap-6">
            <div>
              <div class="text-xs uppercase tracking-widest text-stone-500">Товары</div>
              <h2 class="text-2xl font-serif text-charcoal mt-1">
                {{ productModalMode === 'edit' ? 'Редактирование' : 'Новый товар' }}
              </h2>
            </div>
            <button class="text-stone-400 hover:text-charcoal transition-colors" @click="closeProductModal" :disabled="isSavingProduct">
              Закрыть
            </button>
          </div>

          <div class="p-6">
            <div v-if="productSaveError" class="mb-4 border border-red-200 bg-red-50 text-red-700 px-4 py-3 rounded-sm text-sm">
              {{ productSaveError }}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div class="md:col-span-2">
                <label class="text-xs uppercase tracking-widest text-stone-500">Название</label>
                <input v-model="productDraft.name" type="text" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Категория</label>
                <input v-model="productDraft.category" type="text" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Цена</label>
                <input v-model.number="productDraft.price" type="number" min="0" step="0.01" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div class="md:col-span-2">
                <label class="text-xs uppercase tracking-widest text-stone-500">URL изображения</label>
                <input v-model="productDraft.image" type="url" placeholder="https://..." class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div class="md:col-span-2">
                <label class="text-xs uppercase tracking-widest text-stone-500">Описание</label>
                <textarea v-model="productDraft.description" rows="4" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm"></textarea>
              </div>
              <div class="md:col-span-2 flex items-center justify-between gap-4 pt-2">
                <label class="flex items-center gap-3 text-sm text-charcoal">
                  <input v-model="productDraft.in_stock" type="checkbox" class="w-4 h-4" />
                  В наличии
                </label>

                <div class="flex items-center gap-3">
                  <button class="px-5 py-2 border border-sand text-charcoal hover:bg-stone-50 transition-colors uppercase tracking-widest text-xs font-medium rounded-sm" @click="closeProductModal" :disabled="isSavingProduct">
                    Отмена
                  </button>
                  <button class="px-6 py-2 bg-charcoal text-white hover:bg-clay transition-colors uppercase tracking-widest text-xs font-medium rounded-sm disabled:opacity-60 disabled:cursor-not-allowed" @click="saveProduct" :disabled="isSavingProduct">
                    {{ isSavingProduct ? 'Сохранение...' : 'Сохранить' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isBlogModalOpen" class="fixed inset-0 z-50">
      <div class="absolute inset-0 bg-charcoal/60" @click="closeBlogModal"></div>
      <div class="absolute inset-x-0 top-10 md:top-16 mx-auto w-[92%] max-w-3xl">
        <div class="bg-white border border-sand rounded-sm shadow-xl overflow-hidden max-h-[calc(100vh-5rem)] flex flex-col">
          <div class="px-6 py-5 border-b border-sand flex items-start justify-between gap-6">
            <div>
              <div class="text-xs uppercase tracking-widest text-stone-500">Журнал</div>
              <h2 class="text-2xl font-serif text-charcoal mt-1">
                {{ blogModalMode === 'edit' ? 'Редактирование поста' : 'Новый пост' }}
              </h2>
            </div>
            <button class="text-stone-400 hover:text-charcoal transition-colors" @click="closeBlogModal" :disabled="isSavingBlogPost">
              Закрыть
            </button>
          </div>

          <div class="p-6 overflow-y-auto">
            <div v-if="blogSaveError" class="mb-4 border border-red-200 bg-red-50 text-red-700 px-4 py-3 rounded-sm text-sm">
              {{ blogSaveError }}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div class="md:col-span-2">
                <label class="text-xs uppercase tracking-widest text-stone-500">Заголовок</label>
                <input v-model="blogDraft.title" type="text" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>

              <div class="md:col-span-2">
                <label class="text-xs uppercase tracking-widest text-stone-500">Краткое описание</label>
                <textarea v-model="blogDraft.excerpt" rows="3" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm"></textarea>
              </div>

              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Рубрика</label>
                <input v-model="blogDraft.category" type="text" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Дата</label>
                <input v-model="blogDraft.date" type="text" placeholder="15 Фев 2026 или 15.02.2026" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Время чтения</label>
                <input v-model="blogDraft.readTime" type="text" placeholder="8 мин" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>
              <div>
                <label class="text-xs uppercase tracking-widest text-stone-500">Featured</label>
                <div class="mt-3">
                  <label class="flex items-center gap-3 text-sm text-charcoal">
                    <input v-model="blogDraft.featured" type="checkbox" class="w-4 h-4" />
                    Показывать как главный пост
                  </label>
                </div>
              </div>

              <div class="md:col-span-2">
                <label class="text-xs uppercase tracking-widest text-stone-500">URL обложки</label>
                <input v-model="blogDraft.image" type="url" placeholder="https://..." class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm" />
              </div>

              <div class="md:col-span-2">
                <label class="text-xs uppercase tracking-widest text-stone-500">Контент (опционально)</label>
                <textarea v-model="blogDraft.content" rows="8" class="mt-2 w-full bg-transparent border border-sand rounded-sm py-2.5 px-3 focus:outline-none focus:border-clay text-sm"></textarea>
              </div>
            </div>
          </div>

          <div class="px-6 py-4 border-t border-sand bg-white sticky bottom-0 flex items-center justify-end gap-3">
            <button class="px-5 py-2 border border-sand text-charcoal hover:bg-stone-50 transition-colors uppercase tracking-widest text-xs font-medium rounded-sm" @click="closeBlogModal" :disabled="isSavingBlogPost">
              Отмена
            </button>
            <button class="px-6 py-2 bg-charcoal text-white hover:bg-clay transition-colors uppercase tracking-widest text-xs font-medium rounded-sm disabled:opacity-60 disabled:cursor-not-allowed" @click="saveBlogPost" :disabled="isSavingBlogPost">
              {{ isSavingBlogPost ? 'Сохранение...' : 'Сохранить' }}
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>