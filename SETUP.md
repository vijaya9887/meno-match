# Meno Match - Setup & Running Guide

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 12+

### 1. Backend Setup

```bash
# Navigate to backend
cd packages/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database and seed
python -c "from src.database import init_db, seed_db; init_db(); seed_db()"

# Run server
python run.py
```

Backend will be available at `http://localhost:3001`
API docs available at `http://localhost:3001/docs`

### 2. Frontend Setup

```bash
# Navigate to frontend
cd packages/frontend

# Install dependencies
npm install

# Create .env file (optional - defaults to localhost)
echo "VITE_API_URL=http://localhost:3001" > .env

# Run dev server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 3. Database Setup (if using existing PostgreSQL)

Make sure PostgreSQL is running and update `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/meno_match
```

## Database Setup with Docker (Optional)

```bash
# Start PostgreSQL
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# Wait a moment then initialize
python packages/backend/run.py
```

## Testing the Application

### 1. Search by Natural Language
- Visit `http://localhost:3000`
- Try: "Show me French speakers" or "AI machine learning experts"

### 2. Filter Results
- Click "Show Filters"
- Select geography, then search

### 3. View Speaker Profile
- Click "View Profile" on any speaker card
- See expertise, engagement history, and feedback

## API Testing

### Using cURL
```bash
# Search speakers
curl -X POST http://localhost:3001/api/speakers/search \
  -H "Content-Type: application/json" \
  -d '{
    "natural_language_query": "French climate experts",
    "limit": 10,
    "offset": 0
  }'

# Get specific profile
curl http://localhost:3001/api/profiles/{speaker_id}
```

### Using FastAPI Docs
Navigate to `http://localhost:3001/docs` for interactive API documentation

## Project Structure

```
meno-match/
├── packages/
│   ├── backend/
│   │   ├── src/
│   │   │   ├── main.py          # FastAPI app
│   │   │   ├── models.py        # SQLAlchemy models
│   │   │   ├── schemas.py       # Pydantic schemas
│   │   │   ├── services.py      # Business logic
│   │   │   ├── database.py      # DB initialization
│   │   │   ├── routes_speakers.py
│   │   │   ├── routes_profiles.py
│   │   │   └── config.py
│   │   ├── requirements.txt
│   │   └── run.py
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── App.tsx
│   │   │   ├── services.ts      # API client
│   │   │   ├── config.ts
│   │   │   └── components/
│   │   │       ├── SearchBar.tsx
│   │   │       ├── SpeakerCard.tsx
│   │   │       ├── SearchResults.tsx
│   │   │       └── SpeakerProfileView.tsx
│   │   ├── package.json
│   │   └── vite.config.ts
│   └── shared/
│       └── src/
│           └── types.ts         # Shared TypeScript types
└── epics/
    ├── E1-speaker-search-matching/
    │   └── docs/
    ├── E2-speaker-profiles-engagement/
    │   └── docs/
    └── E3-speaker-recommendations/
        └── docs/
```

## Available Commands

### Backend
```bash
cd packages/backend
python run.py                    # Start dev server
python -c "from src.database import seed_db; seed_db()"  # Reseed database
```

### Frontend
```bash
cd packages/frontend
npm run dev                      # Development server
npm run build                    # Production build
npm run preview                  # Preview production build
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in backend: edit src/config.py, API_PORT variable
# Change port in frontend: edit vite.config.ts, port in server config
```

### Database Connection Failed
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env is correct
- Run: `psql -U postgres -d meno_match -c "SELECT 1"`

### CORS Errors
- Check frontend and backend URLs match in vite.config.ts proxy
- Backend CORS is enabled for all origins (*) - restrict in production

## Performance Tips

- Use SQLAlchemy query optimization with select() and joinedload()
- Add database indexes on frequently searched fields (email, geography)
- Implement Redis caching for search results
- Use full-text search (PostgreSQL FTS) for better natural language matching

## Next Steps

1. **Data Engineer**: 
   - Expand speaker database with real data
   - Implement advanced NLP for better search relevance
   - Add Elasticsearch for enterprise search

2. **Architect**:
   - Design caching strategy
   - Plan database scaling
   - Document API versioning strategy

3. **UI Engineer**:
   - Add autocomplete to search
   - Implement advanced filter UI
   - Add speaker comparison feature
