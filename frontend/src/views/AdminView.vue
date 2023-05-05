<template>
  <div class="container mt-3">
    <div class="d-flex flex-row-reverse">
        <input type="text" class="form-control mb-3 w-50" placeholder="Search..." v-model="searchTerm" />
    </div>
    <div class="table-responsive">
    <table class="table table-dark table-bordered table-striped table-hover bg-white text-center rounded rounded-3 overflow-hidden">
        <thead>
            <tr class="align-middle">
                <th role="button" @click="toggleSort('id')">
                    <span class="nowrap">
                        ID
                        <i v-if="sortBy.field === 'id' && sortBy.order === 'asc'" class="fas fa-sort-up"></i>
                        <i v-else-if="sortBy.field === 'id'" class="fas fa-sort-down"></i>
                        <i v-else class="fas fa-sort"></i>
                    </span>
                </th>
                <th role="button" @click="toggleSort('name')">
                    <span class="nowrap">
                        Name
                        <i v-if="sortBy.field === 'name' && sortBy.order === 'asc'" class="fas fa-sort-up"></i>
                        <i v-else-if="sortBy.field === 'name'" class="fas fa-sort-down"></i>
                        <i v-else class="fas fa-sort"></i>
                    </span>
                </th>
                <th role="button" @click="toggleSort('username')">
                    <span class="nowrap">
                        Username
                        <i v-if="sortBy.field === 'username' && sortBy.order === 'asc'" class="fas fa-sort-up"></i>
                        <i v-else-if="sortBy.field === 'username'" class="fas fa-sort-down"></i>
                        <i v-else class="fas fa-sort"></i>
                    </span>
                </th>
                <th role="button" @click="toggleSort('company_email')">
                    <span class="nowrap">
                        Company Email
                        <i v-if="sortBy.field === 'company_email' && sortBy.order === 'asc'" class="fas fa-sort-up"></i>
                        <i v-else-if="sortBy.field === 'company_email'" class="fas fa-sort-down"></i>
                        <i v-else class="fas fa-sort"></i>
                    </span>
                </th>
                <th role="button" @click="toggleSort('personal_email')">
                    <span class="nowrap">
                        Personal Email
                        <i v-if="sortBy.field === 'personal_email' && sortBy.order === 'asc'" class="fas fa-sort-up"></i>
                        <i v-else-if="sortBy.field === 'personal_email'" class="fas fa-sort-down"></i>
                        <i v-else class="fas fa-sort"></i>
                    </span>
                </th>
                <th role="button" @click="toggleSort('birth_date')">
                    <span class="nowrap">
                        Date of Birth
                        <i v-if="sortBy.field === 'birth_date' && sortBy.order === 'asc'" class="fas fa-sort-up"></i>
                        <i v-else-if="sortBy.field === 'birth_date'" class="fas fa-sort-down"></i>
                        <i v-else class="fas fa-sort"></i>
                    </span>
                </th>
                <th role="button" @click="toggleSort('phone_number')">
                    <span class="nowrap">
                        Phone Number
                        <i v-if="sortBy.field === 'phone_number' && sortBy.order === 'asc'" class="fas fa-sort-up"></i>
                        <i v-else-if="sortBy.field === 'phone_number'" class="fas fa-sort-down"></i>
                        <i v-else class="fas fa-sort"></i>
                    </span>
                </th>
                <th role="button" @click="toggleSort('address')">
                    <span class="nowrap">
                        Address
                        <i v-if="sortBy.field === 'address' && sortBy.order === 'asc'" class="fas fa-sort-up"></i>
                        <i v-else-if="sortBy.field === 'address'" class="fas fa-sort-down"></i>
                        <i v-else class="fas fa-sort"></i>
                    </span>
                </th>


            </tr>
        </thead>
      <tbody>
        <tr class="align-middle" v-for="user in filteredUsers" :key="user.id" @click="openInfoModal(user.id)">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.company_email }}</td>
            <td>{{ user.personal_email }}</td>
            <td>{{ user.birth_date }}</td>
            <td>{{ user.phone_number }}</td>
            <td>{{ user.address }}</td>
        </tr>
      </tbody>
    </table>
</div>

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

                                <label for="birth_date" class="form-label">Date of Birth</label>
                                <input type="date" class="form-control" id="birth_date" v-model="selectedUser.birth_date">

                                <label for="phone_number" class="form-label">Phone Number</label>
                                <input type="text" class="form-control" id="phone_number" v-model="selectedUser.phone_number">

                                <label for="address" class="form-label">Address</label>
                                <input type="text" class="form-control" id="address" v-model="selectedUser.address">
                                
                                <label for="personal_email" class="form-label">Personal Email</label>
                                <input type="email" class="form-control" id="personal_email" v-model="selectedUser.personal_email">
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" @click="closeInfoModal">Close</button>
                            <button type="submit" class="btn btn-primary" @click="updateUser">Submit</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, computed } from 'vue';

export default {
    setup() {

        const header = {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        };

        const users = ref([]);
        const sortBy = ref({ field: '', order: 'asc' });
        const selectedUser = ref();
        const searchTerm = ref('');
        const showInfoModal = ref(false);

        const fetchUsers = async () => {
            const response = await axios.get('http://127.0.0.1:5000/users', header)
                response.data.forEach(user => {
                    user.birth_date = formatDate(user.birth_date);
                });
                users.value = response.data;
        }

        const updateUser = async () => {
            const data = {
                first_name: selectedUser.value.name.split(' ')[0],
                last_name: selectedUser.value.name.split(' ')[1],
                username: selectedUser.value.username,
                birth_date: selectedUser.value.birth_date,
                phone_number: selectedUser.value.phone_number,
                address: selectedUser.value.address,
                company_email: selectedUser.value.company_email,
                personal_email: selectedUser.value.personal_email,
            }
            const response = await axios.patch(`http://127.0.0.1:5000/users/${selectedUser.value.id}`, data, header)
            .catch((error) => {
                console.log(error);
            });
            fetchUsers();
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
        };

        const toggleSort = (field) => {
            if (sortBy.value.field === field) {
                sortBy.value.order = sortBy.value.order === 'asc' ? 'desc' : 'asc';
            } else {
                sortBy.value.field = field;
                sortBy.value.order = 'asc';
            }
        };

        const filteredUsers = computed(() => {
            let filtered = users.value;

            if (searchTerm.value !== '') {
                filtered = filtered.filter((user) =>
                Object.values(user).some((value) =>
                    String(value).toLowerCase().includes(searchTerm.value.toLowerCase())
                )
                );
            }

            if (sortBy.value.field !== '') {
                filtered.sort((a, b) => {
                if (a[sortBy.value.field] < b[sortBy.value.field]) return sortBy.value.order === 'asc' ? -1 : 1;
                if (a[sortBy.value.field] > b[sortBy.value.field]) return sortBy.value.order === 'asc' ? 1 : -1;
                return 0;
                });
            }

            return filtered;
        });

        fetchUsers();

        return {
            fetchUsers,
            users,
            formatDate,
            selectedUser,
            showInfoModal,
            openInfoModal,
            closeInfoModal,
            updateUser,
            filteredUsers,
            toggleSort,
            sortBy,
            searchTerm,
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
    .nowrap {
        white-space: nowrap;
    }
</style>