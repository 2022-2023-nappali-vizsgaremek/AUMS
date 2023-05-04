<template>
<nav class="navbar navbar-expand-lg sticky-top">
      <div class="container-fluid">
        <a class="navbar-brand text-white" href="/login">AUMS</a>
        <div class="navicon">
          <label class="burger burger1 navbar-toggler" for="burger1" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <input class="hidden" id="burger1" type="checkbox" v-model="burgerChecked"/><span></span>
          </label>
        </div>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <div class="navbar-nav">
            <router-link class="nav-link text-white" to="/login" :class="{ 'router-link-active': currentRoute.value === '/login' }" @click="closeNavbar">
              <span>Home</span>
            </router-link>
            <router-link class="nav-link text-white" to="/register" :class="{ 'router-link-active': currentRoute.value === '/register' }" @click="closeNavbar" v-if="isAuthenticated">
              <span>Register</span>
            </router-link>
            <router-link class="nav-link text-white" to="/cards" :class="{ 'router-link-active': currentRoute.value === '/cards' }" @click="closeNavbar" v-if="isAuthenticated">
              <span>Cards</span>
            </router-link>
            <router-link class="nav-link text-white" to="/schedule" :class="{ 'router-link-active': currentRoute.value === '/schedule' }" @click="closeNavbar" v-if="isAuthenticated">
              <span>Schedule</span>
            </router-link>
          </div>
        </div>
      </div>
    </nav>
</template>

<script setup>
  import { Collapse } from '../../node_modules/bootstrap/dist/js/bootstrap.esm.min.js'
  import { ref, computed} from 'vue'
  import { useRoute } from 'vue-router'
  
  const currentRoute = useRoute()
  const burgerChecked = ref(false)
  
  const isAuthenticated = computed(() => {
    return localStorage.getItem('access_token') !== null
  })

  const closeNavbar = () => {
    const navbarCollapseElement = document.getElementById('navbarCollapse');
    const collapseInstance = new Collapse(navbarCollapseElement);


    setTimeout(() => {
      if(burgerChecked.value) {
      burgerChecked.value = false;
      collapseInstance.hide();
    } else {
      burgerChecked.value = true;
      collapseInstance.show();
    }
    }, 20);
  };
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
  .navbar-brand {
      font-weight: bold;
      font-size: 1.5rem;
  }

  .hidden {
    visibility: hidden;
    position: absolute;
    width: 0;
    height: 0;
  }
  .burger {
    display: block;
    position: relative;
    width: 3rem;
    height: 3rem;
    border-radius: 3px;
    box-shadow: 0 0 4.1666666667vw rgba(214, 51, 132, 0.25), 0 0 0.8333333333vw rgba(214, 51, 132, 0.1);
    margin: 0.5rem;
  }
  .burger span {
    -webkit-user-select: none;
      -moz-user-select: none;
        -ms-user-select: none;
            user-select: none;
    position: absolute;
    margin: 0.0625rem auto 0.525rem -0.75rem;
    text-indent: -999em;
    top: 50%;
    left: 50%;
    margin-top: -0.0625rem;
    cursor: pointer;
  }
  .burger span, .burger span:before, .burger span:after {
    display: block;
    width: 1.5rem;
    height: 0.125rem;
    background-color: #fff;
    transition: 0.3s;
    opacity: 1;
  }
  .burger span:before, .burger span:after {
    position: absolute;
    content: "";
  }
  .burger span:before {
    top: -0.525rem;
  }
  .burger span:after {
    top: 0.525rem;
  }

  .navicon {
    display: flex;
  }

  .burger1 input:checked + span:before, .burger1 input:checked + span:after {
    top: 0px;
    margin-top: -0.5875rem;
  }
  .burger1 input:checked + span {
    background-color: transparent;
  }
  .burger1 input:checked + span:before {
    transform: translateY(0.525rem) rotate(45deg);
  }
  .burger1 input:checked + span:after {
    transform: translateY(0.525rem) rotate(-45deg);
  }
</style>