<template>
  <Bar :chart-data="chartData" :chart-options="chartOptions" />
</template>

<script>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  props: {
    chartData: { type: Object, required: true },
    chartOptions: { type: Object, default: () => ({ responsive: true }) }
  }
}
</script>
