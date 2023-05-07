<template>
    <nav class="navbar navbar-expand-lg fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand text-white ms-2" href="/login">AUMS</a>
            <div class="navicon me-2" @click="closeNavbar">
                <div class="burger burgerIcon navbar-toggler">
                    <input class="hidden" id="burgerIcon" type="checkbox"/><span></span>
                </div>
            </div>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <div class="navbar-nav text-lg-start text-center">
                    <router-link class="nav-link text-white" to="/login" :class="{ 'router-link-active': currentRoute.value === '/login' }" @click="closeNavbar">
                        <span>Home</span>
                    </router-link>
                    <router-link class="nav-link text-white" to="/register" :class="{ 'router-link-active': currentRoute.value === '/register' }" @click="closeNavbar" v-if="isAuthenticated && role_level >= 5">
                        <span>Register</span>
                    </router-link>
                    <router-link class="nav-link text-white" to="/cards" :class="{ 'router-link-active': currentRoute.value === '/cards' }" @click="closeNavbar" v-if="isAuthenticated && role_level >= 5">
                        <span>Cards</span>
                    </router-link>
                    <router-link class="nav-link text-white" to="/schedule" :class="{ 'router-link-active': currentRoute.value === '/schedule' }" @click="closeNavbar" v-if="isAuthenticated && role_level >= 2">
                        <span>Schedule</span>
                    </router-link>
                    <router-link class="nav-link text-white" to="/admin" :class="{ 'router-link-active': currentRoute.value === '/admin' }" @click="closeNavbar" v-if="isAuthenticated && role_level >= 5">
                        <span>User Management</span>
                    </router-link>
                    <router-link class="nav-link text-white" to="/log_dump" :class="{ 'router-link-active': currentRoute.value === '/log_dump' }" @click="closeNavbar" v-if="isAuthenticated && role_level >= 5">
                        <span>Log</span>
                    </router-link>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
    import { ref, computed} from "vue"
    import { useRoute } from "vue-router"
    import { Collapse } from "../../node_modules/bootstrap/dist/js/bootstrap.esm.min.js"

    const burgerInput = ref(null);
    const currentRoute = useRoute();

    const isAuthenticated = computed(() =>
    { return localStorage.getItem("access_token") !== null });

    const role_level = computed(() =>
    { return localStorage.getItem("role_level"); });

    const closeNavbar = () =>
    {
        if(window.innerWidth > 992) return;

        const collapseInstance = new Collapse(navbarCollapseElement);
        const burgerCheckbox = document.getElementById("burgerIcon");
        const navbarCollapseElement = document.getElementById("navbarCollapse");

        burgerInput.value = !burgerInput.value;

        if (burgerInput.value)
        {
            collapseInstance.show();
            burgerCheckbox.checked = true;
        }
        else
        {
            collapseInstance.hide();
            burgerCheckbox.checked = false;
        }
    };
</script>

<style scoped>
    .navbar-nav .router-link-active
    {
        font-weight: bold;
        border-radius: 0.5rem;
        background-color: rgba(158, 135, 200, 0.5);
    }

    .navbar
    {
        color: #d9d4e1;
        background-color: #2a224a;
    }
    .navbar-brand
    {
        font-weight: bold;
        font-size: 1.5rem;
    }

    .hidden
    {
        width: 0;
        height: 0;
        visibility: hidden;
        position: absolute;
    }

    .burger
    {
        width: 3rem;
        height: 3rem;
        margin: 0.5rem;
        display: block;
        position: relative;
        border-radius: 3px;
        box-shadow: 0 0 4.1666666667vw rgba(0, 0, 0, 0.25), 0 0 0.8333333333vw rgba(214, 51, 132, 0.1);
    }
    .burger span
    {
        user-select: none;
        -ms-user-select: none;
        -moz-user-select: none;
        -webkit-user-select: none;

        top: 50%;
        left: 50%;
        cursor: pointer;
        position: absolute;
        margin-top: -0.0625rem;
        text-indent: -999em;
        margin: 0.0625rem auto 0.525rem -0.75rem;
    }
    .burger span, .burger span:before, .burger span:after
    {
        opacity: 1;
        width: 1.5rem;
        display: block;
        height: 0.125rem;
        transition: 0.3s;
        background-color: #fff;
    }
    .burger span:before, .burger span:after
    {
        content: "";
        position: absolute;
    }
    .burger span:after { top: 0.525rem; }
    .burger span:before { top: -0.525rem; }

    .navicon { display: flex; }
    .burgerIcon input:checked + span:before, .burgerIcon input:checked + span:afte
    {
        top: 0px;
        margin-top: -0.5875rem;
    }
    .burgerIcon input:checked + span { background-color: transparent; }
    .burgerIcon input:checked + span:before { transform: translateY(0.525rem) rotate(45deg); }
    .burgerIcon input:checked + span:after { transform: translateY(0.525rem) rotate(-45deg); }
</style>