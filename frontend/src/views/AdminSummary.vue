<template>
  <div>
    <nav class="navbar mb-4">
      <router-link to="/admin-dashboard">Home</router-link> |
      <router-link to="/user-stat">Users</router-link> |
      <router-link to="/admin-summary">Summary</router-link> |
      <router-link to="/">Logout</router-link>
    </nav>

    <h2 class="text-center mb-4">Admin Summary</h2>
    <div class="charts-container">
      <div class="chart-box">
        <h4 class="text-center">Parking Cost by Location</h4>
        <canvas id="barChart"></canvas>
      </div>

      <div class="chart-box">
        <h4 class="text-center">Spot Availability</h4>
        <canvas id="pieChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

Chart.register(...registerables, ChartDataLabels);

export default {
  name: 'adminsummary',
  data() {
    return {
      barChart: null,
      pieChart: null
    };
  },
  mounted() {
    this.fetchCostSummary();
    this.fetchSpotSummary();
  },
  methods: {
    async fetchCostSummary() {
      const token = localStorage.getItem("auth_token");

      try {
        const res = await fetch(`http://localhost:5000/admin/cost-summary`, {
          headers: {
            'Authorization': token
          }
        });
        const data = await res.json();

        if (Array.isArray(data)) {
          const labels = data.map(item => item.location);
          const values = data.map(item => item.total_cost);
          this.renderBarChart(labels, values);
        }

      } catch (error) {
        console.error('Error fetching cost summary:', error);
      }
    },

    async fetchSpotSummary() {
      const token = localStorage.getItem("auth_token");

      try {
        const res = await fetch(`http://localhost:5000/admin/spot-summary`, {
          headers: {
            'Authorization': token
          }
        });
        const data = await res.json();

        if (Array.isArray(data)) {
          const labels = data.map(item => item.location);
          const available = data.map(item => item.available);
          const occupied = data.map(item => item.occupied);

          const chartData = {
            labels: labels.flatMap(loc => [`${loc} (A)`, `${loc} (O)`]),
            values: labels.flatMap((_, i) => [available[i], occupied[i]])
          };

          this.renderPieChart(chartData.labels, chartData.values);
        }

      } catch (error) {
        console.error('Error fetching spot summary:', error);
      }
    },

    renderBarChart(labels, data) {
      const ctx = document.getElementById('barChart');

      if (this.barChart) this.barChart.destroy();

      this.barChart = new Chart(ctx, {
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
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Parking Cost by Location'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },

    renderPieChart(labels, data) {
      const ctx = document.getElementById('pieChart');

      if (this.pieChart) this.pieChart.destroy();

      this.pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: 'Spot Summary',
            data: data,
            backgroundColor: [
              '#66bb6a', '#ef5350',
              '#29b6f6', '#ffca28',
              '#ab47bc', '#ffa726',
              '#26c6da', '#8d6e63'
            ]
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Available vs Occupied Spots by Location'
            },
            datalabels: {
              color: '#fff',
              formatter: (value, ctx) => value,
              font: {
                weight: 'bold'
              }
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.charts-container {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.chart-box {
  width: 100%;
  max-width: 600px;
  padding: 10px;
}

canvas {
  width: 100% !important;
  height: 400px !important;
}
</style>
