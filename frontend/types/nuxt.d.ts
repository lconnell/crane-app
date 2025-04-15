// Type declaration for Nuxt 3 auto-imported composables and modules
// Fixes: Cannot find module '#app' or its corresponding type declarations

declare module '#app';

declare module '#imports' {
  const composables: any;
  export = composables;
}
