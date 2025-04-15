<template>
  <v-container class="fill-height d-flex flex-column justify-center align-center text-center">
    <v-row>
      <v-col>
        <h1 class="display-2 font-weight-bold mb-4">Crane Shop Management</h1>
        <p class="subtitle-1 mb-6">Manage workorders and inventory for your crane rental and repair shop with ease.</p>
        <v-btn color="primary" class="mr-4" to="/workorders">Go to Workorders</v-btn>
        <v-btn color="secondary" to="/inventory">Go to Inventory</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
// Home page - simple navigation
</script>

<style scoped>
.fill-height {
  min-height: 80vh;
}
</style>
