# 🚀 Meno Match - Getting Started

## Project Overview

**Meno Match** is an intelligent speaker search and matching platform with a clean separation of concerns using a monorepo architecture.

### Key Features (Epic 1)
- ✅ Natural language speaker search
- ✅ Global speaker discovery  
- ✅ Relevance-based ranking
- ✅ Advanced filtering by expertise, geography, topics
- ✅ Consolidated speaker profiles
- ✅ Engagement history tracking

### Tech Stack
- **Backend**: Python + FastAPI + SQLAlchemy
- **Frontend**: React + TypeScript + Vite
- **Database**: PostgreSQL
- **Architecture**: Monorepo (packages/backend, packages/frontend, packages/shared)

## 📁 Project Structure

```
meno-match/
├── packages/
│   ├── backend/              # FastAPI server
│   │   ├── src/
│   │   │   ├── main.py       # FastAPI app entry point
│   │   │   ├── models.py     # SQLAlchemy ORM models
│   │   │   ├── schemas.py    # Pydantic validation schemas
│   │   │   ├── services.py   # Business logic
│   │   │   ├── database.py   # Database initialization
│   │   │   ├── routes_speakers.py   # Search endpoints
│   │   │   └── routes_profiles.py   # Profile endpoints
│   │   ├── requirements.txt
│   │   ├── run.py
│   │   └── .env              # Environment variables
│   │
│   ├── frontend/             # React Vite app
│   │   ├── src/
│   │   │   ├── App.tsx       # Main component
│   │   │   ├── services.ts   # API client
│   │   │   ├── config.ts     # Configuration
│   │   │   └── components/
│   │   │       ├── SearchBar.tsx
│   │   │       ├── SearchResults.tsx
│   │   │       ├── SpeakerCard.tsx
│   │   │       └── SpeakerProfileView.tsx
│   │   ├── index.html
│   │   ├── vite.config.ts
│   │   └── package.json
│   │
│   └── shared/               # Shared TypeScript types
│       └── src/types.ts
│
├── epics/                    # Feature epics documentation
│   ├── E1-speaker-search-matching/
│   ├── E2-speaker-profiles-engagement/
│   └── E3-speaker-recommendations/
│
├── SETUP.md                  # Detailed setup instructions
├── ARCHITECTURE.md           # System architecture
├── docker-compose.yml        # PostgreSQL container
├── install.sh                # Automatic installation script
└── quickstart.sh             # Quick start script
```

## ⚡ Quick Start (5 minutes)

### Option 1: Automatic Installation

```bash
# Make scripts executable
chmod +x install.sh quickstart.sh

# Install dependencies
./install.sh

# Start PostgreSQL
docker-compose up -d

# Start backend (Terminal 1)
cd packages/backend
source venv/bin/activate
python run.py

# Start frontend (Terminal 2)  
cd packages/frontend
npm run dev
```

Then visit **http://localhost:3000**

### Option 2: Manual Installation

#### Step 1: Install Python Dependencies
```bash
cd packages/backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Step 2: Start Database
```bash
docker-compose up -d
# Or use local PostgreSQL with these credentials:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/meno_match
```

#### Step 3: Initialize Database
```bash
# From packages/backend/ with venv activated
python3 -c "from src.database import init_db, seed_db; init_db(); seed_db()"
```

#### Step 4: Start Backend
```bash
python run.py
# Backend runs on http://localhost:3001
# API docs: http://localhost:3001/docs
```

#### Step 5: Start Frontend
```bash
cd packages/frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

## 🧪 Testing the App

### Try Natural Language Search
1. Go to http://localhost:3000
2. Type: "French climate experts"
3. See results ranked by relevance

### Try with Filters
1. Click "Show Filters"
2. Select geography (e.g., "France")
3. Search again

### View Speaker Profile
1. Click "View Profile" on any speaker card
2. See full details, expertise, and engagement history

### API Testing

Using cURL:
```bash
# Search speakers
curl -X POST http://localhost:3001/api/speakers/search \
  -H "Content-Type: application/json" \
  -d '{
    "natural_language_query": "AI machine learning",
    "limit": 10
  }'

# Get speaker profile
curl http://localhost:3001/api/profiles/[speaker_id]

# Health check
curl http://localhost:3001/health
```

Or use the interactive docs at **http://localhost:3001/docs**

## 📊 Database

### Tables

**speakers**
- Core speaker information
- JSON arrays for expertise, topics, geography, languages
- Indexed on email for quick lookups

**engagements**
- Historical event participation
- Feedback ratings (1-5)
- Linked to speakers via speaker_id

**search_history**
- Analytics tracking
- Query logs for trending analysis

### Sample Data
The database is pre-seeded with 5 sample speakers from different regions and disciplines:
- Marie Dubois (Climate/Sustainability Expert - France)
- Dr. Priya Sharma (AI/ML Researcher - India)  
- João Silva (Social Entrepreneur - Brazil)
- Dr. Emma Johnson (Healthcare Innovation - UK)
- Kenji Tanaka (Cross-Cultural Communication - Japan)

## 🎯 Features & Epics

### Epic 1: Speaker Search & Intelligent Matching ✅ READY
- M1: Natural language search ✓
- M2: Global speaker discovery ✓
- M4: Relevance ranking ✓
- M5: Advanced filtering ✓
- M6: High-level queries ✓
- M7: Direct profile access ✓
- M8: Core context display ✓
- M9: Manual selection ✓

### Epic 2: Speaker Profiles & Engagement 📋 PLANNED
- Advanced profile customization
- Media galleries
- Testimonials and references
- Performance analytics

### Epic 3: Speaker Recommendations 🤖 PLANNED
- Personalized recommendations
- ML-powered matching
- Analytics-driven suggestions

## 🔧 Development

### Adding a New Speaker
```bash
# Backend console (with venv activated)
python3
```

```python
from src.database import SessionLocal
from src.models import Speaker

db = SessionLocal()
speaker = Speaker(
    first_name="John",
    last_name="Smith",
    email="john@example.com",
    biography="Expert speaker",
    expertise=["public speaking", "business"],
    topics=["leadership"],
    geography=["USA"],
    languages=["English"]
)
db.add(speaker)
db.commit()
```

### Modifying Search Logic
Edit `packages/backend/src/services.py` - `SpeakerService.search_speakers()`

### Modifying Frontend UI
Edit components in `packages/frontend/src/components/`

### Environment Variables

Backend (`.env`):
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/meno_match
API_PORT=3001
DEBUG=True
```

Frontend (optional, defaults to localhost):
```
VITE_API_URL=http://localhost:3001
```

## 📚 API Documentation

Auto-generated interactive docs available at: **http://localhost:3001/docs**

### Main Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/speakers/search` | Search speakers by natural language |
| GET | `/api/speakers/` | List all speakers with pagination |
| GET | `/api/profiles/{id}` | Get speaker profile with history |
| GET | `/health` | Service health check |

## 🚀 Deployment

### Development
```bash
# Terminal 1 - Backend
cd packages/backend
source venv/bin/activate
python run.py

# Terminal 2 - Frontend
cd packages/frontend
npm run dev
```

### Production Build
```bash
# Backend
python run.py  # (with DEBUG=False)

# Frontend  
npm run build   # Creates dist/ folder
npm run preview # Test production build locally
```

## 🐛 Troubleshooting

### "Connection refused" on port 3001
- Ensure backend is running: `python run.py`
- Check `.env` DATABASE_URL is correct
- PostgreSQL must be running: `docker-compose up -d`

### "Cannot GET /" on port 3000
- Ensure frontend is running: `npm run dev`
- Check it's on correct port in vite.config.ts

### Database "no rows" returned
- Run seed script: `python -c "from src.database import seed_db; seed_db()"`
- Check database connection: `psql -U postgres -d meno_match -c "SELECT COUNT(*) FROM speakers;"`

### Module import errors (Python)
- Activate venv: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Dependencies not installing
```bash
# Backend - upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt

# Frontend
npm install
```

## 📖 Additional Resources

- **Architecture Details**: See [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Detailed Setup**: See [SETUP.md](./SETUP.md)
- **API Docs**: http://localhost:3001/docs (when running)
- **Epic Specifications**: See `epics/E*/docs/`

## 👥 Team Roles

### For Data Engineers
- Expand speaker dataset with real data
- Implement advanced NLP matching
- Add Elasticsearch for enterprise search
- See: `packages/backend/src/services.py` - `SpeakerService.search_speakers()`

### For Architects  
- Design caching strategy (Redis)
- Plan database scaling
- Implement API versioning
- Set up monitoring and logging

### For UI Engineers
- Add autocomplete to search
- Implement advanced filter UI
- Add speaker comparison feature
- Create profile editing interface

## 🎓 Learning Path

1. **Start**: Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the system
2. **Explore**: Browse the codebase structure
3. **Test**: Run the app and try the features
4. **Modify**: Edit code and see changes live (hot reload)
5. **Extend**: Add new features following existing patterns

## 📝 Next Steps

- [ ] Set up database locally
- [ ] Run the application
- [ ] Search for speakers using natural language
- [ ] Test API directly using `/docs`
- [ ] Customize sample speaker data
- [ ] Deploy to staging/production

## 🤝 Contributing

1. Create a feature branch from `dev`
2. Make changes and test locally
3. Create a Pull Request with description
4. Team reviews and provides feedback
5. Merge to `dev`

---

**Ready to get started?** Follow the [Quick Start](#-quick-start-5-minutes) section above!

Questions? Check [SETUP.md](./SETUP.md) or [ARCHITECTURE.md](./ARCHITECTURE.md)
