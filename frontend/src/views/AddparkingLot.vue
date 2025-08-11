<template>
  <div class="container mt-4">
    <h2 class="text-center mb-3">New Parking Lot</h2>
    <form @submit.prevent="addLot">
      <div class="form-group">
        <label>Prime Location Name:</label> 
        <input v-model="lot.prime_location_name" class="form-control" required />
      </div> <br> <br>

      <div class="form-group mt-2">
        <label>Address:</label>
        <textarea v-model="lot.address" class="form-control" rows="3" required></textarea>
      </div>  <br> <br>

      <div class="form-group mt-2">
        <label>Pin Code:</label>
        <input v-model="lot.pin_code" class="form-control" required />
      </div>  <br> <br>

      <div class="form-group mt-2">
        <label>Price (per hour):</label>
        <input type="number" v-model="lot.price" class="form-control" required />
      </div>  <br> <br>

      <div class="form-group mt-2">
        <label>Maximum Spots:</label>
        <input type="number" v-model="lot.number_of_spots" class="form-control" required />
      </div>  <br> <br>

      <div class="mt-4 text-center">
        <button class="btn btn-primary" type="submit">Add</button>
        <button class="btn btn-secondary ms-3" @click="goBack">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lot: {
        prime_location_name: "",
        address: "",
        pin_code: "",
        price: "",
        number_of_spots: ""
      }
    };
  },
  methods: {
    async addLot() {
      try {
        const response = await fetch('http://localhost:5000/api/parkinglot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.lot)
        });

        if (response.ok) {
          alert("Parking lot added successfully!");
          this.$router.push("/admin-dashboard");
        } else {
          const err = await response.json();
          alert("Error: " + err.message);
        }
      } catch (err) {
        console.error(err);
        alert("Server Error");
      }
    },
    goBack() {
      this.$router.go(-1);  // or use `this.$router.push('/admin/dashboard')`
    }
  }
};
</script>

<style scoped>
/* Optional custom styles */
</style>
