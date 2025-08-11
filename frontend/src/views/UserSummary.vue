<template>
  <div>
    <nav class="navbar mb-4">
      <router-link to="/user-dashboard">Home</router-link> |
      <router-link to="/user-summary">Summary</router-link> |
      <router-link to="/">Logout</router-link>
      <br>
      
      <router-link to="/edituser">Edit Profile</router-link>
    </nav>
    <router-view/>
    <h2> Welcome {{ this.username }}</h2>
    <h2>User Parking Summary</h2>
    <div class="chart-row">
      <canvas id="barChart" class="chart-canvas"></canvas>
      <canvas id="pieChart" class="chart-canvas"></canvas>
    </div>
  </div>
</template>
<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'UserSummary',
  data() {
    return {
      user_id: '',
      username:'',
    };
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    this.user_id = user.user_id;
    this.username = user.username;
    this.fetchUserSummary();
  },
  methods: {
    async fetchUserSummary() {
      const token = localStorage.getItem("auth_token");

      try {
        const res = await fetch(`http://localhost:5000/api/user-summary`, {
          headers: {
            'Authorization': token
          }
        });

        const data = await res.json();

        // Prepare for Bar chart: Location vs Total Cost
        const barLabels = data.cost_by_location.map(item => item.location);
        const barData = data.cost_by_location.map(item => item.total_cost);

        // Prepare for Pie chart: Location vs No. of Reservations
        const pieLabels = data.reservation_by_location.map(item => item.location);
        const pieData = data.reservation_by_location.map(item => item.count);

        this.renderBarChart(barLabels, barData);
        this.renderPieChart(pieLabels, pieData);

      } catch (error) {
        console.error('Error fetching summary:', error);
      }
    },
renderBarChart(labels, data) {
  const ctx = document.getElementById('barChart');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total Parking Cost (₹)',
        data: data,
        backgroundColor: '#42a5f5'
      }]
    },
    options: {
      responsive: false,  // disable responsiveness
      maintainAspectRatio: false,
      width: 400,
      height: 200,
      plugins: {
        title: {
          display: true,
          text: 'Parking Cost by Prime Location'
        }
      }
    }
  });
},

renderPieChart(labels, data) {
  const ctx = document.getElementById('pieChart');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Reservations',
        data: data,
        backgroundColor: ['#66bb6a', '#ef5350', '#ffa726', '#ab47bc', '#26c6da']
      }]
    },
    options: {
      responsive: false,  // disable responsiveness
      maintainAspectRatio: false,
      width: 300,
      height: 300,
      plugins: {
        title: {
          display: true,
          text: 'Reservation Count by Prime Location'
        }
      }
    }
  });
},

   }
};
</script>
<style scoped>
.chart-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  margin-top: 20px;
  flex-wrap: wrap; /* Allows stacking on small screens */
}

.chart-canvas {
  width: 400px !important;
  height: 300px !important;
}
</style>
