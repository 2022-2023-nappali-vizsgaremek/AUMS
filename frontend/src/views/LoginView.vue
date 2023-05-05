<template>
  <div class="limiter d-flex align-items-center justify-content-center" style="min-height: calc(100vh - 66.8px);">
    <div class="container-login100">
      <div class="wrap-login100 justify-content-center">
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
          <div v-else class="text-center">
            <h2>Personal Data</h2>
            <hr class="my-4">
            <h4>Name</h4>
            <p style="font-size: larger;">{{ currentUser.name }}</p>
            <h4>Username</h4>
            <p style="font-size: larger;">{{ currentUser.username }}</p>
            <h4>Birth</h4>
            <p style="font-size: larger;">{{ currentUser.birth_date }}</p>
            <h4>Personal Email</h4>
            <p style="font-size: larger;">{{ currentUser.personal_email }}</p>
            <h4>Company Email</h4>
            <p style="font-size: larger;">{{ currentUser.company_email }}</p>
            <h4>Phone Number</h4>
            <p style="font-size: larger;">{{ currentUser.phone_number }}</p>
            <h4>Address</h4>
            <p style="font-size: larger;">{{ currentUser.address }}</p>
            <button class="login100-form-btn mt-5" @click="openModal">
              Change Personal Data
            </button>
            <button class="login100-form-btn-danger mt-4" @click="logout">
              LOGOUT
            </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Change Personal Data Modal -->
  <transition name="fade">
  <div v-show="showModal" class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <h5 class="modal-title text-center">Change Password</h5>
        <hr>
        <form @submit.prevent="saveChangedData">
          <div class="modal-body">
            <div class="form-outline wrap-input100">
              <input type="password" id="old_password" name="old_password" class="input100" v-on:focusout="checkField($event.target)" placeholder="Old Password"/>
              <span class="focus-input100"></span>
              <span class="symbol-input100">
                  <i class="fa fa-lock" aria-hidden="true"></i>
              </span>
            </div>
            <div class="form-outline wrap-input100">
                <input type="password" id="new_password" name="new_password" class="input100" v-on:focusout="checkField($event.target)" placeholder="New Password"/>
                <span class="focus-input100"></span>
                <span class="symbol-input100">
                    <i class="fa fa-lock" aria-hidden="true"></i>
                </span>
            </div>
            <div class="form-outline wrap-input100">
              <input type="password" id="new_password2" name="new_password2" class="input100" v-on:focusout="checkField($event.target)" placeholder="New Password Again"/>
              <span class="focus-input100"></span>
              <span class="symbol-input100">
                  <i class="fa fa-lock" aria-hidden="true"></i>
              </span>
          </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
            <button type="submit" class="btn btn-primary">Save changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</transition>
</template>

<script setup>
const currentUser = ref({
  name: localStorage.getItem('name'),
  username: localStorage.getItem('username'),
  birth_date: localStorage.getItem('birth_date'),
  personal_email: localStorage.getItem('personal_email'),
  company_email: localStorage.getItem('company_email'),
  phone_number: localStorage.getItem('phone_number'),
  address: localStorage.getItem('address')
});

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
      localStorage.setItem('role_level', response.data["role_level"]);
      localStorage.setItem('name', response.data["name"]);
      localStorage.setItem('username', response.data["username"]);
      localStorage.setItem('birth_date', response.data["birth_date"]);
      localStorage.setItem('personal_email', response.data["personal_email"]);
      localStorage.setItem('company_email', response.data["company_email"]);
      localStorage.setItem('phone_number', response.data["phone_number"]);
      localStorage.setItem('address', response.data["address"]);

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