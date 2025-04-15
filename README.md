# Crane App – Rental & Repair Shop Management

Welcome to the Crane App! This is a modern, full-stack web application designed to manage workorders and inventory for a crane rental and repair shop.

---

## Project Overview

- **Frontend**: Built with [Nuxt 3](https://nuxt.com/) (Vue 3) and [Vuetify](https://vuetifyjs.com/) for a fast, responsive, and user-friendly interface.
- **Backend**: Powered by [FastAPI](https://fastapi.tiangolo.com/) with [SQLite](https://www.sqlite.org/) for rapid development and easy deployment.
- **Authentication**: Secure JWT-based login and route protection.

---

## Repository Structure

```
crane-app-vue/
├── backend/    # FastAPI backend (API, DB, auth)
│   └── README.md
├── frontend/   # Nuxt 3 + Vuetify frontend (UI)
│   └── README.md
├── README.md   # <--- You are here (project overview)
```

- **`frontend/`**: All Vue/Nuxt app code, UI components, pages, and assets. See [frontend/README.md](./frontend/README.md) for setup and usage.
- **`backend/`**: All FastAPI code, database, and API logic. See [backend/README.md](./backend/README.md) for setup and usage.

---

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lconnell/crane-app.git
   cd crane-app-vue
   ```
2. **Follow setup instructions for each part:**
   - [Frontend setup](./frontend/README.md)
   - [Backend setup](./backend/README.md)

---

## Key Features
- Manage workorders: create, edit, assign technicians, track status
- Inventory management: add, update, delete parts
- Secure authentication and protected routes
- Modern, responsive UI

---

## Suggestions for Newcomers
- **Start with the README in each subfolder** for detailed setup and usage.
- To develop locally, run both the backend and frontend servers (see their READMEs).
- If you encounter issues, check for missing dependencies or port conflicts.
- Review the code comments for guidance on structure and logic.
- Contributions and questions are welcome!

---

For further questions or to report issues, please open an issue on the repository or contact the maintainer.

