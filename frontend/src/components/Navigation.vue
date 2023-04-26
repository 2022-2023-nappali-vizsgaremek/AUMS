<template>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="/login">AUMS</a>
            <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <div class="navbar-nav">
            <router-link class="nav-link" to="/login" :class="{ 'router-link-active': this.$route.path === '/login' } "><span data-bs-target="#navbarCollapse.show" data-bs-toggle="collapse">Login</span></router-link>
            <router-link class="nav-link" to="/register" :class="{ 'router-link-active': this.$route.path === '/register' }"><span data-bs-target="#navbarCollapse.show" data-bs-toggle="collapse">Register</span></router-link>
            <router-link class="nav-link" to="/cards" :class="{ 'router-link-active': this.$route.path === '/cards' }"><span data-bs-target="#navbarCollapse.show" data-bs-toggle="collapse">Cards</span></router-link>
            <router-link class="nav-link" to="/schedule" :class="{ 'router-link-active': this.$route.path === '/schedule' }"><span data-bs-target="#navbarCollapse.show" data-bs-toggle="collapse">Schedule</span></router-link>
            </div>
            </div>
        </div>
    </nav>
</template>

<style scoped>
    .navbar-nav .router-link-active {
    color: #4158d0;
    font-weight: bold;
    }
    .navbar {
        background-color: #e3f2fd;
    }
</style>