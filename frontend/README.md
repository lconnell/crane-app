# Crane Rental & Repair Shop Management System

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
