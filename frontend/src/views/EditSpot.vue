<!-- <template>
  <div class="container mt-4">
    <h2>Edit/Delete Parking Spot</h2>

    <div v-if="spot">
      <p><strong>Spot ID:</strong> {{ spot.id }}</p>
      <p><strong>Status:</strong> {{ spot.status === 'A' ? 'Available' : 'Occupied' }}</p>

      <button
        class="btn btn-danger me-2"
        :disabled="spot.status !== 'A'"
        @click="deleteSpot"
      >
        Delete
      </button>

      <button class="btn btn-secondary" @click="goBack">Close</button>
    </div>
    <div v-else>
      <p>Loading spot details...</p>
    </div>
  </div>
</template> -->
<template>
  <div class="container mt-4">
    <h2>Edit/Delete Parking Spot</h2>
    <div v-if="spot">
      <p><strong>Spot ID:</strong> {{ spot.id }}</p>
      <p>
        <strong>Status:</strong>
        {{ spot.status === 'A' ? 'Available' : 'Occupied' }}
      </p>

      <button
        v-if="spot.status === 'A'"
        class="btn btn-danger me-2"
        @click="deleteSpot"
      >Delete</button>

      <button
        v-else
        class="btn btn-primary me-2"
        @click="showOccupiedDetails"
      >Show Usage Details</button>

      <button class="btn btn-secondary" @click="goBack">Close</button>
    </div>
    <div v-else>
      <p>Loading spot details...</p>
    </div>
  </div>
</template>
<script>
export default {
  name: "EditSpot",
  data() {
    return { spot: null };
  },
  async created() {
    const { lotId, spotNum } = this.$route.params;
    const token = localStorage.getItem("auth_token");
    const res = await fetch(`/api/parkingspot/${lotId}/${spotNum}/details`, {
      headers: { Authorization: token }
    });
    const json = await res.json();
    if (res.ok && json.status === 'ok') {
      this.spot = json.spot;
    } else {
      alert(json.message || 'Spot not found');
      this.$router.go(-1);
    }
  },
  methods: {
    async deleteSpot() {
      if (this.spot.status !== "A") {
        alert("Only available spots can be deleted."); return;
      }
      if (!confirm("Are you sure you want to delete this spot?")) return;
      const token = localStorage.getItem("auth_token");
      const res = await fetch(`/api/parkingspot`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json", Authorization: token },
        body: JSON.stringify({ id: this.spot.id }),
      });
      const data = await res.json();
      if (res.ok && data.status === "ok") {
        alert("Spot deleted successfully");
        this.$router.push("/admin-dashboard");
      } else {
        alert(data.message || "Failed to delete spot");
      }
    },
    showOccupiedDetails() {
      alert(
        `User: ${this.spot.username}\n` +
        `Vehicle: ${this.spot.vehicle_number}\n` +
        `In: ${this.spot.parking_timestamp}\n` +
        `Out: ${this.spot.leaving_timestamp || 'N/A'}\n` +
        `Estimated Cost: $${this.spot.estimated_cost}`
      );
    },
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>