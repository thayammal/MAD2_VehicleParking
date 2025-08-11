<template>
  <div class="test-view">
    <h1>Test View</h1>
    <p>This is a test view for demonstration purposes.</p>
    <input type="text" name="testInput" placeholder="Type something here..." v-model="this.name" />
    <button type="button" @click="this.get_call()"> Click Me</button>
    {{this.name}}
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'TestPage',
  data() {
    return {
      name: ''
    };
  },
  methods: {
    printName() {
      console.log('name var - ', this.name);
    },
    get_call(){
        axios
            .post('http://localhost:5000/',
                {
                    name: this.name,
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            )
            .then(response => {
                console.log('Response from backend:', response.data);
                console.log('Response status', response.status);
                this.name = response.data.message; // Assuming the backend returns a message
                // #console.log('Name updated:', this.name);

            })
            .catch(error => {
                console.error('Error fetching data from backend:', error);
            });
    }
 },
};

</script>

<style>

</style>