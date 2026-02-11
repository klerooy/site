<script setup>
import { RouterView } from 'vue-router'
import SiteFooter from './components/SiteFooter.vue'
import SiteHeader from './components/SiteHeader.vue'
</script>

<template>
  <div class="site-shell">
    <SiteHeader />
    <main class="page-main">
      <RouterView />
    </main>
    <SiteFooter />
  </div>
</template>
