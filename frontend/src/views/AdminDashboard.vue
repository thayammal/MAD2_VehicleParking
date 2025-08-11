<template>
    <nav>
    <router-link to="/admin-dashboard"> Home </router-link> |
    <router-link to="/user-stat"> Users </router-link> |
    <router-link to="/search"> Search </router-link> |
    <router-link to="/admin-summary"> Summary </router-link> |
    <router-link to="/"> Logout </router-link>
    </nav>
  <router-view/>

  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <p class="mb-3">
              <strong> Parking Lots </strong>
              <span class="text-muted ms-2"> | <router-link class="btn btn-primary" to="/add-lot">+ Add Lot</router-link> </span>
      </p>
    </div>
    <br>

    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="lot in parkingLots" :key="lot.id" class="col">
        <div class="card h-100 shadow-sm d-flex flex-column">
          <div class="card-body d-flex flex-column">
            <p class="mb-2">
              <strong>{{ lot.prime_location_name }}</strong>
              <span class="text-muted ms-2"> | {{ lot.address }}</span>
            </p>
            <!-- Edit/Delete buttons -->
           <div class="my-2">
            <button class="edit-link" @click="editLot(lot.id)">Edit</button>
            <button class="delete-link" @click="deleteLot(lot.id)">Delete</button>
          </div>
            <p><strong>Spots:</strong> {{ lot.occupiedCount }} / {{ lot.number_of_spots }}</p>
            <div class="spot-grid mt-auto"> 
                <button 
                    v-for="n in lot.number_of_spots"
                    :key="`${lot.id}-${n}`"
                    class="spot-btn"
                    :class="getSpotStatus(lot, n) === 'A' ? 'btn btn-success' : 'btn btn-danger'"
                    @click="goToEditSpot(lot, n)"
                >
                    {{ n }} - {{ getSpotStatus(lot, n) }}
                </button>
           </div>         
          </div>
        </div>
      </div>
    </div>

    
    <!-- Modal for Occupied Spot Info -->
    
  </div>
</template>

<script>
export default {
  data() {
    return {
      parkingLots: [],
      currentUserId: 1 // Ensure this is set from your auth logic
    };
  },
  mounted() {
    this.fetchLots();
  },
  methods: {

    editLot(lotId) {
          this.$router.push({ name: 'EditLot', params: { id: lotId } });
      },

    async deleteLot(lotId) {
       if (!confirm('Are you sure you want to delete this lot?')) return;
        try {
        const res = await fetch(`http://localhost:5000/api/parkinglot`, {
        method: 'DELETE',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ id: lotId })
      });
      const json = await res.json();
      if (json.status === 'ok') {
        this.parkingLots = this.parkingLots.filter(l => l.id !== lotId);
      } else {
        alert(`Delete failed: ${json.message}`);
      }
    } catch (e) {
      console.error(e);
    }
    },
    async fetchLots() {
            const res = await fetch("http://localhost:5000/api/parkinglot");
            if (!res.ok) return console.error("Failed to load lots");

            const data = await res.json();
            this.parkingLots = data.lots.map(lot => {
                const spots = lot.spots || [];
                const occupiedCount = spots.filter(s => s.status === 'O').length;
                const availableCount = spots.filter(s => s.status === 'A').length;
                console.log(this.lot);

                return {
                ...lot,
                occupiedCount,
                availableCount,
                spots,  // keep for button display
                };
            });
            },

    getSpotStatus(lot, n) {
        const spot = lot.spots.find(s => parseInt(s.id) === n);
        return spot ? spot.status : 'A';  // default to 'A' if not found
        },
    
    goToEditSpot(lot,n) {
        this.$router.push({ 
          name: 'editspot',
          params: { lotId : lot.id, spotNum : n} 
        })
      },
        
  }
};
</script>


<style scoped>
.spot-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px; /* Adjust spacing between buttons */
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 60px;
}

.spot-btn {
  width: 50px;
  height: 40px;
  font-size: 14px;
  padding: 0;
  color : blue;
  text-align: center;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 280px;
}

.edit-link {
  margin-right: 1rem; /* adds ~16px spacing */
  color: #0d6efd; /* Bootstrap info color */
}
.delete-link {
  color: #dc3545; /* Bootstrap danger color */
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}


</style>
