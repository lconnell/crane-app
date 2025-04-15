<template>
  <v-container>
    <h1 class="mb-6">Inventory</h1>
    <v-card class="mb-4 pa-4">
      <v-row align="center">
        <v-col cols="12" md="6">
          <v-text-field v-model="search" label="Search parts..." @update:modelValue="fetchParts" clearable />
        </v-col>
        <v-col cols="12" md="6" class="text-right">
          <v-btn color="primary" @click="showCreate = true">Add Part</v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-data-table
      :headers="headers"
      :items="parts"
      :loading="loading"
      item-key="id"
      class="elevation-1"
      @click:row="onRowClick"
      :no-data-text="loading ? 'Loading...' : 'No parts found.'"
    />
    <PartDialog
      v-model="showDialog"
      :part="selectedPart"
      @saved="fetchParts"
      @deleted="fetchParts"
    />
    <PartDialog
      v-model="showCreate"
      :part="null"
      @saved="fetchParts"
    />
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import PartDialog from '~/components/PartDialog.vue';

// State variables
const search = ref('');
const parts = ref<any[]>([]);
const loading = ref(false);
const showDialog = ref(false);
const showCreate = ref(false);
const selectedPart = ref<any | null>(null);

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Name', key: 'name' },
  { title: 'Stock', key: 'stock' },
  { title: 'Last Used', key: 'last_used' },
];

function onRowClick({ item }: { item: any }) {
  selectedPart.value = item;
  showDialog.value = true;
}

async function fetchParts() {
  loading.value = true;
  // TODO: Fetch from backend
  // Example error handling
  try {
    // Simulate fetch
    // parts.value = await fetchPartsFromAPI(search.value);
  } catch (err) {
    // Handle error (show notification, etc.)
  } finally {
    loading.value = false;
  }
}

onMounted(fetchParts);

// Nuxt 3 page meta for auth protection
definePageMeta({
  middleware: 'auth',
});
</script>

<style scoped>
.text-right {
  text-align: right;
}
</style>
