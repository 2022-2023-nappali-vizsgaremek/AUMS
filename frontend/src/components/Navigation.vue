<template>
<nav class="navbar navbar-expand-lg sticky-top">
      <div class="container-fluid">
        <a class="navbar-brand text-white" href="/login">AUMS</a>
        <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <div class="navbar-nav">
            <router-link class="nav-link text-white" to="/login" :class="{ 'router-link-active': currentRoute.value === '/login' } "><span data-bs-target="#navbarCollapse.show" data-bs-toggle="collapse">Home</span></router-link>
            <router-link class="nav-link text-white" to="/register" :class="{ 'router-link-active': currentRoute.value === '/register' }" v-if="isAuthenticated"><span data-bs-target="#navbarCollapse.show" data-bs-toggle="collapse">Register</span></router-link>
            <router-link class="nav-link text-white" to="/cards" :class="{ 'router-link-active': currentRoute.value === '/cards' }" v-if="isAuthenticated"><span data-bs-target="#navbarCollapse.show" data-bs-toggle="collapse">Cards</span></router-link>
            <router-link class="nav-link text-white" to="/schedule" :class="{ 'router-link-active': currentRoute.value === '/schedule' }" v-if="isAuthenticated"><span data-bs-target="#navbarCollapse.show" data-bs-toggle="collapse">Schedule</span></router-link>
          </div>
        </div>
      </div>
    </nav>
</template>

<script setup>
  import { computed } from 'vue'
  import { useRoute } from 'vue-router'
  
  const currentRoute = useRoute()
  
  const isAuthenticated = computed(() => {
    return localStorage.getItem('access_token') !== null
  })
  </script>

<style scoped>
    .navbar-nav .router-link-active {
    background-color: rgba(97, 155, 138, 0.5);
    border-radius: 0.7rem;
    color: #4158d0;
    font-weight: bold;
    }
    .navbar {
        background-color: #2a224a;
        color: #d9d4e1;
    }
</style>