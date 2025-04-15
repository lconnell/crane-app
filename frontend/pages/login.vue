<template>
  <v-container class="fill-height d-flex flex-column justify-center align-center">
    <v-card class="pa-6 login-card" max-width="500">
      <h2 class="mb-4">Sign In</h2>
      <v-form @submit.prevent="onLogin">
        <v-text-field v-model="username" label="Username" type="text" required />
        <v-text-field v-model="password" label="Password" type="password" required />
        <v-btn :loading="loading" type="submit" color="primary" class="mt-4" block>Sign In</v-btn>
      </v-form>
      <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
      <v-alert v-if="success" type="success" class="mt-4">Login successful! Redirecting...</v-alert>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
// Import useRouter from Nuxt 3
import { useRouter } from '#app';

const username = ref('');
const password = ref('');
const error = ref('');
const success = ref(false);
const loading = ref(false);
const router = useRouter();

// Handles login by sending credentials to FastAPI and storing JWT on success
async function onLogin() {
  loading.value = true;
  error.value = '';
  try {
    // FastAPI expects application/x-www-form-urlencoded with 'username' and 'password'
    const body = new URLSearchParams();
    body.append('username', username.value);
    body.append('password', password.value);
    console.log('Attempting login with:', username.value);
    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });
    console.log('Login response status:', response.status);
    if (!response.ok) {
      throw new Error('Invalid username or password');
    }
    const data = await response.json();
    console.log('Login success, response data:', data);
    // Store JWT in localStorage
    localStorage.setItem('jwt', data.access_token);
    success.value = true;
    // Wait 1 second before redirect for UX
    setTimeout(() => {
      router.push('/workorders');
    }, 1000);
  } catch (e: any) {
    error.value = e?.message || 'Login failed';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-card {
  width: 100%;
  max-width: 500px;
}
</style>
