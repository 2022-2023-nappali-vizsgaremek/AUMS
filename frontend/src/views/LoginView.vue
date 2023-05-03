<template>
  <div class="limiter">
    <div class="container-login100">
      <div class="wrap-login100">
        <div class="login100-pic" data-tilt v-if="!isAuthenticated">
          <img src="../images/img-01.png" alt="IMG">
        </div>

        <form class="login100-form" @submit.prevent="onSubmit" v-if="!isAuthenticated">
          <span class="login100-form-title text-white">
            Member Login
          </span>

          <div class="wrap-input100" data-validate="Valid email is required: ex@abc.xyz">
            <input class="input100" type="text" name="email" placeholder="Email">
            <span class="focus-input100"></span>
            <span class="symbol-input100">
              <i class="fa fa-envelope" aria-hidden="true"></i>
            </span>
          </div>

          <div class="wrap-input100" data-validate="Password is required">
            <input class="input100" type="password" name="pass" placeholder="Password">
            <span class="focus-input100"></span>
            <span class="symbol-input100">
              <i class="fa fa-lock" aria-hidden="true"></i>
            </span>
          </div>
          <div class="container-login100-form-btn">
            <button class="login100-form-btn" @click="login">
              Login
            </button>
          </div>
        </form>

        <div v-else >
        <div class="container-login100-form-btn">
            <button class="login100-form-btn" @click="logout">
              LOGOUT
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
const isAuthenticated = ref(false);
const login = async () => {
  const email = document.querySelector('input[name="email"]').value;
  const password = document.querySelector('input[name="pass"]').value;
  const data = {
    company_email: email,
    password: password
  };
  const response = await axios.post('http://127.0.0.1:5000/login', data)
  .catch((error) => {
    alert(error.response.data.message);
  })
  .then(response => {
    if (response) {
      isAuthenticated.value = true;
      alert(response.data.message);
      localStorage.setItem('access_token', response.data["access_token"]);
	  location.reload();
    }
  });
};
const logout = () => {
  localStorage.removeItem('access_token');
  isAuthenticated.value = false;
  location.reload();
};
if (localStorage.getItem('access_token')) {
  isAuthenticated.value = true;
}
</script>