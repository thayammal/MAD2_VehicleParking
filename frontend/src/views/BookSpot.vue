<template>
  <div class="container mt-4">
    <h2 class="mb-3">Book Your Parking Spot</h2>

    <form @submit.prevent="submitBooking" class="card p-4">
      <div class="mb-3">
        <label for="lotId" class="form-label">Lot ID</label>
        <input type="text" class="form-control" id="lotId" :value="lot_id" disabled>
      </div>
      <br>
      <br>
      <div class="mb-3">
        <label for="spotId" class="form-label">Spot ID</label>
        <input type="text" class="form-control" id="spotId" :value="spot_id" disabled>
      </div>
      <br>
      <br>
      <div class="mb-3">
        <label for="userId" class="form-label">User ID</label>
        <input type="text" class="form-control" id="userId" :value="user_id" disabled>
      </div>
      <br>
      <br>
      <div class="mb-3">
        <label for="vehicleNumber" class="form-label">Vehicle Number</label>
        <input v-model="vehicle_number" type="text" class="form-control" id="vehicleNumber" required>
      </div>
      <br>
      <br>
      <div class="d-flex justify-content-between">
        <button type="submit" class="btn btn-success">Reserve </button>
        <button type="button" class="btn btn-secondary" @click="cancel">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'BookSpot',
  data() {
    return {
      lot_id: null,
      spot_id: null,
      user_id: null,
      vehicle_number: '',
    };
  },
  async created() {
    // Fetch user info from localStorage
    const tokenData = JSON.parse(localStorage.getItem('user') || '{}');
    this.user_id = tokenData.user_id;

    this.lot_id = this.$route.query.lot_id;

    try {
      const token = localStorage.getItem('auth_token');  // consistent token key
      const response = await fetch(`http://localhost:5000/api/available-spot?lot_id=${this.lot_id}`, {
        headers: {
          'Authorization': `${token}`
        }
      });

      // Try parsing JSON (check if response is valid)
      const data = await response.json();

      if (response.ok && data.spot_number) {
        this.spot_id = data.spot_number;  
      } else {
        alert('⚠️ No available spot found in the selected lot.');
        this.$router.push('/user-dashboard');
      }

    } catch (err) {
      console.error('Error fetching spot:', err);
      alert('⚠️ Error contacting server. Please login again or try later.');
      this.$router.push('/user-dashboard');
    }
  },
  methods: {

    async submitBooking() {
      try {
        const token = localStorage.getItem('auth_token');  // use consistent token key
        const response = await fetch('http://localhost:5000/api/book-spot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `${token}`  // fix: add Bearer
          },
          body: JSON.stringify({
            lot_id: this.lot_id,
            spot_id: this.spot_id,
            user_id: this.user_id,
            vehicle_number: this.vehicle_number
          })
        });

        const result = await response.json();

        if (response.ok) {
          alert('✅ Spot booked successfully!');
          this.$router.push('/user-dashboard');
        } else {
          alert('❌ Booking failed: ' + (result.message || 'Unknown error'));
        }
      } catch (error) {
        console.error('Booking error:', error);
        alert('⚠️ Server error. Please try again later.');
      }
    },
    cancel() {
      this.$router.push('/user-dashboard');
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 500px;
}
</style>
