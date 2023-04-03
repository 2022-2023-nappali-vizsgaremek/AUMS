<script setup>
import axios from 'axios';

const login = async () => {
	const email = document.querySelector('input[name="email"]').value;
	const password = document.querySelector('input[name="pass"]').value;

	const data = {
		email: email,
		password: password
	};

	const response = await axios.post('http://10.0.14.11:5000/', data)
	.catch((error) => {
		alert(error.response.data.message);
	})
	.then(response => {
		if (response)
			alert(response.data.message);

	});
}


</script>
<template>
<div class="limiter">
		<div class="container-login100">
			<div class="wrap-login100">
				<div class="login100-pic" data-tilt>
					<img src="../images/img-01.png" alt="IMG">
				</div>

				<form class="login100-form">
					<span class="login100-form-title">
						Member Login
					</span>

					<div class="wrap-input100" data-validate = "Valid email is required: ex@abc.xyz">
						<input class="input100" type="text" name="email" placeholder="Email">
						<span class="focus-input100"></span>
						<span class="symbol-input100">
							<i class="fa fa-envelope" aria-hidden="true"></i>
						</span>
					</div>

					<div class="wrap-input100" data-validate = "Password is required">
						<input class="input100" type="password" name="pass" placeholder="Password">
						<span class="focus-input100"></span>
						<span class="symbol-input100">
							<i class="fa fa-lock" aria-hidden="true"></i>
						</span>
					</div>

					
				</form>
				<div class="container-login100-form-btn">
						<button class="login100-form-btn" @click="login">
							Login
						</button>
					</div>
			</div>
		</div>
	</div>

</template>
<style>
</style>

