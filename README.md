# WriteDarker
Projekt um Paper mit LLM zu schreiben

## Projektidee

Die Idee ist, eine Web App zu programmieren, mit der man gemeinsam an einem wissenschaftlichen Paper schreiben kann. Dafür werden folgende Komponenten benötigt:

1. **Web UI**  
   Die Benutzeroberfläche soll als Webanwendung umgesetzt werden, idealerweise mit [Quasar Framework](https://quasar.dev/) (Vue.js-basiert). Sie ermöglicht das Schreiben, Bearbeiten und Verwalten von Paper-Inhalten.

2. **Datenbank**  
   Eine relationale Datenbank, vorzugsweise [PostgreSQL](https://www.postgresql.org/), verwaltet Literaturquellen, Projekte und die eigenen Texte. Sie dient als zentrales Speichersystem für alle relevanten Daten.  Zunächst aber Implementation von SQLlite.

3. **Backend**  
   Das Backend wird idealerweise in Python entwickelt. Es übernimmt die Kommunikation zwischen der Web UI, der Datenbank und der OpenAI ChatGPT API. So können Texte generiert, gespeichert und abgerufen werden.

## Kernfunktionen

- **Literaturdatenbank:**  
  Verwaltung und Pflege von Literaturquellen, die für das Paper genutzt werden können.

- **Paper schreiben im Markdown-Format:**  
  Erstellung und Bearbeitung wissenschaftlicher Paper im Markdown-Format, inklusive der Möglichkeit, Literaturquellen direkt einzupflegen.

- **Struktur eines wissenschaftlichen Papers:**  
  Unterstützung der typischen Struktur mit folgenden Abschnitten:
  - Titel
  - Abstract
  - Einleitung
  - Methodenteil
  - Ergebnisse
  - Diskussion
  - Zusammenfassung



- **KI-Funktionen für einzelne Abschnitte:**  
  Für jeden Abschnitt stehen KI-gestützte Funktionen wie AutoText, Chat und weitere Schreibunterstützungen zur Verfügung.

<!-- Weitere Funktionen können hier ergänzt werden -->
WriteDarker/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI-Anwendung
│   │   ├── crud.py         # CRUD-Operationen für DB
│   │   ├── models.py       # SQLAlchemy-Modelle
│   │   ├── schemas.py      # Pydantic-Schemas
│   │   └── ai.py           # Endpunkte für KI (z.B. mcP-Protokoll)
│   ├── database.db         # SQLite-Datenbank (wird automatisch erstellt)
│   └── requirements.txt    # Python-Abhängigkeiten
│
├── frontend/
│   └── ...                 # Quasar/Vue.js-Projekt
│
├── README.md
└── .gitignore


## Backend

from fastapi import FastAPI
from . import crud, ai, models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(crud.router, prefix="/db", tags=["database"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])

