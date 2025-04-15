import { defineNuxtRouteMiddleware, navigateTo } from '#imports';

// Simple global auth middleware for Nuxt 3
// Checks for a JWT token in localStorage to determine if user is authenticated
// Adjust logic for your actual authentication method (e.g., cookies, session, etc.)
export default defineNuxtRouteMiddleware((to, from) => {
  // Only run on client side
  const token = process.client ? localStorage.getItem('jwt') : null;

  if (!token && to.path !== '/login') {
    // If not authenticated and not already on login page, redirect to login
    return navigateTo('/login');
  }
  if (token && to.path === '/login') {
    // If authenticated and trying to access login, redirect to workorders
    return navigateTo('/workorders');
  }
});
