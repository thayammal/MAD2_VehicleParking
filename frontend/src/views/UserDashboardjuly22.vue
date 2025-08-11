<template>
  <div class="user-dashboard">
    <nav class="navbar mb-4">
      <router-link to="/user-dashboard">Home</router-link> |
      <router-link to="/summary">Summary</router-link> |
      <router-link to="/">Logout</router-link>
      <br>
      
      <span class="ms-auto">Welcome, {{ this.username }}</span>
      <router-link to="/edituser">Edit Profile</router-link>
    </nav>
    <router-view/>
    <h2> Welcome {{ username }}</h2>
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
              <th>ID</th><th>Address</th><th>Price</th><th>Available</th><th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in results.lots" :key="lot.id">
              <td>{{ lot.id }}</td>
              <td>{{ lot.address }}</td>
              <td>₹{{ lot.price }}</td>
              <td>{{ lot.availableSpots }}/{{ lot.totalSpots }}</td>
              <td>
                <button @click="bookLot(lot.id)" class="btn-book">
                  Book
                </button>
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
      token: localStorage.getItem('token') || ''
    };
  },
  mounted() {
  const stored = localStorage.getItem('user');
  if (stored) {
    try {
      this.username = JSON.parse(stored).username || stored;
    } catch {
      this.username = stored;
    }
  }
},
  methods: {
    logout() {
      localStorage.removeItem('user');
      this.$router.push({ name: 'Login' });
    },
    async doSearch() {
      const config = { headers: { 'Authentication-Token': this.token } };

      try {
        const resp = await axios.get('/api/parkinglot', {
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
          availableSpots: lot.number_of_spots - occupiedCount,
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
}

}
};
</script>

<style scoped>
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
  margin-top: 16px;
}
.results-table th, td {
  padding: 8px;
  border: 1px solid #ccc;
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
