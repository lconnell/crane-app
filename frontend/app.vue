<template>
  <v-app>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </v-app>
</template>

<script setup lang="ts">
// This ensures Vuetify context (including icons) is available everywhere
import "@/assets/vuetify-overrides.css";
</script>
