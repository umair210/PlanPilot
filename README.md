# PlanPilot

PlanPilot is a full-stack app that turns goals into structured phases and tasks.

## Tech Stack
- Backend: FastAPI, SQLAlchemy (async), SQLite, OpenAI API
- Frontend: SvelteKit, Vite, TypeScript, GSAP

## Requirements
- Python 3.11+
- Node.js 18+
- npm

## Setup

### Backend
```bash
cd backend
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -e .
cp .env.example .env

uvicorn app.main:app --port 8000
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env

npm run dev
```

Open http://localhost:5173

## Environment Variables

### backend/.env
- OPENAI_API_KEY (required for AI plan generation)
- OPENAI_MODEL (gpt-5.2)
- DATABASE_URL (default: sqlite+aiosqlite:///./planpilot.db)
- CORS_ORIGINS (default: http://localhost:5173)

### frontend/.env
- VITE_API_BASE_URL (example: http://localhost:8000)

## Production Notes
- Set CORS_ORIGINS to your deployed frontend origin (comma-separated).
- If frontend and backend share the same origin, CORS is not needed.
- Keep secrets in environment variables


## API
- Health: http://localhost:8000/health
- API base: http://localhost:8000
- API docs: http://localhost:8000/docs

## License
Add a LICENSE file (MIT is a common choice).
