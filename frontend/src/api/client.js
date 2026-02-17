const API_BASE = '/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  })

  const isJson = response.headers.get('content-type')?.includes('application/json')
  const payload = isJson ? await response.json() : null

  if (!response.ok) {
    const detail = payload?.detail || payload?.message || 'Ошибка запроса'
    throw new Error(detail)
  }

  return payload
}

export async function getProductById(id) {
  try {
    const response = await fetch(`${API_BASE}/products/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Не удалось загрузить товар с ID ${id}:`, error);
    return null;
  }
}

export async function getPopularProducts() {
  try {
    const response = await fetch(`${API_BASE}/products/popular`);
    if (!response.ok) {
      throw new Error('Ошибка сети');
    }
    return await response.json();
  } catch (error) {
    console.error('Не удалось загрузить популярные товары:', error);
    return [];
  }
}

export const api = {
  getHome: () => request('/home'),
  getCategories: () => request('/categories'),
  getProducts: (params) => {
    const qs = new URLSearchParams()

    Object.entries(params || {}).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        qs.set(key, value)
      }
    })

    return request(`/products?${qs.toString()}`)
  },
  getProductById: (id) => request(`/products/${id}`),
  getSpecials: () => request('/specials'),
  getContacts: () => request('/contacts'),
  getAccount: () => request('/account'),
  getSuggestions: (query) => request(`/search/suggest?q=${encodeURIComponent(query)}`),
  getCart: () => request('/cart'),
  addToCart: (product_id, qty = 1) => request('/cart/items', {
    method: 'POST',
    body: JSON.stringify({ product_id, qty })
  }),
  updateCartItem: (product_id, qty) => request(`/cart/items/${product_id}`, {
    method: 'PATCH',
    body: JSON.stringify({ qty })
  }),
  removeCartItem: (product_id) => request(`/cart/items/${product_id}`, {
    method: 'DELETE'
  }),
  setDelivery: (delivery_method) => request('/cart/delivery', {
    method: 'PATCH',
    body: JSON.stringify({ delivery_method })
  }),
  applyPromo: (code) => request('/cart/promo', {
    method: 'POST',
    body: JSON.stringify({ code })
  }),
  clearPromo: () => request('/cart/promo', {
    method: 'DELETE'
  }),
  checkout: (payload) => request('/checkout', {
    method: 'POST',
    body: JSON.stringify(payload)
  }),
  sendContact: (payload) => request('/contact', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}
