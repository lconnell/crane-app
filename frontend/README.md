# Crane App Frontend

This is the frontend for the Crane Shop Management application, built with **Nuxt 3**, **Vue 3**, and **Vuetify**.

## Features
- Workorder management (create, edit, delete, list)
- Inventory management
- JWT-based authentication (with FastAPI backend)
- Responsive UI with Vuetify

## Project Structure
- `components/` – Vue components (dialogs, forms, etc.)
- `pages/` – Nuxt pages (workorders, inventory, login)
- `middleware/` – Global route guards (auth)
- `plugins/` – Vuetify plugin setup
- `types/` – TypeScript type declarations

## Getting Started

### Prerequisites
- Node.js v18+
- npm v9+

### Install dependencies
```bash
cd frontend
npm install
```

### Run the development server
```bash
npm run dev
```

The app will be available at [http://localhost:8888](http://localhost:8888).

### Environment
- Expects backend API at `http://localhost:8000` (see backend README)

## Authentication
- JWT tokens are stored in localStorage after login.
- All protected routes use a global auth middleware (`middleware/auth.global.ts`).

## Linting & Formatting
- TypeScript strict mode
- ESLint and Prettier recommended for code quality

## Notes
- If you see TypeScript errors about auto-imports, ensure `types/nuxt.d.ts` exists.
- For UI customization, edit `assets/vuetify-overrides.css`.

---
For more details, see the root README or the backend README.


This is a modern, intuitive frontend application for managing crane rental and repair shop inventory and workorders.

## Tech Stack
- **Nuxt 3** (Vue 3 framework)
- **Vuetify** (UI component library)
- **JWT Authentication** (to be integrated with FastAPI backend)

## Features
- Workorder management: create, update, delete, search, assign technician, track status, add notes
- Inventory management: create, update, delete, search, view part history
- Authentication: sign-in with JWT

## Project Structure
- `/pages` – Main app pages (Workorders, Inventory, Login)
- `/components` – Reusable Vue components
- `/layouts` – App layout and navigation

## Getting Started
1. Install dependencies:
   ```bash
   npm install
   ```
2. Run the development server:
   ```bash
   npm run dev
   ```
3. Open [http://localhost:8888](http://localhost:8888)

---

This app is the frontend for a fullstack system. Backend (FastAPI + PostgreSQL) is in a separate repository.


```bash
npm install
npm install -D @types/node
npm audit fix --force
```
