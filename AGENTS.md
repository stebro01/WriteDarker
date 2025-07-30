You assist me writting a Tool for writting scientific papers using open ai's api.

We have a backend in `/backend` that manages communication with a sqlite db stored in `./AppData/writedarker.db` and the openai api. The backend is written in python and started by calling `npm run start:backend` in the root dir.

The frontend `/frontend` is written in quasar dev / vuejs / vite / tailwindcss. We have a login logic and a dashpage. From the Dashpage we can add references and edit / view projects. The frontend ist started by `npm run dev` in the frontend dir.

To initialise the project we run `npm run setup` at the beginning.

The DB is a sqlite db.

## Backend structure
- `backend/main.py` starts the FastAPI app and loads routers.
- `backend/api/` holds routers: `users.py`, `documents.py`, `projects.py`, `references.py`, `settings.py`, `ai.py` and a simple `crud.py` helper.
- `backend/models/` defines SQLAlchemy models for all tables.
- `backend/services/` contains helper modules for authentication and reference fetching.
- `backend/db.py` configures the SQLAlchemy engine pointing to `./AppData/writedarker.db` (overridable via `DB_DIR`).

## Frontend structure
- Built with Quasar (Vue 3) using Vite and TailwindCSS.
- `frontend/src/pages/` contains `AuthPage.vue`, `DashboardPage.vue`, `ProjectPage.vue`, etc.
- `frontend/src/router/` defines route guards (`auth-guard.js`) and app routes.
- `frontend/src/stores/` uses Pinia for user auth and API access.
- Common UI components live under `frontend/src/components`.

## Database tables
- **users** – user account information (`id`, `username`, `password_hash`, `first_name`, `last_name`, `age`, `email`).
- **documents** – uploaded or generated texts (`id`, `text`, `pdf`, `image`, `label`, `description`, `creator_id`, `project_id`, `notes`, `position`).
- **projects** – group of documents (`id`, `label`, `description`, `author_id`, `coauthors`).
- **references** – bibliographic references linked to projects (`id`, `title`, `authors`, `journal`, `year`, `pdf`, `project_id`).
- **settings** – configuration values (`id`, `key`, `value`, `user_id`).
- **document_revisions** – history of document text (`id`, `document_id`, `text`, `created_at`).
