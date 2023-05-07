<template>
    <div class="container mt-5 mb-5">
        <transition name="alert-fade">
            <div role="alert" v-if="errorAlertVisible"  style="z-index: 9999; position: absolute"
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

        <div class="row justify-content-center mt-5">
            <div class="col-12 col-md-9 col-lg-7
                shadow rounded rounded-4 p-3 col-xl-6">
                <div class="card rounded rounded-4 p-0">
                    <div class="card-body rounded rounded-4 p-5">
                        <h2 class="text-uppercase text-center mb-5">Register new user</h2>
                        <form>
                            <div class="form-outline wrap-input100">
                                <input type="text" id="firstName" class="input100 shadow rounded rounded-3"
                                placeholder="First Name" v-model="firstName">

                                <span class="focus-input100"></span>
                                <span class="symbol-input100">
                                <i class="fa fa-user" aria-hidden="true"></i>
                                </span>
                            </div>

                            <div class="form-outline wrap-input100">
                                <input type="text" id="lastName" class="input100 shadow rounded rounded-3"
                                placeholder="Last Name" v-model="lastName">

                                <span class="focus-input100"></span>
                                <span class="symbol-input100">
                                    <i class="fa fa-user" aria-hidden="true"></i>
                                </span>
                            </div>

                            <div class="form-outline wrap-input100">
                                <input type="date" id="birthDate" class="input100 shadow rounded rounded-3"
                                placeholder="BirthDate" v-model="birthDate">

                                <span class="focus-input100"></span>
                                <span class="symbol-input100">
                                    <i class="fa fa-calendar" aria-hidden="true"></i>
                                </span>
                            </div>

                            <div class="form-outline wrap-input100">
                                <input type="text" id="address" class="input100 shadow rounded rounded-3"
                                placeholder="Address" v-model="address">

                                <span class="focus-input100"></span>
                                <span class="symbol-input100">
                                    <i class="fa fa-home" aria-hidden="true"></i>
                                </span>
                            </div>

                            <div class="form-outline wrap-input100">
                                <input type="text" id="phone" class="input100 shadow rounded rounded-3"
                                placeholder="Phone number" v-model="phone">

                                <span class="focus-input100"></span>
                                <span class="symbol-input100">
                                    <i class="fa fa-phone" aria-hidden="true"></i>
                                </span>
                            </div>

                            <div class="form-outline wrap-input100">
                                <input type="email" id="email" class="input100 shadow rounded rounded-3"
                                placeholder="Email Address" v-model="email">

                                <span class="focus-input100"></span>
                                <span class="symbol-input100">
                                    <i class="fa fa-envelope" aria-hidden="true"></i>
                                </span>
                            </div>

                            <div class="form-outline wrap-input100">
                                <select id="roleLevel"
                                    v-model="roleLevel" class="input100 shadow rounded rounded-3" >
                                        <option value="" disabled selected>Role Level</option>
                                        <option v-for="i in 5" :key="i" :value="i">{{ i }}</option>
                                </select>
                                <span class="focus-input100"></span>
                                <span class="symbol-input100">
                                    <i class="fa fa-level-up" aria-hidden="true"></i>
                                </span>
                            </div>

                            <div class="d-flex justify-content-center mt-4">
                                <button type="button" @click="register" class="btn-lg rounded
                                login100-form-btn btn-block gradient-custom-4 shadow rounded-3">Register</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import axios from "axios";
    import { ref } from "vue";

    const header =
    {
        headers:
        { "Authorization": "Bearer " + localStorage.getItem("access_token") }
    };

    const phone = ref("");
    const email = ref("");
    const address = ref("");
    const lastName = ref("");
    const firstName = ref("");
    const birthDate = ref("");
    const roleLevel = ref("");

    let alertMessage = ref();
    let errorAlertVisible = ref(false);
    let successAlertVisible = ref(false);

    const register = async () =>
    {
        const roleRegex = /^[1-5]$/;
        const phoneRegex = /^\d{11}$/;
        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        const addressRegex = /^[a-zA-Z0-9\s,."-]{3,}$/;
        const emailRegex = /^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$/;
        const nameRegex = /^[a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ]+(([\" ][a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ])?[a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ]*)*$/;

        if (!nameRegex.test(firstName.value))
        {
            alertMessage.value = "FIRST NAME IS REQUIRED, AND CAN ONLY CONTAIN LETTERS";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!nameRegex.test(lastName.value))
        {
            alertMessage.value = "LAST NAME IS REQUIRED, AND CAN ONLY CONTAIN LETTERS";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!dateRegex.test(birthDate.value))
        {
            alertMessage.value = "BIRTH DATE IS REQUIRED, AND MUST BE IN YYYY-MM-DD FORMAT";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!addressRegex.test(address.value))
        {
            alertMessage.value = "ADDRESS MUST BE AT LEAST 3 CHARACTERS LONG, AND CAN ONLY CONTAIN LETTERS, NUMBERS AND SOME SPECIAL CHARACTERS";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!phoneRegex.test(phone.value))
        {
            alertMessage.value = "PHONE NUMBER MUST BE 11 DIGITS";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!emailRegex.test(email.value))
        {
            alertMessage.value = "EMAIL MUST CONTAIN '@' AND '.' AND CAN ONLY CONTAIN LETTERS, NUMBERS AND SOME SPECIAL CHARACTERS";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        if (!roleRegex.test(roleLevel.value))
        {
            alertMessage.value = "ROLE LEVEL MUST BE BETWEEN 1 AND 5";
            setTimeout(() => { errorAlertVisible.value = false; }, 3000);
            errorAlertVisible.value = true;
            return;
        }

        const data =
        {
            address: address.value,
            phone_number: phone.value,
            last_name: lastName.value,
            personal_email: email.value,
            birth_date: birthDate.value,
            first_name: firstName.value,
            role_level: roleLevel.value
        };

        const response = await axios.post("http://127.0.0.1:5000/register", data, header)
        .catch((error) =>
        {
            if (error.response)
            {
                alertMessage.value = error.response.data.message.toUpperCase();
                setTimeout(() => { errorAlertVisible.value = false; }, 3000);
                errorAlertVisible.value = true;
            }
        })
        .then((response) =>
        {
            if (response)
            {
                successAlertVisible.value = true;
                alertMessage.value = "USER SUCCESSFULLY REGISTERED";

                setTimeout(() =>
                {
                    successAlertVisible.value = false;
                    window.location.href = "/login";
                }, 3000);
            }
            else
            {
                alertMessage.value = "UNABLE TO REGISTER USER, PLEASE TRY AGAIN LATER";
                setTimeout(() => { errorAlertVisible.value = false; }, 3000);
                errorAlertVisible.value = true;
            }
        });
    };
</script>

<style>
    .card
    {
        color: #c8bde8;
        background: #2f2655;
        box-shadow: 0 0 15px 0px rgba(35, 61, 77, 1);
    }

    .alert { transition: opacity 0.3s ease-in-out; }
    .alert-fade-enter, .alert-fade-leave-to { opacity: 0; }
    .alert-fade-enter-active, .alert-fade-leave-active { transition: opacity 0.250s; }

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
</style>