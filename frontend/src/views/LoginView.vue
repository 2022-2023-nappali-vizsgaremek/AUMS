<template>
  <div class="limiter">
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
            <p style="font-size: larger;">{{ currentUser.phone }}</p>
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
        <h5 class="modal-title text-center">Change Personal Data</h5>
        <hr>
        <form @submit.prevent="saveChangedData">
          <div class="modal-body">
            <div class="form-outline wrap-input100">
              <input type="text" id="fullName" autofocus  name="name" class="input100" placeholder="Name"/>
              <span class="focus-input100"></span>
              <span class="symbol-input100">
                  <i class="fa fa-user" aria-hidden="true"></i>
              </span>
            </div>
            <div class="form-outline wrap-input100">
              <input type="text" id="address" name="address" class="input100" placeholder="Address"/>
              <span class="focus-input100"></span>
              <span class="symbol-input100">
                  <i class="fa fa-home" aria-hidden="true"></i>
              </span>
            </div>
            <div class="form-outline wrap-input100">
              <input type="text" id="phone" name="phone" class="input100" placeholder="Phone number"/>
              <span class="focus-input100"></span>
              <span class="symbol-input100">
                  <i class="fa fa-phone" aria-hidden="true"></i>
              </span>
            </div>
            <div class="form-outline wrap-input100">
              <input type="email" id="email" name="email" class="input100" placeholder="Email"/>
              <span class="focus-input100"></span>
              <span class="symbol-input100">
                  <i class="fa fa-envelope" aria-hidden="true"></i>
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

    const openModal = () => {
      showModal.value = true;
    };

    const closeModal = () => {
      showModal.value = false;
    };

    const saveChangedData = () => {
      let name = document.querySelector('#fullName').value;
      let address = document.querySelector('#address').value;
      let phone = document.querySelector('#phone').value;
      let email = document.querySelector('#email').value;

      if (name == "") {
        name = currentUser.value.name;
      } else {
        currentUser.value.name = name;
      };
      if (address == "") {
        address = currentUser.value.address;
      } else {
        currentUser.value.address = address;
      };
      if (phone == "") {
        phone = currentUser.value.phone;
      } else {
        currentUser.value.phone = phone;
      };
      if (email == "") {
        email = currentUser.value.personal_email;
      } else {
        currentUser.value.personal_email = email;
      };
      console.log(currentUser.value);
      const response = axios.patch(`http://127.0.0.1:5000/users/${currentUser.value.id}`,currentUser.value, header)
      .catch((error) => {
        alert(error.response.data.message);
      })
      
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