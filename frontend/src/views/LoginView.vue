<template>
    <div class="container mt-5 mb-5">
        <div class="row justify-content-center mt-5">
            <transition name="alert-fade">
                <div role="alert" v-if="errorAlertVisible" style="z-index: 9999; position: absolute"
                    class="alert alert-danger text-center shadow mx-auto rounded rounded-3 mb-5 w-75 fs-5 alert-fade">
                    {{ alertMessage }}
                </div>
            </transition>

            <transition name="alert-fade">
                <div role="alert" v-if="successAlertVisible" style="z-index: 9999; position: absolute"
                    class="alert alert-success text-center shadow mx-auto rounded rounded-3 mb-5 w-75 fs-5 alert-fade">
                    {{ alertMessage }}
                </div>
            </transition>

            <div class="col-12 col-md-9 col-lg-7
                shadow rounded rounded-4 p-3 col-xl-6">
                <div class="card rounded rounded-4 p-0">
                    <div class="card-body rounded text-center rounded-4 p-5">
                        <div v-if="!isAuthenticated">
                            <h2 class="text-uppercase text-center mb-5">AUMS LOGIN</h2>
                            <img src="../images/logo.ico" alt="Logo" border="0"
                                class="p-3 shadow rounded rounded-5 img-fluid" style="border-radius: 50%">

                            <form class="mt-5">
                                <div class="form-outline wrap-inputcss">
                                    <input type="text" id="email" class="inputcss shadow rounded rounded-3"
                                        placeholder="Company Email/Username" v-model="email">

                                    <span class="focus-inputcss"></span>
                                    <span class="symbol-inputcss">
                                        <i class="fa fa-user" aria-hidden="true"></i>
                                    </span>
                                </div>

                                <div class="form-outline wrap-inputcss">
                                    <input type="password" id="password" class="inputcss shadow rounded rounded-3"
                                        placeholder="Password" v-model="password">

                                    <span class="focus-inputcss"></span>
                                    <span class="symbol-inputcss">
                                        <i class="fa fa-lock" aria-hidden="true"></i>
                                    </span>
                                </div>

                                <div class="text-center mt-5">
                                    <button type="button" @click="login"
                                        class="btn btn-primary btn-lg shadow rounded rounded-3 w-100">
                                        LOGIN
                                    </button>
                                </div>
                            </form>
                        </div>
                        <div v-else class="fs-5">
                            <h2 class="text-uppercase text-center mb-4">User, <span class="text-info">{{ currentUser.name }}</span></h2>
                            <div class="row">
                                <div class="col-md-6 col">
                                    <div class="rounded rounded-3 shadow p-2 w-100 mx-auto mt-3 info-box">
                                        <span class="text-uppercase text-center p-1">USERNAME<br>
                                            <span class="text-secondary">{{ currentUser.username }}</span>
                                        </span>
                                    </div>
                                    <hr>
                                    <div class="rounded rounded-3 shadow p-2 w-100 mx-auto mt-3 info-box">
                                        <span class="text-uppercase text-center p-1">BIRTH DATE<br>
                                            <span class="text-secondary">{{ currentUser.birth_date }}</span>
                                        </span>
                                    </div>
                                    <hr>
                                    <div class="rounded rounded-3 shadow p-2 w-100 mx-auto mt-3 info-box">
                                        <span class="text-uppercase text-center p-1">PHONE NUMBER<br>
                                            <span class="text-secondary">{{ currentUser.phone_number }}</span>
                                        </span>
                                    </div>
                                </div>
                                <div class="col-md-6 col">
                                    <div class="rounded rounded-3 shadow p-2 w-100 mx-auto mt-3 info-box">
                                        <span class="text-uppercase text-center p-1">COMPANY EMAIL<br>
                                            <span class="text-secondary">{{ currentUser.company_email }}</span>
                                        </span>
                                    </div>
                                    <hr>
                                    <div class="rounded rounded-3 shadow p-2 w-100 mx-auto mt-3 info-box">
                                        <span class="text-uppercase text-center p-1">PERSONAL EMAIL<br>
                                            <span class="text-secondary">{{ currentUser.personal_email }}</span>
                                        </span>
                                    </div>
                                    <hr>
                                    <div class="rounded rounded-3 shadow p-2 w-100 mx-auto mt-3 info-box">
                                        <span class="text-uppercase text-center p-1">ADDRESS<br>
                                            <span class="text-secondary">{{ currentUser.address }}</span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-5">
                                <button type="button" @click="showModal = true"
                                    class="btn btn-outline-primary btn-lg shadow rounded rounded-3 w-100 mb-3">
                                    CHANGE PASSWORD
                                </button>
                                <button type="button" @click="logout"
                                    class="btn btn-danger btn-lg shadow rounded rounded-3 w-100">
                                    LOGOUT
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal fade  blur" :class="{ show: showModal }" tabindex="-1"
            :style="{ display: showModal ? 'block' : 'none' }" @click="($event) => toggleModal($event)">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content rounded rounded-4 p-5">
                    <div class="card-header text-center">
                        <h2 class="text-uppercase text-center m-0">CHANGE PASSWORD</h2>
                    </div>
                    <form class="mt-4">
                        <div class="form-outline wrap-inputcss mb-3">
                            <input type="password" id="currentPassword" class="inputcss shadow rounded rounded-3"
                                placeholder="Current Password" v-model="currentPassword">

                            <span class="focus-inputcss"></span>
                            <span class="symbol-inputcss">
                                <i class="fa fa-lock" aria-hidden="true"></i>
                            </span>
                        </div>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-outline wrap-inputcss mt-3 mb-3">
                                    <input type="password" id="newPassword" class="inputcss shadow rounded rounded-3"
                                        placeholder="New Password" v-model="newPassword">

                                    <span class="focus-inputcss"></span>
                                    <span class="symbol-inputcss">
                                        <i class="fa fa-lock" aria-hidden="true"></i>
                                    </span>
                                </div>
                            </div>

                            <div class="col-md-6">
                                <div class="form-outline wrap-inputcss mt-3 mb-3">
                                    <input type="password" id="confirmPassword" class="inputcss shadow rounded rounded-3"
                                        placeholder="Confirm Password" v-model="confirmPassword">

                                    <span class="focus-inputcss"></span>
                                    <span class="symbol-inputcss">
                                        <i class="fa fa-lock" aria-hidden="true"></i>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div class="text-center mt-5">
                            <button type="button" @click="changePassword"
                                class="btn btn-primary btn-lg shadow rounded rounded-3 w-100">
                                CHANGE PASSWORD
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from "vue";
    import axios from "axios";

    const alertMessage = ref();
    const errorAlertVisible = ref(false);
    const successAlertVisible = ref(false);

    const email = ref("");
    const password = ref("");
    const showModal = ref(false);
    const isAuthenticated = ref(false);

    const newPassword = ref("");
    const currentPassword = ref("");
    const confirmPassword = ref("");

    const currentUser = ref(
    {
        name: localStorage.getItem("name"),
        address: localStorage.getItem("address"),
        username: localStorage.getItem("username"),
        birth_date: localStorage.getItem("birth_date"),
        phone_number: localStorage.getItem("phone_number"),
        company_email: localStorage.getItem("company_email"),
        personal_email: localStorage.getItem("personal_email"),
    });

    const usernameRegex = /^[a-zA-Z0-9_\-\.]+$/;
    const passwordRegex = /^[a-zA-Z0-9_\-\.]+$/;
    const emailRegex = /^([a-zA-Z0-9_\-\.]+)@proj-aums\.hu$/;

    const login = async () =>
    {
        if (!email.value || (!emailRegex.test(email.value) && !usernameRegex.test(email.value)))
        {
            alertMessage.value = "EMAIL IS REQUIRED, AND MUST BE VALID";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!password.value || !passwordRegex.test(password.value))
        {
            alertMessage.value = "PASSWORD IS REQUIRED, AND MUST BE VALID";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        const data =
        {
            password: password.value,
            company_email: email.value,
        };

        const response = await axios.post("http://127.0.0.1:5000/login", data).catch((error) =>
        {
            alertMessage.value = error.response.data.message.toUpperCase();
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
        })
        .then(response =>
        {
            if (response)
            {
                isAuthenticated.value = true;

                localStorage.setItem("name", response.data["name"]);
                localStorage.setItem("address", response.data["address"]);
                localStorage.setItem("username", response.data["username"]);
                localStorage.setItem("role_level", response.data["role_level"]);
                localStorage.setItem("birth_date", response.data["birth_date"]);
                localStorage.setItem("phone_number", response.data["phone_number"]);
                localStorage.setItem("access_token", response.data["access_token"]);
                localStorage.setItem("company_email", response.data["company_email"]);
                localStorage.setItem("personal_email", response.data["personal_email"]);

                location.reload();
            }
        });
    };

    const changePassword = async () =>
    {
        if (!currentPassword.value || !passwordRegex.test(currentPassword.value))
        {
            alertMessage.value = "CURRENT PASSWORD IS REQUIRED, AND MUST BE VALID";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!newPassword.value || !passwordRegex.test(newPassword.value))
        {
            alertMessage.value = "NEW PASSWORD IS REQUIRED, AND MUST BE VALID";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!confirmPassword.value || !passwordRegex.test(confirmPassword.value))
        {
            alertMessage.value = "CONFIRM PASSWORD IS REQUIRED, AND MUST BE VALID";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        const data =
        {
            new_password: newPassword.value,
            current_password: currentPassword.value,
            confirm_password: confirmPassword.value,
            access_token: localStorage.getItem("access_token"),
        };

        const header =
        {
            headers:
            { "Authorization": "Bearer " + localStorage.getItem("access_token") }
        };

        const response = await axios.post("http://127.0.0.1:5000/change_password", data, header).catch((error) =>
        {
            alertMessage.value = error.response.data.message.toUpperCase();
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
        })
        .then(response =>
        {
            if (response)
            {
                setTimeout(() => { successAlertVisible.value = false; }, 3000);
                alertMessage.value = response.data.message.toUpperCase();
                successAlertVisible.value = true;
            }
        });
    }

    const toggleModal = (event) =>
    {
        if (event.target === event.currentTarget)
        {
            showModal.value = !showModal.value;
            document.body.style.overflow = showModal.value ? "hidden" : "auto";
        }
    };

    const logout = () =>
    {
        localStorage.removeItem("access_token");
        isAuthenticated.value = false;
        location.reload();
    };
    if (localStorage.getItem("access_token"))  isAuthenticated.value = true
</script>

<style>
    .info-box
    {
        height: 150px;
        display: flex;
        overflow-y: auto;
        text-align: center;
        align-items: center;
        flex-direction: column;
        justify-content: center;
    }
    .blur
    {
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }

    .card
    {
        color: #c8bde8;
        background: #2f2655;
        box-shadow: 0 0 15px 0px rgba(35, 61, 77, 1);
    }

    .alert { transition: opacity 0.3s ease-in-out; }
    .alert-fade-enter, .alert-fade-leave-to { opacity: 0; }
    .alert-fade-enter-active, .alert-fade-leave-active { transition: opacity 0.250s; }

    hr
    {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
    }

    ::-webkit-scrollbar-thumb
    {
        border-radius: 0px;
        background: #2f2655;
    }
    ::-webkit-scrollbar-track
    {
        border-radius: 5px;
        box-shadow: inset 0 0 5px #3b3b3b;
    }
    ::-webkit-scrollbar { width: 20px; }
    ::-webkit-scrollbar-thumb:hover { background: #3c3463; }

    .modal
    {
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .modal-content
    {
        z-index: 998;
        background-color: #ffffff;
    }

    .modal-backdrop
    {
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 997;
        position: fixed;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .fade-enter-from, .fade-leave-to { opacity: 0; }
    .fade-enter-to, .fade-leave-from { opacity: 1; }
    .fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
</style>