<template>
  <div class="container mt-4">
    <h2>Release Parking Spot</h2>

    <!-- Form to confirm release -->
    <form @submit.prevent="submitRelease" v-if="!showDetails">
      <div class="mb-3">
        <label for="lot_id" class="form-label">Lot ID</label>
        <input type="text" id="lot_id" v-model="lot_id" class="form-control" readonly />
      </div>

      <div class="mb-3">
        <label for="spot_id" class="form-label">Spot ID</label>
        <input type="text" id="spot_id" v-model="spot_id" class="form-control" readonly />
      </div>

      <div class="mb-3">
        <label for="user_id" class="form-label">User ID</label>
        <input type="text" id="user_id" v-model="user_id" class="form-control" readonly />
      </div>

      <button type="submit" class="btn btn-success">Submit</button>
      <button type="button" class="btn btn-secondary ms-2" @click="goToDashboard">Cancel</button>
    </form>

    <!-- Table format for release summary -->
    <div v-if="showDetails" class="mt-4">
      <h4 class="mb-3">Release Summary</h4>
      <table class="table table-bordered table-striped">
        <tbody>
          <tr>
            <th>Lot ID</th>
            <td>{{ releaseResult.lot_id }}</td>
          </tr>
          <tr>
            <th>Spot ID</th>
            <td>{{ releaseResult.spot_id }}</td>
          </tr>
          <tr>
            <th>User ID</th>
            <td>{{ releaseResult.user_id }}</td>
          </tr>
          <tr>
            <th>Parking Time</th>
            <td>{{ formatDateTime(releaseResult.parking_timestamp) }}</td>
          </tr>
          <tr>
            <th>Release Time</th>
            <td>{{ formatDateTime(releaseResult.release_timestamp) }}</td>
          </tr>
          <tr>
            <th>Total Cost</th>
            <td>₹{{ releaseResult.total_cost }}</td>
          </tr>
        </tbody>
      </table>

      <button class="btn btn-primary mt-3" @click="goToDashboard">Go to Dashboard</button>
    </div>
  </div>
</template>


<script>
export default {
  name: 'ReleaseSpot',
  data() {
    return {
      lot_id: this.$route.query.lot_id || '',
      spot_id: this.$route.query.spot_id || '',
      user_id: '',
      releaseResult: null,
      showDetails: false
    };
  },
  created() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    this.user_id = user.user_id;
  },
  mounted() {
    this.releaseSpot();  // Automatically call release on mount
  },
  methods: {
    async releaseSpot() {
      const token = localStorage.getItem('auth_token');

      try {
        const res = await fetch('http://localhost:5000/api/release-spot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `${token}`
          },
          body: JSON.stringify({
            lot_id: this.lot_id,
            spot_id: this.spot_id,
            user_id: this.user_id
          })
        });

        const data = await res.json();

        if (res.ok) {
          this.releaseResult = data;
          this.showDetails = true;
        } else {
          alert('❌ Release failed: ' + data.message);
          this.$router.push('/user-dashboard');
        }

      } catch (error) {
        console.error('Fetch error:', error);
        alert('⚠️ Server error while releasing spot.');
        this.$router.push('/user-dashboard');
      }
    },
    formatDateTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    goToDashboard() {
      this.$router.push({ path: '/user-dashboard', query: { refresh: 'true' } });
    }
  }
};
</script>


<style scoped>
.container {
  max-width: 600px;
}
</style>
