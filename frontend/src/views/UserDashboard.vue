<template>
  <div class="user-dashboard">
    <nav class="navbar mb-4">
      <router-link to="/user-dashboard">Home</router-link> |
      <router-link to="/user-summary">Summary</router-link> |
      <router-link to="/">Logout</router-link>
      <br>
      
      <router-link to="/edituser">Edit Profile</router-link>
    </nav>
    <router-view/>
    <h2> Welcome {{ username }}</h2> 

<!-- 👇 Recent Reservations Section -->
<div v-if="recentReservations.length" class="section-card">
  <h3 class="section-title">📌 Recent Reservations</h3>
  <table class="results-table">
    <thead>
      <tr>
        <th>Lot ID</th>
        <th>Location</th>
        <th>Vehicle Number</th>
        <th>Parking Time</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="res in recentReservations" :key="res.lot_id + res.parking_timestamp">
        <td>{{ res.lot_id }}</td>
        <td>{{ res.location }}</td>
        <td>{{ res.vehicle_number }}</td>
        <td>{{ res.parking_timestamp }}</td>
        <td>
           <button
            v-if="res.reservation_status === 'Release'"
            @click="goToReleasePage(res.lot_id, res.spot_id)"
            class="btn btn-danger"
          >Release</button>
          <span v-else>Parked Out</span>
        </td>
      </tr>
    </tbody>
  </table>
</div>
</div>
<!-- Divider -->
    <hr />

<!-- 🔍 Search Section -->
<div class="section-card">
  <h3 class="section-title">🔍 Search Parking Lots</h3>
  <p>Use the search bar below to find parking lots by location or pincode.</p>

  <div class="search-container">
    <div class="search-controls">
      <label for="search-criterion">Search By:</label>
      <select v-model="criterion" class="search-select">
        <option value="location">Location</option>
        <option value="pincode">Pincode</option>
      </select>

      <input
        v-model="query"
        @keyup.enter="doSearch"
        type="text"
        placeholder="Enter location or pincode"
        class="search-input"
      />

      <button type="button" @click="doSearch" class="search-btn">🔍</button>
    </div>

    <div v-if="results">
      <table class="results-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Address</th>
            <th>Price</th>
            <th>Available</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lot in results.lots" :key="lot.id">
            <td>{{ lot.id }}</td>
            <td>{{ lot.address }}</td>
            <td>₹{{ lot.price }}</td>
            <td>{{ lot.availableSpots }}/{{ lot.totalSpots }}</td>
            <td>
              <router-link :to="{ path: '/book-spot', query: { lot_id: lot.id } }">
                <button class="btn btn-primary">Book</button>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="!results.lots.length" class="no-results">No lots found.</div>
    </div>
  </div>
</div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'UserDashboard',
  data() {
    return {
      criterion: 'location',
      query: '',
      results: null,
      username: '',
      token: localStorage.getItem('auth_token') || '',
      recentReservations: []
    };
  },
  mounted() {
  const lotId = this.$route.params.lot_id;
  const spotId = this.$route.params.spot_id;
  console.log('Navigated to release:', lotId, spotId);
  this.token = localStorage.getItem('auth_token') || ''
  const stored = localStorage.getItem('user');
  if (stored) {
    try {
      this.username = JSON.parse(stored).username || stored;
    } catch {
      this.username = stored;
    }
    }
    this.fetchRecentReservations(); // fetch anyway

  // If user just returned from releasing
  if (this.$route.query.refresh === 'true') {
    console.log("🔁 Refreshing dashboard after release...");
    this.fetchRecentReservations();
    this.$router.replace({ query: {} });  // Clears URL query after reload

  }
},
  methods: {
    logout() {
      localStorage.removeItem('user');
      this.$router.push({ name: 'Login' });
      },

    async fetchRecentReservations() {
      const config = { headers: { 'Authorization': this.token } };
      try {
        const resp = await axios.get(`http://localhost:5000/api/recent-reservations`, config);
        console.log('Fetched recent:', resp.data.recent); 
        this.recentReservations = resp.data.recent || [];
        
      } 
      catch (err) {
        console.error('Error loading recent reservations:', err);
      }
    },

   goToReleasePage(lotId, spotId) {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      const userId = user.user_id;

    this.$router.push({
      name: 'ReleaseSpot',
        query: {
        lot_id: lotId,
        spot_id: spotId,
        user_id: userId
      }
    });
  },

    async doSearch() {
    const config = { headers: { 'Authorization': this.token } };

    try {
        const resp = await axios.get(`http://localhost:5000/api/parkinglot`, {
        params: {
        query: this.criterion === 'location' ? this.query : undefined,
        pincode: this.criterion === 'pincode' ? this.query : undefined
      },
      ...config
        });
        const lots = resp.data.lots || [];
        this.results = {
        lots: lots.map(lot => {
            const spots = Array.isArray(lot.spots) ? lot.spots : [];
            const occupiedCount = spots.filter(s => s.status === 'O').length;
        return {
          id: lot.id,
          address: lot.address,
          price: lot.price,
          totalSpots: lot.number_of_spots,
          availableSpots: lot.available_spots,
          spots
        };
      })
    };
  } catch (err) {
    if (err.response && err.response.status === 404) {
      this.results = { lots: [] };
    } else {
      console.error('Search error:', err);
    }
  }
},

}
};
</script>

<style scoped>
.section-card {
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 20px;
  margin: 2rem auto;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  max-width: 1000px;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 600;
}
.search-container {
  max-width: 800px;
  margin: 1rem auto;
}
.search-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}
.search-select, .search-input, .search-btn {
  padding: 8px 12px;
  font-size: 14px;
}
.search-input {
  flex: 1;
}
.search-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  cursor: pointer;
}
.search-btn:hover {
  background-color: #1565c0;
}
.results-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
  font-size: 15px;
}

.results-table th {
  background-color: #f0f4f8;
  color: #333;
  text-align: left;
}

.results-table th, .results-table td {
  padding: 10px;
  border: 1px solid #dee2e6;
}

.results-table td {
  background-color: #fafafa;
}
.btn-book {
  background: #28a745;
  color: white;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
}
.no-results {
  margin-top: 16px;
  color: #555;
}
</style>
