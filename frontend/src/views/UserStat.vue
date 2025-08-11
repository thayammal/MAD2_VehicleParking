<template>
  <div v-if="isAdmin" class="container mt-4">
    <nav class="mb-4">
      <router-link to="/admin-dashboard">Home</router-link> |
      <router-link to="/user-stat">Users</router-link> |
      <router-link to="/search">Search</router-link> |
      <router-link to="/summary">Summary</router-link> |
      <router-link to="/">Logout</router-link>
    </nav>

    <h2>Registered Users</h2>
    <table class="styled-table">
      <thead>
        <tr><th>ID</th>  <th>Username</th>   <th>Email</th>     <th> Address </th>     <th> Phone Number </th>     </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.email }}</td>
          <td> {{ u.address }}</td>
          <td> {{ u.phone_number }}</td>
        </tr>
        <tr v-if="!loading && users.length === 0">
          <td colspan="4" class="text-center">No users found.</td>
        </tr>
      </tbody>
    </table>

    <div v-if="loading" class="text-center mt-3">Loading users...</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserStat',
  data() {
    return {
      users: [],
      loading: false,
      error: null,
      isAdmin: false
    }
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const token = localStorage.getItem('auth_token')
    this.isAdmin = token && user.role === 'admin'

    if (!this.isAdmin) {
      this.$router.replace('/')
    } else {
      this.fetchUsers()
    }
  },
  methods: {
    formatDate(dt) {
      return new Date(dt).toLocaleString()
    },
    async fetchUsers() {
      this.loading = true
      this.error = null

      try {
        const token = localStorage.getItem('auth_token')
        const res = await axios.get('http://127.0.0.1:5000/api/userinfo', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        const data = res.data
        if (Array.isArray(data.users)) {
          this.users = data.users
        } else {
          this.error = data.message || 'Invalid response format.'
        }
      } catch (e) {
        console.error(e)
        this.error = e.response?.data?.message || 'Network/server error'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
nav a.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}
.styled-table {
  border-collapse: collapse;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  font-size: 0.9em;
  min-width: 600px;
  box-shadow: 0 0 15px rgba(0,0,0,0.1);
}

.styled-table thead tr {
  background: #2E8B57;
  color: #ffffff;
  text-align: left;
}

.styled-table th,
.styled-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
}

.styled-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.styled-table tbody tr:hover {
  background-color: #d1f7e0;
}

.styled-table tbody tr.active-row {
  font-weight: bold;
  color: #2E8B57;
}

.no-data {
  text-align: center;
  color: #888;
}



</style>
