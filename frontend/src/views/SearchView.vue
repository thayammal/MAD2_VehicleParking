<template>
  <nav class="mb-4">
      <router-link to="/admin-dashboard">Home</router-link> |
      <router-link to="/user-stat">Users</router-link> |
      <router-link to="/search">Search</router-link> |
      <router-link to="/admin-summary">Summary</router-link> |
      <router-link to="/">Logout</router-link>
    </nav>

    <h2> Search Users or Parking Lots</h2>
    <p>Use the search bar below to find users by ID or parking lots by location.</p>
  <div class="search-container">
    <div class="search-controls">
      
      <label for="search-criterion">Search By:</label>      

      <select v-model="criterion" class="search-select">
        <option value="location">Location</option>
        <option value="userid">User ID</option>
      </select>
      <input
        v-model="query"
        @keyup.enter="doSearch"
        type="text"
        placeholder="Search..."
        class="search-input"
      />
      <button @click="doSearch" class="search-btn">
        🔍
      </button>
    </div>

    <div v-if="results" class="search-results">
      <div v-if="criterion === 'location' && results?.lots?.length">
          <ParkingDetail
        v-for="lot in results.lots"
          :key="lot.id"
          :lot="lot"
        />
    </div>
     <div v-else-if="results?.user">
  <UserInfo :user="results.user" :reservations="results.reservations" />
</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ParkingDetail from '@/components/ParkingDetail.vue'
import UserInfo from '@/components/UserInfo.vue'
export default {
  name: 'SearchView',
  components: { 
    ParkingDetail,
    UserInfo
  },
  
  data() {
    return {
      criterion: 'location',
      query: '',
      results: null,
      token: localStorage.getItem('token') || ''  
    }
  },
  mounted() {
    // Called when the component is added to the DOM
    this.token = localStorage.getItem('token') || ''
  },
  methods: {
    async doSearch() {
      this.results = null;                          // ✅ clear previous results
      console.log("🧪 Searching for:", this.query);

  const config = {
    headers: { 'Authentication-Token': this.token }
  };
try {
  let resp;
  if (this.criterion === 'location') {
    resp = await axios.get('/api/parkinglot', {
      params: { query: this.query },
      ...config
    });

    this.results = {
      lots: resp.data.lots ?? resp.data   // expected lots list
    };
    console.log('lot details', this.results.lots)

  } else {
    resp = await axios.get(`/api/search/userinfo/${this.query}`, {
      params: { query: this.query },
      ...config
    });

    //const raw = resp.data.lots ?? resp.data;
    const raw = resp.data.data ?? {};
    const {
      reservations = [],
      ...userDetails
    } = raw;

    this.results = {
      user: userDetails,
      reservations
    };
  }

  //console.log('Search results:', this.results.lots);
//  console.log("Search results:", JSON.stringify(this.results, null, 2));

} catch (error) {
  console.error("Search failed:", error);
  this.results = null;
}

}
    
  }
}
</script>


<style scoped>
.search-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 10px;
}

.search-controls {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 16px;
}

.search-select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  font-size: 14px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.search-btn {
  padding: 8px 12px;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #1565c0;
}

.search-results {
  margin-top: 20px;
}

</style>