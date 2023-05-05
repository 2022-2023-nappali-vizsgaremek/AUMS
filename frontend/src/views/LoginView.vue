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
            <h4>Email</h4>
            <p style="font-size: larger;">{{ currentUser.personal_email }}</p>
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

<script>
import { onMounted, ref } from 'vue';
import axios from 'axios';

export default {
  name: 'LoginForm',
  setup() {
    const users = ref([]);
    let currentUser = ref([]);
    const showModal = ref(false);

    const header = {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      }
    };

    const checkField = (field) => {
      if(field.value == ''){
        field.style.border = '1px solid red';
        return false;
      }else{
        clearBorder('#' + field.id);
        return true;
      }
    };

    const openModal = () => {
      showModal.value = true;
    };

    const closeModal = () => {
      showModal.value = false;
    };

    const saveChangedData = () => {
      let old_password = document.querySelector('input[name="password"]').value;
      let new_password = document.querySelector('input[name="new_password"]').value;
      let new_password2 = document.querySelector('input[name="new_password2"]').value;

      if (old_password != currentUser.value.password) {
        alert("Old password is incorrect!");
        return;
      }

      if (new_password != new_password2) {
        alert("New passwords are not the same!");
        return;
      }

      const data = {
        
      };
      console.log(currentUser.value);
      const response = axios.patch(`http://127.0.0.1:5000/users/${currentUser.value.id}`, data);
      
      showModal.value = false;
    }

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
      let email = localStorage.getItem('email');
      if (!email.includes("@proj-aums.hu")) {
        email += "@proj-aums.hu";
      }
      for (const user of users.value) {
        if (user.company_email == email) {
          currentUser.value = user;
          break;
        }
      }
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
      
      alert(response.data.message);
      localStorage.setItem('access_token', response.data["access_token"]);
      localStorage.setItem('role_level', response.data["role_level"]);
	  location.reload();
    }
    onMounted(() => {
      loadUsers();
    });
    return {
      users,
      header,
      showModal,
      currentUser,
      isAuthenticated,
      login,
      logout,
      loadUsers,
      openModal,
      closeModal,
      checkField,
      getUserData,
      saveChangedData,
    };
  },
};
</script>
<style>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  font-weight: bold;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Increase the z-index value */
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>