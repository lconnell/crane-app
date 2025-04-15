<template>
  <v-app>
    <v-app-bar color="primary" dark app>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>Crane Shop Management</v-toolbar-title>
      <v-spacer />
      <v-spacer />
      <v-btn v-if="isAuthenticated" @click="logout" text class="logout-link" title="Sign Out">
        Logout
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item to="/workorders" title="Workorders" prepend-icon="mdi-clipboard-list-outline" />
        <v-list-item to="/inventory" title="Inventory" prepend-icon="mdi-warehouse" />
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <slot />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from '#app';

const drawer = ref(false);
const router = useRouter();

// Use ref and onMounted to avoid SSR hydration mismatch
const isAuthenticated = ref(false);

onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('jwt');
});

function logout() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('jwt');
    isAuthenticated.value = false;
  }
  router.push('/login');
}

</script>

<style scoped>
.v-main {
  background: #f5f5f7;
  min-height: 100vh;
}
</style>
