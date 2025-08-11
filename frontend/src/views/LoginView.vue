<template>
  <div class="login">
    <h1>Login Page</h1>
    
    <label for="email">Email:</label>
    <input type="text" name="email" placeholder="Enter your Email" v-model="email" />
    <br /><br />
    
    <label for="password">Password:</label>
    <input type="password" name="password" placeholder="Enter your Password" v-model="password" />
    <br /><br />
    
    <button type="button" @click="login">Login</button>
    
    <p v-if="errorMessage" style="color:red;">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    login() {
      axios.post('http://localhost:5000/login', {
        email: this.email,
        password: this.password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        const data = response.data;

        // Save to localStorage
        localStorage.setItem('auth_token', data.auth_token);
        localStorage.setItem('user', JSON.stringify({
          email: data.email,
          username: data.username,
          password:this.password,
          role: data.role,
          user_id: data.user_id,
          last_login_at: data.last_login_at
        }));

        // Redirect based on role
        if (data.role === 'admin') {
          this.$router.push('/admin-dashboard');
        } else {
          this.$router.push('/user-dashboard');
        }
      })
      .catch(error => {
        if (error.response) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = 'Network error. Please try again.';
        }
        console.error('Login error:', error);
      });
    }
  }
};
</script>

<style scoped>
.login {
  padding: 2rem;
  max-width: 400px;
  margin: auto;
}
</style>
