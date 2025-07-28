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

3. (Optional) Start a local PostgreSQL instance with Docker Compose:

   ```bash
   docker-compose up -d
   ```

4. Run the application:

   ```bash
   uvicorn backend.main:app --reload
   ```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to set up branches, follow coding standards, and track issues.

## License

This project is released under the [MIT License](LICENSE).
