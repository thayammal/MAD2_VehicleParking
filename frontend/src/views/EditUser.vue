<template>
  <div class="container mt-4">
    <h2>Edit User Profile</h2>
    <form @submit.prevent="updateUser" class="mt-4">
      <div class="mb-3">
        <label class="form-label">Username :</label>
        <input type="text" class="form-control" :value="user.username" disabled>
      </div>
      <br>
      <br>
      <!-- Email -->
      <div class="mb-3">
        <label class="form-label">Email :</label>
        <input type="email" class="form-control" v-model="form.email" required>
      </div>
      <br>
      <br>
      <!-- Phone -->
      <div class="mb-3">
        <label class="form-label">Phone Number :</label>
        <input type="text" class="form-control" v-model="form.phone_number" required>
      </div>
      <br>
      <br>
      <!-- Password -->
      <div class="mb-3">
        <label class="form-label">Password :</label>
        <input type="password" class="form-control" v-model="form.password" required>
      </div>
      <br>
      <br>
      <button type="submit" class="btn btn-success">Save Changes</button>
      <router-link to="/user-dashboard" class="btn btn-secondary ms-2">Cancel</router-link>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: { id: null, username: '', email: '', phone_number: '' },
      form: { email: '', phone_number: '', password: '' }
    }
  },
  created() {
    const item = localStorage.getItem('user')
    if (!item) {
      alert('No user info found. Please log in again.')
      return this.$router.push('/login')
    }
    const u = JSON.parse(item)
    this.user = u
    this.form.email = u.email
    this.form.phone_number = u.phone_number
    // leave form.password blank for security
  },
  methods: {
    async updateUser() {
      try {
        const payload = {
          user_id: this.user.user_id,
          email: this.form.email,
          phone_number: this.form.phone_number,
          password: this.form.password
        }

        console.log('Sending payload:', payload)
        const res = await fetch('http://localhost:5000/api/userinfo', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        console.log('HTTP status:', res.status, 'Content-Type header:', res.headers.get('Content-Type'));

        const json = await res.json()
        if (res.ok && json.status === 'ok') {
          alert('User updated successfully')
          const updated = { ...this.user, ...{ email: this.form.email, phone_number: this.form.phone_number } }
          localStorage.setItem('user', JSON.stringify(updated))
          this.$router.push('/user-dashboard')
        } else {
          alert(`Update failed (${res.status}): ${json.message}`)
        }
      } catch (e) {
        console.error(e)
        alert('Network or server error')
      }
    }
  }
}
</script>

<style scoped>
.container { max-width: 600px; }
</style>
