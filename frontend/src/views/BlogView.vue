<template>
  <section class="section">
    <div class="container">
      <article class="card blog-hero">
        <h1 class="title">Блог мастерской</h1>
        <p class="subtitle">
          Здесь будут гайды по материалам, подборки палитр и советы для начинающих художников.
        </p>
      </article>

      <div class="blog-grid">
        <article class="card blog-card" v-for="post in posts" :key="post.title">
          <img :src="post.image" :alt="post.title" />
          <div>
            <h2>{{ post.title }}</h2>
            <p>{{ post.text }}</p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
const posts = [
  {
    title: 'Как выбрать первую акварель',
    text: 'Разбираем пигменты, бумагу и базовый набор кистей для уверенного старта.',
    image: 'https://images.unsplash.com/photo-1452860606245-08befc0ff44b?auto=format&fit=crop&w=1200&q=80'
  },
  {
    title: 'Твердость карандаша: H, HB, B',
    text: 'Понятная схема, какие карандаши использовать для построения и штриховки.',
    image: 'https://images.unsplash.com/photo-1449247613801-ab06418e2861?auto=format&fit=crop&w=1200&q=80'
  },
  {
    title: 'Подарки художнику без ошибок',
    text: '5 универсальных идей от сертификата до готового творческого бокса.',
    image: 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1200&q=80'
  }
]
</script>

<style scoped>
.blog-hero {
  padding: 26px;
}

.blog-grid {
  margin-top: 24px;
  display: grid;
  gap: 18px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.blog-card {
  overflow: hidden;
}

.blog-card img {
  width: 100%;
  height: 210px;
  object-fit: cover;
}

.blog-card div {
  padding: 16px;
}

.blog-card h2 {
  margin: 0;
  font-size: 1.2rem;
}

.blog-card p {
  color: var(--text-soft);
}

@media (max-width: 980px) {
  .blog-grid {
    grid-template-columns: 1fr;
  }
}
</style>
