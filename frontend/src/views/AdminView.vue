<template>
  <div class="container mt-3">
    <table class="table table-striped table-bordered bg-white">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Date of Birth</th>
          <th>Phone Number</th>
          <th>Address</th>
          <th>Company Email</th>
          <th>Personal Email</th>
          <th>Username</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id" @click="openInfoModal(user.id)">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.birth_date }}</td>
            <td>{{ user.phone_number }}</td>
            <td>{{ user.address }}</td>
            <td>{{ user.company_email }}</td>
            <td>{{ user.personal_email }}</td>
            <td>{{ user.username }}</td>
        </tr>
      </tbody>
    </table>

<!-- Info Modal -->
        <div v-if="selectedUser" v-show="showInfoModal" class="modal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Update user</h5>
                        <button type="button" class="btn-close" @click="closeInfoModal"></button>
                    </div>
                    <form @submit.prevent="">
                        <div class="modal-body">
                            <div class="mb-3">
                                <label for="name" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name" v-model="selectedUser.name">

                                <label for="username" class="form-label">Username</label>"
                                <input type="text" class="form-control" id="username" v-model="selectedUser.username">

                                <label for="birth_date" class="form-label">Date of Birth</label>
                                <input type="date" class="form-control" id="birth_date" v-model="selectedUser.birth_date">

                                <label for="phone_number" class="form-label">Phone Number</label>
                                <input type="text" class="form-control" id="phone_number" v-model="selectedUser.phone_number">

                                <label for="address" class="form-label">Address</label>
                                <input type="text" class="form-control" id="address" v-model="selectedUser.address">

                                <label for="company_email" class="form-label">Company Email</label>"
                                <input type="email" class="form-control" id="company_email" v-model="selectedUser.company_email">
                                
                                <label for="personal_email" class="form-label">Personal Email</label>"
                                <input type="email" class="form-control" id="personal_email" v-model="selectedUser.personal_email">
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" @click="closeInfoModal">Close</button>
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
    setup() {

        const header = {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        };

        const users = ref([]);
        const selectedUser = ref();
        const showInfoModal = ref(false);

        const fetchUsers = async () => {
            const response = await axios.get('http://127.0.0.1:5000/users', header)
                response.data.forEach(user => {
                    user.birth_date = formatDate(user.birth_date);
                });
                users.value = response.data;
        }

        const formatDate = (dateString) => {
            const date = new Date(dateString);
            return date.toISOString().split('T')[0];
        };

        const openInfoModal = (userId) => {
            selectedUser.value = users.value.find(user => user.id === userId);
            showInfoModal.value = true;
        };

        const closeInfoModal = () => {
            showInfoModal.value = false;
        }

        fetchUsers();

        return {
            fetchUsers,
            users,
            formatDate,
            selectedUser,
            showInfoModal,
            openInfoModal,
            closeInfoModal
        };
    },
};
</script>

<style scoped>
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