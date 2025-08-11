<!-- About View for default route -->
<template>
  <div class="about">
    <h1>About the Car Parking App</h1>
    <p>This application is designed to help users manage parking lots efficiently.</p>
    <p>Features include:</p>
    <ul>
      <li>View available parking lots</li>
      <li>Edit parking lot details</li>
      <li>Manage user registrations and logins</li>
    </ul>
    <router-link to="/" class="btn btn-primary">Back to Home</router-link>
  </div>
</template>
<script>        
export default {
  name: 'AboutView',
  data() {
    return {};
  },
  methods: {}
};  
</script>
<style scoped>  
.about {
  text-align: center;
  margin-top: 50px;
}
.about h1 {
  font-size: 2.5em;
  margin-bottom: 20px;          
}
.about p {
  font-size: 1.2em;
  margin-bottom: 30px;
}   
.about ul {
  list-style-type: none;
  padding: 0;
}
.about li {
  font-size: 1.1em;
  margin: 10px 0;
}
</style>