<template>
  <div class="register">
    <h1>User Registration</h1>

    <label for="email">Email:</label>
    <input type="email" v-model="email" placeholder="Enter your email" />
    <br /><br />

    <label for="username">Username:</label>
    <input type="text" v-model="username" placeholder="Choose a username" />
    <br /><br />

    <label for="password">Password:</label>
    <input type="password" v-model="password" placeholder="Create a password" />
    <br /><br />

    <label for="address"> Address :</label>
    <input type="text" v-model="address" placeholder="Your Address" />
    <br /><br />

    <label for="phone_number">Phone Number:</label>
    <input type="text" v-model="phone_number" placeholder="Your Phone Number" />
    <br /><br />

    <button @click="register">Register</button>

    <p v-if="successMessage" style="color: green">{{ successMessage }}</p>
    <p v-if="errorMessage" style="color: red">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterView',
  data() {
    return {
      email: '',
      username: '',
      password: '',
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    register() {
      this.successMessage = '';
      this.errorMessage = '';

      axios.post('http://localhost:5000/register', {
        email: this.email,
        username: this.username,
        password: this.password,
        address: this.address,
        phone_number: this.phone_number
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(() => {
        this.successMessage = 'Registration successful. Redirecting to login...';
        this.email = '';
        this.username = '';
        this.password = '';
        this.address = '';
        this.phone_number = '';
        setTimeout(() => this.$router.push('/login'), 1500);
      })
      .catch(error => {
        if (error.response && error.response.data && error.response.data.message) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = 'Registration failed. Please try again.';
        }
      });
    }
  }
};
</script>

<style scoped>
.register {
  padding: 2rem;
  max-width: 400px;
  margin: auto;
}
</style>
