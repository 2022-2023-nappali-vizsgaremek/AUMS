<template>
    <div class="container-fluid mt-5 pt-5">
        <div class="d-flex flex-row-reverse">
            <input type="text" class="form-control shadow mx-auto p-2 mb-3 w-50" placeholder="Search" v-model="searchTerm" />
        </div>
        <div class="table-responsive p-5">
            <table class="table table-dark table-bordered table-striped table-hover bg-white text-center rounded rounded-3 overflow-hidden">
                <thead>
                    <tr class="align-middle">
                        <th role="button" class="p-3" @click="toggleSort('id')">
                            <span class="nowrap">
                                ID
                                <i v-if="sortBy.field === 'id'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fas fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('name')">
                            <span class="nowrap">
                                Name
                                <i v-if="sortBy.field === 'name'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fas fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('username')">
                            <span class="nowrap">
                                Username
                                <i v-if="sortBy.field === 'username'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fas fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('company_email')">
                            <span class="nowrap">
                                Company Email
                                <i v-if="sortBy.field === 'company_email'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fas fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('personal_email')">
                            <span class="nowrap">
                                Personal Email
                                <i v-if="sortBy.field === 'personal_email'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fas fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('birth_date')">
                            <span class="nowrap">
                                Date of Birth
                                <i v-if="sortBy.field === 'birth_date'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fas fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('phone_number')">
                            <span class="nowrap">
                                Phone Number
                                <i v-if="sortBy.field === 'phone_number'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fas fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('address')">
                            <span class="nowrap">
                                Address
                                <i v-if="sortBy.field === 'address'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                            <i v-else class="fas fa-sort"></i>
                            </span>
                        </th>
                        <th>
                            Remove
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
                        <td>
                            <i role="button" class="fa fa-remove" @click.stop="removeUser(user.id)" style="font-size:35px;color:red"></i>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <transition name="fade">
            <div v-if="selectedUser" v-show="showInfoModal" class="modal" tabindex="-1">
                <div class="modal-dialog modal-lg">
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
        </transition>
    </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed } from "vue";

const header =
{
    headers:
    { "Authorization": "Bearer " + localStorage.getItem("access_token") }
};

const users = ref([]);
const selectedUser = ref();
const searchTerm = ref("");
const showInfoModal = ref(false);
const sortBy = ref({ field: "", order: "asc" });

const fetchUsers = async () =>
{
    const response = await axios.get("http://127.0.0.1:5000/users", header)
    response.data.forEach(user => { user.birth_date = formatDate(user.birth_date); });

    users.value = response.data;
}

const updateUser = async () =>
{
    const data =
    {
        address: selectedUser.value.address,
        username: selectedUser.value.username,
        birth_date: selectedUser.value.birth_date,
        phone_number: selectedUser.value.phone_number,
        company_email: selectedUser.value.company_email,
        last_name: selectedUser.value.name.split(" ")[1],
        first_name: selectedUser.value.name.split(" ")[0],
        personal_email: selectedUser.value.personal_email,
    }

    const response = await axios.patch(`http://127.0.0.1:5000/users/${selectedUser.value.id}`, data, header)
    .catch((error) => { alert("FAILED TO UPDATE USER") })
    .then(() => { alert("USER UPDATED") });

    fetchUsers();
}

const removeUser = async (userId) =>
{
    if(window.confirm("Are you sure you want to delete this user?") === false) return;
    const response = await axios.delete(`http://127.0.0.1:5000/users/${userId}`, header)
    alert(response.data.message);

    fetchUsers();
}

const formatDate = (dateString) =>
{
    const date = new Date(dateString);
    return date.toISOString().split("T")[0];
};

const openInfoModal = (userId) =>
{
    selectedUser.value = users.value.find(user => user.id === userId);
    showInfoModal.value = true;
};

const closeInfoModal = () =>
{ showInfoModal.value = false; };

const toggleSort = (field) =>
{
    if (sortBy.value.field === field) sortBy.value.order = sortBy.value.order === "asc" ? "desc" : "asc";
    else
    {
        sortBy.value.field = field;
        sortBy.value.order = "asc";
    }
};

const filteredUsers = computed(() =>
{
    let filtered = users.value;

    if (searchTerm.value !== "")
    {
        filtered = filtered.filter((user) =>
        Object.values(user).some((value) =>
            String(value).toLowerCase().includes(searchTerm.value.toLowerCase()) ));
    }

    if (sortBy.value.field !== "")
    {
        filtered.sort((a, b) =>
        {
            if (a[sortBy.value.field] < b[sortBy.value.field]) return sortBy.value.order === "asc" ? -1 : 1;
            if (a[sortBy.value.field] > b[sortBy.value.field]) return sortBy.value.order === "asc" ? 1 : -1;
            return 0;
        });
    }

    return filtered;
});

fetchUsers();
</script>


<style scoped>
    .modal
    {
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        z-index: 9999;
        position: fixed;
        font-weight: bold;
        align-items: center;
        justify-content: center;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .nowrap { white-space: nowrap; }
    .fade-enter-from, .fade-leave-to { opacity: 0; }
    .fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
</style>