# Nestio 🏠

A full stack property listings map application built with FastAPI, PostgreSQL, React, TypeScript, and MapLibre GL JS.

Built as a portfolio project to demonstrate proficiency in modern backend and frontend engineering patterns, testing, and DevOps practices.

## Author

**Brice Mehelo** — Senior Full Stack Engineer & SaaS Founder

GitHub: [github.com/bricemehelo](https://github.com/bricemehelo)

> "Teams and products that scale are built on standards — not quick fixes."

---

## What It Does

- Browse property listings on an interactive map
- Search and filter by city, type, status, and price range
- Click a map marker to highlight the matching listing card
- Click a listing card to fly the map to that property's location

---

## Tech Stack

### Backend

- **FastAPI** — Python web framework
- **SQLAlchemy** — ORM for PostgreSQL
- **Pydantic** — Data validation and serialisation
- **Alembic** — Database migrations
- **pytest** — Backend testing

### Frontend

- **React 18 + TypeScript** — UI framework
- **Vite** — Build tool
- **MapLibre GL JS** — Interactive map rendering
- **React Query (TanStack)** — Server state and data fetching
- **Jotai** — Global UI state management (filters, selected property)
- **Vitest + React Testing Library** — Frontend testing

### Infrastructure

- **Docker Compose** — Local multi-container setup
- **PostgreSQL 15** — Database
- **Vercel** — Frontend deployment
- **Railway** — Backend and database deployment
- **GitHub Actions** — CI/CD

---

## Architecture

Layered N-Tier architecture with strict separation of concerns:

```
Router → Service → Repository → Database
```

- **Router** — HTTP only. Status codes, request/response
- **Service** — Business logic only. Rules, validation, error handling
- **Repository** — Data access only. All PostgreSQL queries live here
- **Database** — PostgreSQL via SQLAlchemy ORM

---

## Design Patterns Used

| Pattern    | Where                                                              |
| ---------- | ------------------------------------------------------------------ |
| Singleton  | Database engine — created once, shared across all requests         |
| Repository | All DB queries behind PropertyRepository                           |
| Decorator  | FastAPI route decorators (@router.get, @router.post)               |
| Observer   | Jotai atoms — map and list react to shared selected property state |
| Adapter    | Axios API client wrapping HTTP calls                               |
| DTO        | Pydantic schemas separating API contract from DB model             |

---

## Project Structure

```
nestio/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   └── property.py
│   │   ├── schemas/
│   │   │   └── property.py
│   │   ├── repositories/
│   │   │   └── property_repo.py
│   │   ├── services/
│   │   │   └── property_service.py
│   │   └── routers/
│   │       └── properties.py
│   ├── alembic/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_property_repository.py
│   │   ├── test_property_service.py
│   │   └── test_property_router.py
│   ├── requirements.txt
│   └── .env
└── frontend/
    └── src/
        ├── api/
        │   ├── client.ts
        │   └── properties.ts
        ├── components/
        │   ├── Map.tsx
        │   ├── PropertyCard.tsx
        │   ├── PropertyList.tsx
        │   ├── SearchBar.tsx
        │   ├── FilterPanel.tsx
        │   └── __tests__/
        ├── hooks/
        │   └── useProperties.ts
        ├── store/
        │   └── propertyAtoms.ts
        └── types/
            └── property.ts
```

---

## Local Development Setup

### Prerequisites

- Python 3.13
- Node 20
- PostgreSQL 15
- Docker Desktop (for Docker Compose setup)

### Without Docker

**1. Start PostgreSQL**

```bash
brew services start postgresql@15
```

**2. Backend**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:

```
DATABASE_URL=postgresql://your_username@localhost:5432/nestio_db
TEST_DATABASE_URL=postgresql://your_username@localhost:5432/nestio_test_db
```

Run migrations:

```bash
alembic upgrade head
```

Start the server:

```bash
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

**3. Frontend**

```bash
cd frontend
nvm use 20
npm install
npm run dev
```

Create a `.env` file in the `frontend/` folder:

```
VITE_API_URL=http://localhost:8000
```

Frontend runs at `http://localhost:5173`

### With Docker Compose

```bash
docker compose up --build
```

All three services start automatically:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

---

## Running Tests

### Backend

```bash
cd backend
source venv/bin/activate
python3 -m pytest tests/ -v
```

### Frontend

```bash
cd frontend
npm run test
```

---

## API Endpoints

| Method | Endpoint               | Description                               |
| ------ | ---------------------- | ----------------------------------------- |
| GET    | `/api/properties/`     | List all properties with optional filters |
| GET    | `/api/properties/{id}` | Get a single property by ID               |
| POST   | `/api/properties/`     | Create a new property listing             |
| PATCH  | `/api/properties/{id}` | Partially update a property               |
| DELETE | `/api/properties/{id}` | Delete a property                         |

### Query Parameters for GET /api/properties/

| Parameter     | Type   | Description                        |
| ------------- | ------ | ---------------------------------- |
| search        | string | Search title and description       |
| city          | string | Filter by city                     |
| property_type | string | apartment, house, land, commercial |
| status        | string | for_sale, for_rent, sold, rented   |
| min_price     | number | Minimum price filter               |
| max_price     | number | Maximum price filter               |
| skip          | number | Pagination offset                  |
| limit         | number | Results per page (max 100)         |

---

## Deployment

- **Frontend** — Vercel. Connect the GitHub repo and set `VITE_API_URL` to the Railway backend URL.
- **Backend** — Railway. Set `DATABASE_URL` to the Railway PostgreSQL instance URL.

---

## Standards

- Conventional commits — `feat:`, `fix:`, `chore:`, `test:`, `refactor:`
- No secrets in code — all configuration via `.env` files
- Layered separation — routers know nothing about DB, repositories know nothing about HTTP
- Tests written for every layer — repository, service, router, and frontend components
- Comments on every file explaining what and why

---

# Terminal 1 — Backend

cd ~/Projects/2026/nestio/backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 — Frontend

cd ~/Projects/2026/nestio/frontend
nvm use 20
npm run dev

# Confirm PostgreSQL is running

brew services start postgresql@15

Docker implemented
fix map
preparing for CI/CD
preparing for AI integration

Note: consider applying this to portharcourt as case study
