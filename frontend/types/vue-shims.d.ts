// TypeScript shim for importing .vue files
// Fixes: Cannot find module '~/components/WorkorderDialog.vue' or its corresponding type declarations

declare module '*.vue' {
  import { DefineComponent } from 'vue';
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
