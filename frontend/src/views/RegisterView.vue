<script setup>
import axios from 'axios';

const register = async () => {
    const name = document.querySelector('#fullName').value;
    const username = document.querySelector('#userName').value;
    const birthdate = document.querySelector('#birthDate').value;
    const address = document.querySelector('#address').value;
    const phone = document.querySelector('#phone').value;
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;

    const first_name = name.split(' ')[0];
    const last_name = name.split(' ')[1];

    const emailRegex = new RegExp('^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$');

    if(last_name == undefined || first_name == undefined || last_name == '' || first_name == ''){
        alert('Name must be in format: Firstname Lastname')
        document.querySelector('#fullName').style.border = '1px solid red';
        return;
    }else{
        clearBorder('#fullName');
    }

    if(phone.length != 11 || isNaN(phone)){
        alert('Phone number must be 11 digits')
        document.querySelector('#phone').style.border = '1px solid red';
        return;
    }else{
        clearBorder('#phone');
    }

    if(!emailRegex.test(email)){
        alert('Email is not valid')
        document.querySelector('#email').style.border = '1px solid red';
        return;
    }else{
        clearBorder('#email');
    }

    if(password.length < 3){
        alert('Password must be at least 3 characters')
        document.querySelector('#password').style.border = '1px solid red';
        return;
    }else{
        clearBorder('#password');
    }

    const data = {
        first_name: first_name,
        last_name: last_name,
        username: username,
        birth_date: birthdate,
        address: address,
        phone_number: phone,
        personal_email: email,
        password: password
    };

    const response = await axios.post('http://127.0.0.1:5000/register', data)
    .catch((error) => {
        alert(error.response.data.message);
    }).then((response) => {
        if (response) {
            alert(response.data.message);
            window.location.href = '/login';
        }
    });
};

const clearBorder = (id) => {
    document.querySelector(id).style.border = '1px solid #ced4da';
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
</script>

<template>
    <div class="mask d-flex align-items-center h-100 gradient-custom-3">
        <div class="container h-100">
            <div class="row d-flex justify-content-center align-items-center">
                <div class="col-12 col-md-9 col-lg-7 col-xl-6">
                    <div class="container">
                        <div class="card" style="border-radius: 15px;">
                            <div class="card-body p-5">
                                <h2 class="text-uppercase text-center mb-5">Register new user</h2>
                                <form>
                                    <div class="form-outline form-floating mb-2">
                                        <input type="text" id="fullName" autofocus  name="name" class="form-control form-control-lg" v-on:focusout="checkField($event.target)"/>
                                        <label for="fullName">Name</label>
                                    </div>

                                    <div class="form-outline form-floating mb-2">
                                        <input type="text" id="userName" name="username" class="form-control form-control-lg" v-on:focusout="checkField($event.target)"/>
                                        <label  for="userName">Username</label>
                                    </div>

                                    <div class="form-outline form-floating mb-2">
                                        <input type="date" id="birthDate" name="birthdate" class="form-control form-control-lg" v-on:focusout="checkField($event.target)"/>
                                        <label  for="birthDate">BirthDate</label>
                                    </div>

                                    <div class="form-outline form-floating mb-2">
                                        <input type="text" id="address" name="address" class="form-control form-control-lg" v-on:focusout="checkField($event.target)"/>
                                        <label  for="address">Address</label>
                                    </div>

                                    <div class="form-outline form-floating mb-2">
                                        <input type="text" id="phone" name="phone" class="form-control form-control-lg" v-on:focusout="checkField($event.target)"/>
                                        <label  for="phone">Phone number</label>
                                    </div>

                                    <div class="form-outline form-floating mb-2">
                                        <input type="email" id="email" name="email" class="form-control form-control-lg" v-on:focusout="checkField($event.target)"/>
                                        <label  for="email">Email</label>
                                    </div>

                                    <div class="form-outline form-floating mb-2">
                                        <input type="password" id="password" name="password" class="form-control form-control-lg" v-on:focusout="checkField($event.target)"/>
                                        <label  for="password">Password</label>
                                    </div>

                                    <div class="d-flex justify-content-center">
                                        <button type="button"
                                            @click="register"
                                            class="btn btn-success btn-block btn-lg gradient-custom-4 text-body">Register
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>