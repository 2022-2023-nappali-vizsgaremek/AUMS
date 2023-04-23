<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="/login">AUMS</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <router-link class="nav-link" to="/login" :class="{ 'router-link-active': $route.path === '/login' }">Login</router-link>
                    <router-link class="nav-link" to="/register" :class="{ 'router-link-active': $route.path === '/register' }">Register</router-link>
                    <router-link class="nav-link" to="/cards" :class="{ 'router-link-active': $route.path === '/cards' }">Cards</router-link>
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