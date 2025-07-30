You assist me writting a Tool for writting scientific papers using open ai's api.

We have a backend in `/backend` that manages communication with a sqlite db stored in `./AppData/writedarker.db` and the openai api. The backend is written in python and started by calling `npm run start:backend` in the root dir.

The frontend `/frontend` is written in quasar dev / vuejs / vite / tailwindcss. We have a login logic and a dashpage. From the Dashpage we can add references and edit / view projects. The frontend ist started by `npm run dev` in the frontend dir.

To initialise the project we run `npm run setup` at the beginning.

The DB is a sqlite db:
