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

The directories present here are mostly placeholders:

```
backend/   # FastAPI skeleton (no real API yet)
frontend/  # Quasar/Vue.js placeholder
```

Additional modules such as CRUD operations and AI endpoints are stubs only. The detailed
structure described below is still planned and not implemented.

## Running the Backend (planned)

Once the backend is implemented you will be able to:

1. Create a Python environment with `python -m venv venv` and activate it.
2. Install dependencies, e.g. `pip install fastapi uvicorn`.
3. Start the application with `uvicorn backend.main:app --reload`.

These instructions are provisional until a full `requirements.txt` is added.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to set up branches, follow coding standards, and track issues.

## License

This project is released under the [MIT License](LICENSE).
