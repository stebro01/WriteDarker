# WriteDarker

WriteDarker is an early-stage experiment to build a collaborative writing environment.
Currently this repository only contains planning notes and a minimal project skeleton.

## Vision

The goal is to create a web application that feels like a lightweight Google Docs alternative. Users will be able to:

- write papers in clearly separated sections (title, abstract, introduction, etc.)
- request iterative AI suggestions for each section to refine the text
- manage projects and authenticate across sessions
- store references in a literature database

## Repository Layout

The backend is organised into dedicated packages:

```
backend/api        # FastAPI routers
backend/services   # business logic
backend/models     # SQLAlchemy models
```

Basic authentication, document handling and project CRUD endpoints are
implemented together with example tests.

## Setup and Running the Backend

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:

   ```bash
   uvicorn backend.main:app --reload
   ```

## Environment Variables

Configuration values can be supplied via environment variables or a `.env` file
at the repository root. Important variables include:

```bash
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
DB_DIR=./AppData
SECRET_KEY=supersecretkey
OPENAI_TOKEN=your-openai-token
DOC_HISTORY_LIMIT=20
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:5173
```

`SECRET_KEY` is used to sign authentication tokens. The database file is stored
inside the folder specified by `DB_DIR`. `ACCESS_TOKEN_EXPIRE_MINUTES` controls
how long generated tokens remain valid. `ALLOWED_ORIGINS` configures which
origins can make cross-origin requests to the API (comma-separated list). The
`OPENAI_TOKEN` and `DOC_HISTORY_LIMIT` values are reserved for future features.

## AI MCP Endpoint

A minimal AI endpoint exists at `POST /ai/mcp`. It accepts JSON with a `prompt`
field and responds with a mocked Master Control Program style message. The
response is generated locally for now. Future releases may use
`OPENAI_TOKEN` to proxy prompts to an actual AI service.

## Development Setup

To install all JavaScript and Python dependencies and run both the
backend and frontend together:

1. Install root npm packages and create the virtual environment:

   ```bash
   npm install
   npm run setup
   ```

2. Start the development servers (backend API and React app):

   ```bash
   npm run start
   ```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to set up branches, follow coding standards, and track issues.

## License

This project is released under the [MIT License](LICENSE).
