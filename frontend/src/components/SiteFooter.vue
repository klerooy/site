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
  <footer class="site-footer section-tight">
    <div class="container footer-card card">
      <div>
        <h3 class="footer-title">Artistic Shop</h3>
        <p class="footer-text">Материалы, которые превращают идею в произведение.</p>
      </div>

      <div>
        <h4 class="footer-sub">Подписка на новости</h4>
        <form class="footer-form" @submit.prevent="subscribe">
          <input
            v-model="email"
            class="input"
            type="email"
            placeholder="Ваш email"
            required
          />
          <button class="btn btn-primary" type="submit">Подписаться</button>
        </form>
        <p v-if="done" class="success">Спасибо! Вы подписаны.</p>
      </div>

      <div>
        <h4 class="footer-sub">Социальные сети</h4>
        <div class="socials">
          <a href="#" aria-label="Telegram">Telegram</a>
          <a href="#" aria-label="VK">VK</a>
          <a href="#" aria-label="Pinterest">Pinterest</a>
        </div>
      </div>
    </div>

    <div class="container footer-bottom">
      <small>© 2026 Artistic Shop</small>
      <a href="#">Политика конфиденциальности</a>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  padding-bottom: 36px;
}

.footer-card {
  padding: 34px;
  display: grid;
  grid-template-columns: 1.2fr 1.4fr 1fr;
  gap: 28px;
}

.footer-title {
  margin: 0;
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
}

.footer-text {
  color: var(--text-soft);
}

.footer-sub {
  margin: 0 0 10px;
  font-size: 1rem;
}

.footer-form {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
}

.socials {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.socials a {
  border: 1px solid var(--stroke);
  border-radius: 999px;
  padding: 7px 11px;
  color: var(--text-soft);
}

.footer-bottom {
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
  color: var(--text-soft);
}

@media (max-width: 920px) {
  .footer-card {
    grid-template-columns: 1fr;
    padding: 26px;
  }

  .footer-form {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
