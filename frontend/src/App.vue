<script setup>
  import Navigation from './components/Navigation.vue';
</script>

<template>
  <div class="app-content container-gradient-scrollable">
    <Navigation />
    <router-view/>
  </div>
</template>