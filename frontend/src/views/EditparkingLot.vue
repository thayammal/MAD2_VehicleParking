<template>
  <div class="container mt-4">
    <h2>Edit Parking Lot</h2>

    <form @submit.prevent="updateLot" class="mt-4">
      <div class="mb-3">
        <label class="form-label">Location Name : </label>
        <input type="text" class="form-control" :value="lot.prime_location_name" disabled> <br> <br>
      </div>
      <div class="mb-3">
        <label class="form-label"> Address : </label>
        <textarea class="form-control" rows="2" :value="lot.address" disabled></textarea>  <br> <br>
      </div>
      <div class="mb-3">
        <label class="form-label">Price : </label>   
        <input
          type="number"
          class="form-control"
          v-model.number="form.price"
          required
        >
      </div>  <br> <br>
      <div class="mb-3">
        <label class="form-label">Number of Spots : </label>
        <input
          type="number"
          class="form-control"
          v-model.number="form.number_of_spots"
          required
          min="1"
        >
      </div>   <br> <br>
      <button type="submit" class="btn btn-success"> Save Changes </button>  
      <router-link to="/admin-dashboard" class="btn btn-secondary ms-2"> Cancel </router-link>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lot: {
        prime_location_name: '',
        address: '',
        price: 0,
        number_of_spots: 0
      },
      form: {
        price: 0,
        number_of_spots: 0
      },
      lotId: null
    };
  },
  async created() {
    this.lotId = this.$route.params.id;
    await this.loadLot();
  },
  methods: {
    async loadLot() {
      try {
        const res = await fetch('http://localhost:5000/api/parkinglot');
        const data = await res.json();
        const found = Array.isArray(data.lots)
          ? data.lots.find(item => item.id === +this.lotId)
          : null;
        if (!found) throw new Error('Lot not found');
        this.lot = found;
        this.form.price = found.price;
        this.form.number_of_spots = found.number_of_spots;
      } catch (e) {
        alert(e.message);
        this.$router.push('/admin-dashboard');
      }
    },
    async updateLot() {
      try {
        const res = await fetch('http://localhost:5000/api/parkinglot', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: this.lotId,
            price: this.form.price,
            number_of_spots: this.form.number_of_spots
          })
        });
        const json = await res.json();
        if (json.status === 'ok') {
          alert('Lot updated successfully');
          this.$router.push('/admin-dashboard');
        } else {
          alert(`Update failed: ${json.message}`);
        }
      } catch (e) {
        console.error(e);
        alert('Network or server error');
      }
    }
  }
};
</script>

<style scoped>
.container { max-width: 600px; }
</style>
