<script setup lang="ts">
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import Home from './views/Home.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-bg-primary">
    <Navbar />
    <main class="flex-1">
      <Home />
    </main>
    <Footer />
  </div>
</template>
