<template>
  <div class="lot-card">
    <h4>Lot ID: {{ lot.id }}</h4>
    <table class="lot-table">
      <thead>
        <tr>
          <th> Lot ID </th>
          <th>Prime Location</th>
          <th> Address </th>
          <th>Number of Spots</th>
          <th> Availble Spots</th>
          <th> Price (₹)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ lot.id }}</td>
          <td>{{ lot.prime_location_name }}</td>
          <td>{{ lot.address }}</td>
          <td>{{ lot.number_of_spots }}</td>
          <td>{{ lot.spots.filter(s => s.status === 'A').length }}</td>
          <td>{{ lot.price }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'ParkingDetail',
  props: {
    lot: Object
  }
}
</script>

<style scoped>
.lot-card {
  margin: 16px 0;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.lot-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
}

.lot-table th,
.lot-table td {
  padding: 8px 12px;
  border: 1px solid #ccc;
}

.lot-table th {
  background-color: #e0e0e0;
}
</style>
<!-- 
<template>
  <div class="lot-card">
    <h3 class="lot-name">{{ lot.prime_location_name }}</h3>
    <p><strong>Address:</strong> {{ lot.address }} (Pin: {{ lot.pin_code }})</p>
    <p><strong>Spots:</strong> {{ lot.available_spots }} / {{  lot.number_of_spots }}</p>
    <p><strong>Price:</strong> ₹{{ lot.price }}</p>
    <div class="spot-grid">
      <button
      v-for="n in lot.number_of_spots"
      :key="`${lot.id}-${n}`"
      class="spot-btn"
      :class="getSpotStatus(n) === 'A' ? 'available' : 'occupied'"
      disabled
      >
        {{ getSpotStatus(n) }}
      </button>

    </div>
  </div>
</template>

<script>
export default {
  name: 'ParkingDetail',
  props: {
    lot: {
      type: Object,
      required: true
    }
  },
  methods: {
    getSpotStatus(n) {
      return n <= this.lot.available_spots ? 'A' : 'O';
    }
  }
}
</script>

<style scoped>
.lot-card {
  margin-bottom: 16px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.spot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 6px;
  margin-top: 12px;
}
.spot-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  color: #fff;
  cursor: default;
}
.spot-btn.available {
  background-color: #4caf50;
}
.spot-btn.occupied {
  background-color: #f44336;
  opacity: 0.8;
}
</style> -->

<!-- <template>
  <div class="spot-grid">
    <button
      v-for="n in lot.number_of_spots"
      :key="`${lot.id}-${n}`"
      class="spot-btn"
      :class="getSpotStatus(lot, n) === 'A' ? 'available' : 'occupied'"
      disabled
    >
      {{ getSpotStatus(lot, n) }}
    </button>
  </div>
</template> -->


<!-- <template>

    <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <p class="mb-3">
              <strong> Parking Lots </strong>
              <span class="text-muted ms-2"> | <router-link class="btn btn-primary" to="/add-lot">+ Add Lot</router-link> </span>
      </p>
      
     
    </div>

    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="lot in parkingLots" :key="lot.id" class="col">
        <div class="card h-100 shadow-sm d-flex flex-column">
          <div class="card-body d-flex flex-column">
            <p class="mb-2">
              <strong>{{ lot.prime_location_name }}</strong>
              <span class="text-muted ms-2"> | {{ lot.address }}</span>
            </p>
            <!-- Edit/Delete buttons -->
           <!-- <div class="my-2">
            <button class="edit-link" @click="editLot(lot.id)">Edit</button>
            <button class="delete-link" @click="deleteLot(lot.id)">Delete</button>
          </div>
            <p><strong>Spots:</strong> {{ lot.occupiedCount }} / {{ lot.number_of_spots }}</p>

            <div class="spot-grid mt-auto">
              <button
                v-for="n in lot.number_of_spots"
                :key="`${lot.id}-${n}`"
                class="spot-btn btn"
                :class="getSpotStatus(lot, n) === 'A' ? 'btn-success' : 'btn-danger'"
                click="reserveSpot(lot, n)"
              >
                {{ getSpotStatus(lot, n) }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div> --> -->
<!-- 
  <div class="lot-card">

    <h3 class="lot-name">{{ lot.prime_location_name }}</h3>
    <p><strong>Address:</strong> {{ lot.address }} (Pin: {{ lot.pin_code }})</p>
    <p><strong>Spots:</strong> {{ lot.number_of_spots }}</p>
    <p><strong>Price:</strong> ₹{{ lot.price }}</p>
    <p class="created"><em>Created: {{ formattedDate }}</em></p>
  </div> -->
<!-- </template> -->

<!-- <script>
export default {
  name: 'ParkingDetail',
  props: {
    lot: {
      type: Object,
      required: true
    }
  },
  methods: {
  getSpotStatus(lot, n) {
    // Example logic: return 'O' if spot taken, else 'A'
    const spot = lot.spots?.find(s => s.spot_number === n);
    return spot?.status === 'O' ? 'O' : 'A';
  }
},
computed: {
    formattedDate() {
      return new Date(this.lot.created_at).toLocaleDateString();
    }
  }
}
</script>

<style scoped>
.lot-card {
  background: #f9f9f9;
  border: 1px solid #ddd;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 4px;
}
.lot-name {
  font-size: 1.2em;
  margin-bottom: 8px;
}
.created {
  color: #555;
  font-size: 0.9em;
}
</style> -->
