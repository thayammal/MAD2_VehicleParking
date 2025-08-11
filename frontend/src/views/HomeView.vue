<!-- Home view for car parking app -->
<template>
  <div class="home">
    <h1>Welcome to the Car Parking App</h1>
    <p>This app allows you to manage parking lots efficiently.</p>
    <router-link to="/login" class="btn btn-primary"> Login </router-link>
    <router-link to="/register" class="btn btn-secondary ms-2"> Register </router-link>
  </div>
</template> 
<script>  
export default {
  name: 'HomeView',
  data() {
    return {};
  },
  methods: {}
};
</script>
<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
.home h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}
.home p {
  font-size: 1.2em;
  margin-bottom: 30px;
}
.home .btn {
  margin: 5px;
  padding: 10px 20px;
  font-size: 1em;
} 
</style>  