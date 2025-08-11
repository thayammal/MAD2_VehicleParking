<!-- <template>
  <div class="user-info" v-if="user">
    <h3>User Details</h3>
<table class="user-table">
  <thead>
    <tr>
      <th>User ID</th>
      <th>Username</th>
      <th>Email</th>
      <th>Address</th>
      <th>Phone Number</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{{ user.user_id }}</td>
      <td>{{ user.username }}</td>
      <td>{{ user.email }}</td>
      <td>{{ user.address || 'N/A' }}</td>
      <td>{{ user.phone_number || 'N/A' }}</td>
    </tr>
  </tbody>
</table>

<h3>Reservation Details</h3>
<table v-if="reservations.length > 0" class="reservation-table">
  <thead>
    <tr>
      <th>Lot Name</th>
      <th>Lot Type</th>
      <th>Spot ID</th>
      <th>Parking Time</th>
      <th>Leaving Time</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(res, i) in reservations" :key="i">
      <td>{{ res.prime_location_name }}</td>
      <td>{{ res.lot_id }}</td>
      <td>{{ res.spot_id }}</td>
      <td>{{ res.parking_timestamp }}</td>
      <td>{{ res.leaving_timestamp }}</td>
    </tr>
  </tbody>
</table>

    <p v-else>No reservations found.</p>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true
    },
    reservations: {
      type: Array,
      required: true
    }
  },
  methods: {
    formatDate(datetimeStr) {
      if (!datetimeStr) return 'N/A';
      const date = new Date(datetimeStr);
      return date.toLocaleString();  // e.g., 17/07/2025, 4:30:00 PM
    }
  }
}
</script>

<style scoped>
.user-info {
  border: 2px solid #4CAF50;
  border-radius: 10px;
  padding: 16px;
  margin-top: 16px;
  background-color: #f9f9f9;
}

h3 {
  margin-top: 20px;
  color: #2c3e50;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #4CAF50;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}
</style> -->
<template>
  <div class="user-info" v-if="user">
    <h3>User Details</h3>
    <table class="user-table">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Address</th>
          <th>Phone Number</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ user.user_id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.address || 'N/A' }}</td>
          <td>{{ user.phone_number || 'N/A' }}</td>
        </tr>
      </tbody>
    </table>

    <h3>Reservation Details</h3>
    <table v-if="reservations.length > 0" class="reservation-table">
      <thead>
        <tr>
          <th>Lot Name</th>
          <th>Lot ID</th>
          <th>Spot ID</th>
          <th>Parking Time</th>
          <th>Leaving Time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(res, i) in reservations" :key="i">
          <td>{{ res.lot_name || 'N/A' }}</td>
          <td>{{ res.lot_id }}</td>
          <td>{{ res.spot_id }}</td>
          <td>{{ formatDate(res.parking_time) }}</td>
          <td>{{ formatDate(res.leaving_time) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No reservations found.</p>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true
    },
    reservations: {
      type: Array,
      required: true
    }
  },
  methods: {
    formatDate(datetimeStr) {
      if (!datetimeStr) return 'N/A';
      const date = new Date(datetimeStr);
      return date.toLocaleString();  // Format: 17/07/2025, 4:30:00 PM
    }
  }
}
</script>

<style scoped>
.user-info {
  border: 2px solid #4CAF50;
  border-radius: 10px;
  padding: 16px;
  margin-top: 16px;
  background-color: #f9f9f9;
}

h3 {
  margin-top: 20px;
  color: #2c3e50;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #4CAF50;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}
</style>
