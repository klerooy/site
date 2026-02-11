<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  slides: {
    type: Array,
    default: () => []
  }
})

const current = ref(0)
let timer

function next() {
  if (!props.slides.length) {
    return
  }
  current.value = (current.value + 1) % props.slides.length
}

function prev() {
  if (!props.slides.length) {
    return
  }
  current.value = (current.value - 1 + props.slides.length) % props.slides.length
}

function start() {
  stop()
  timer = setInterval(next, 5000)
}

function stop() {
  if (timer) {
    clearInterval(timer)
  }
}

onMounted(start)
onBeforeUnmount(stop)
</script>

<template>
  <section class="hero-slider card" @mouseenter="stop" @mouseleave="start">
    <article
      v-for="(slide, index) in slides"
      :key="slide.title"
      class="hero-slide"
      :class="{ active: current === index }"
    >
      <img :src="slide.image" :alt="slide.title" />
      <div class="hero-overlay" />
      <div class="hero-content">
        <span class="pill">Вдохновение</span>
        <h1 class="title">{{ slide.title }}</h1>
        <p>{{ slide.subtitle }}</p>
        <RouterLink class="btn btn-primary" :to="slide.cta_link">{{ slide.cta }}</RouterLink>
      </div>
    </article>

    <div class="hero-controls">
      <button type="button" @click="prev">←</button>
      <button type="button" @click="next">→</button>
    </div>
  </section>
</template>

<style scoped>
.hero-slider {
  position: relative;
  overflow: hidden;
  min-height: 560px;
}

.hero-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transform: scale(1.03);
  transition: opacity 0.85s ease, transform 0.85s ease;
}

.hero-slide.active {
  opacity: 1;
  transform: scale(1);
}

.hero-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(125deg, rgba(53, 44, 35, 0.58) 0%, rgba(53, 44, 35, 0.28) 45%, rgba(53, 44, 35, 0.08) 100%);
}

.hero-content {
  position: absolute;
  left: 60px;
  bottom: 64px;
  max-width: 520px;
  color: #fdf8f0;
  display: grid;
  gap: 14px;
}

.hero-content p {
  margin: 0;
  color: rgba(253, 248, 240, 0.84);
}

.hero-controls {
  position: absolute;
  right: 28px;
  bottom: 28px;
  display: flex;
  gap: 8px;
}

.hero-controls button {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 1px solid rgba(255, 245, 233, 0.5);
  color: #fff8ef;
  background: rgba(255, 255, 255, 0.12);
  cursor: pointer;
}

@media (max-width: 760px) {
  .hero-slider {
    min-height: 470px;
  }

  .hero-content {
    left: 22px;
    right: 22px;
    bottom: 22px;
  }
}
</style>
