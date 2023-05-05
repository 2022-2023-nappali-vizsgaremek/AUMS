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
          <div v-else class="text-center justify-content-center">
            <h2>Profile Data</h2>
            <hr class="my-4">
            <h4>Name</h4>
            <p style="font-size: larger;">{{ currentUser.name }}</p>
            <h4>Personal Email</h4>
            <p style="font-size: larger;">{{ currentUser.personal_email }}</p>
            <h4>Phone Number</h4>
            <p style="font-size: larger;">{{ currentUser.phone }}</p>
            <h4>Address</h4>
            <p style="font-size: larger;">{{ currentUser.address }}</p>
            <button class="login100-form-btn mt-5" @click="logout">
              LOGOUT
            </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import axios from 'axios';

export default {
  name: 'LoginForm',
  setup() {
    const users = ref([]);
    const currentUser = ref([]);

    const header = {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      }
    };

    const loadUsers = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/users', header);
        users.value = response.data;
        getUserData();
      } catch (error) {
        console.error(error);
      }
    };

    const getUserData = () => {
      console.log(users.value);
      let email = localStorage.getItem('email');
      if (email.includes("@proj-aums.hu")) {
        email = email;
      }
      else {
        email += "@proj-aums.hu";
      }
      for (const user of users.value) {
        if (user.company_email == email) {
          currentUser.value = user;
          break;
        }
      }
    }

    const createNewPassword = () => {

    }

    const isAuthenticated = ref(false);
    const login = async () => {
      const email = document.querySelector('input[name="email"]').value;
      localStorage.setItem('email', email);
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
    onMounted(() => {
      loadUsers();
    });
    return {
      users,
      header,
      currentUser,
      isAuthenticated,
      login,
      logout,
      loadUsers,
      getUserData,
      createNewPassword,
    };
  },
};
</script>