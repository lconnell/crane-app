<template>
  <client-only>
    <v-container>
      <h1 class="mb-6">Workorders</h1>
      <div class="workorders-loading-wrapper">
      <!-- Loading spinner overlay -->
      <v-overlay :model-value="loading" class="workorders-overlay" persistent>
        <v-progress-circular indeterminate color="primary" size="64" />
      </v-overlay>
      <v-card class="mb-4 pa-4 workorders-table-card">
        <v-row align="center">
          <v-col cols="12">
            <v-text-field v-model="search" label="Search workorders..." @update:modelValue="fetchWorkorders" clearable class="search-box" />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="statusFilter"
              :items="statusOptions"
              label="Status"
              @update:modelValue="fetchWorkorders"
              clearable
            />
          </v-col>
          <v-col cols="12" md="4" class="text-right">
            <v-btn color="primary" @click="showCreate = true">Create Workorder</v-btn>
          </v-col>
        </v-row>
        <v-data-table
          :headers="headers"
          :items="filteredWorkorders"
          :loading="loading"
          item-key="id"
          class="elevation-1"
          @click:row="onRowClick"
          :no-data-text="loading ? 'Loading...' : 'No workorders found.'"
        >
          <!-- Status column with icon -->
          <template #item.status="{ item }">
            <v-icon v-if="item.status === 'in_progress'" color="primary" title="In Progress">mdi-progress-clock</v-icon>
            <v-icon v-else-if="item.status === 'completed'" color="success" title="Completed">mdi-check-circle</v-icon>
            <v-icon v-else-if="item.status === 'closed'" color="error" title="Closed">mdi-close-circle</v-icon>
            <!-- Explicitly type 'l' as string to satisfy TypeScript -->
<span class="ml-2">{{ item.status.replace('_', ' ').replace(/\b\w/g, (l: string) => l.toUpperCase()) }}</span>
          </template>
          <!-- Updated At column with formatted date -->
          <template #item.updated_at="{ item }">
            <span>{{ formatDate(item.updated_at) }}</span>
          </template>
        </v-data-table>
      </v-card>
      <!-- Error snackbar -->
      <v-snackbar v-model="snackbar" :timeout="4000" color="error" location="bottom">
        {{ errorMessage }}
        <template #actions>
          <v-btn icon @click="snackbar = false"><v-icon>mdi-close</v-icon></v-btn>
        </template>
      </v-snackbar>
      <!-- Edit dialog -->
      <WorkorderDialog
        v-model="showDialog"
        :workorder="selectedWorkorder"
        @saved="async (workorder) => { await saveWorkorder(workorder); }"
        @deleted="async (id) => { await deleteWorkorder(id); }"
      />
      <!-- Create dialog -->
      <WorkorderDialog
        v-model="showCreate"
        :workorder="undefined"
        @saved="async (workorder) => { await saveWorkorder(workorder); }"
      />
    </div>
    </v-container>
  </client-only>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import WorkorderDialog from '~/components/WorkorderDialog.vue';
// @ts-ignore
import { definePageMeta } from '#imports';

// Utilities
function formatDate(date: string | number | Date): string {
  if (!date) return '';
  const d = new Date(date);
  if (isNaN(d.getTime())) return '';
  const pad = (n: number) => n.toString().padStart(2, '0');
  let hours = d.getHours();
  const minutes = pad(d.getMinutes());
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12 || 12;
  return `${pad(d.getMonth() + 1)}/${pad(d.getDate())}/${d.getFullYear()} ${hours}:${minutes} ${ampm}`;
}

// State
const search = ref('');
const statusFilter = ref('');
const statusOptions = ['in_progress', 'closed', 'completed'];
const workorders = ref<any[]>([]);
const filteredWorkorders = computed(() =>
  workorders.value
    .filter((w) => w && typeof w.id !== 'undefined' && w.id !== null)
    .filter((w) => !search.value || w.title.toLowerCase().includes(search.value.toLowerCase()))
    .filter((w) => !statusFilter.value || w.status === statusFilter.value)
);
const loading = ref(false);
const showDialog = ref(false);
const showCreate = ref(false);
const selectedWorkorder = ref<any | null>(null);
const snackbar = ref(false);
const errorMessage = ref('');

// Table headers for Vuetify 3
const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Location', key: 'location' },
  { title: 'Technician', key: 'technician' },
  { title: 'Status', key: 'status' },
  { title: 'Updated', key: 'updated_at' },
];

async function onRowClick(event: MouseEvent, { item }: { item: any }) {
  try {
    let jwt = '';
    if (typeof window !== 'undefined') {
      jwt = localStorage.getItem('jwt') || '';
    }
    if (!jwt) throw new Error('No JWT found');
    const res = await fetch(`http://localhost:8000/api/workorders/${item.id}`, {
      headers: { Authorization: `Bearer ${jwt}` },
    });
    if (!res.ok) throw new Error('Failed to fetch workorder details');
    selectedWorkorder.value = await res.json();
    showDialog.value = true;
  } catch (err) {
    errorMessage.value = 'Failed to load workorder details.';
    snackbar.value = true;
  }
}

// Fetch all workorders (client-only)
async function fetchWorkorders() {
  loading.value = true;
  try {
    let jwt = '';
    if (typeof window !== 'undefined') {
      jwt = localStorage.getItem('jwt') || '';
    }
    if (!jwt) throw new Error('No JWT found');
    const res = await fetch('http://localhost:8000/api/workorders', {
      headers: { Authorization: `Bearer ${jwt}` },
    });
    if (!res.ok) throw new Error('Failed to fetch workorders');
    const data = await res.json();
    const filtered = Array.isArray(data) ? data.filter((w) => w && typeof w.id !== 'undefined' && w.id !== null) : [];
    workorders.value = filtered;
    if (filtered.length === 0) {
      errorMessage.value = 'No workorders could be loaded from the backend.';
      snackbar.value = true;
    }
  } catch (err) {
    console.error('Failed to fetch workorders', err);
    workorders.value = [];
  } finally {
    loading.value = false;
  }
}

// Create or update a workorder
async function saveWorkorder(workorder: any) {
  try {
    const jwt = localStorage.getItem('jwt');
    let url = 'http://localhost:8000/api/workorders';
    let method = 'POST';
    // If editing (has id), use PUT
    if (workorder.id) {
      url += `/${workorder.id}`;
      method = 'PUT';
    }
    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${jwt}`,
      },
      body: JSON.stringify(workorder),
    });
    if (!res.ok) throw new Error(method === 'PUT' ? 'Failed to update workorder' : 'Failed to create workorder');
    await fetchWorkorders();
  } catch (err) {
    console.error('Failed to save workorder', err);
  }
}

// Delete a workorder by ID
async function deleteWorkorder(id: number) {
  try {
    const jwt = localStorage.getItem('jwt');
    const res = await fetch(`http://localhost:8000/api/workorders/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${jwt}` },
    });
    if (!res.ok) throw new Error('Failed to delete workorder');
    await fetchWorkorders();
  } catch (err) {
    console.error('Failed to delete workorder', err);
  }
}

// Only fetch workorders on client to avoid SSR mismatch
// Fetch workorders when the page is mounted (client-only, due to <client-only> wrapper)
fetchWorkorders();

</script>

<style scoped>
.text-right {
  text-align: right;
}
.workorders-table-card {
  width: 90vw;
  max-width: 1600px;
  margin-left: auto;
  margin-right: auto;
}
.workorders-loading-wrapper {
  position: relative;
}
.workorders-overlay {
  z-index: 10;
}
.search-box {
  width: 100%;
}
</style>
