# Meno Match - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                           │
└──────────────────────────────────┬──────────────────────────────┘
                                   │ HTTP/REST
                    ┌──────────────┴──────────────┐
                    │                             │
        ┌───────────▼────────────┐    ┌───────────▼────────────┐
        │   React Frontend       │    │   Vite Dev Server    │
        │   (Port 3000)          │    │   (Port 3000)        │
        │                        │    │                      │
        │ - SearchBar            │    │ - Hot Module Reload  │
        │ - SearchResults        │    │ - Dev Tools          │
        │ - SpeakerCard          │    │ - CSS Processing     │
        │ - ProfileView          │    │                      │
        └───────────┬────────────┘    └──────────────────────┘
                    │ API Calls (/api/*)
                    │
        ┌───────────▼────────────────────────────┐
        │   FastAPI Backend (Port 3001)         │
        │                                        │
        │   ┌─────────────────────────────────┐ │
        │   │   Route Handlers                │ │
        │   │ - /api/speakers/search          │ │
        │   │ - /api/speakers/                │ │
        │   │ - /api/profiles/{id}            │ │
        │   │ - /health                       │ │
        │   └─────────┬───────────────────────┘ │
        │             │                         │
        │   ┌─────────▼───────────────────────┐ │
        │   │   Service Layer                 │ │
        │   │ - SpeakerService                │ │
        │   │   - search_speakers()           │ │
        │   │   - get_speaker_by_id()         │ │
        │   │   - calculate_relevance_score() │ │
        │   │ - EngagementService             │ │
        │   │   - get_speaker_engagements()   │ │
        │   └─────────┬───────────────────────┘ │
        │             │                         │
        │   ┌─────────▼───────────────────────┐ │
        │   │   Database Layer                │ │
        │   │ - SQLAlchemy ORM                │ │
        │   │ - Query Builder                 │ │
        │   │ - Connection Pooling            │ │
        │   └─────────┬───────────────────────┘ │
        └─────────────┼────────────────────────┘
                      │ SQL Queries
        ┌─────────────▼────────────────────┐
        │   PostgreSQL Database            │
        │   (Port 5432)                    │
        │                                  │
        │   Tables:                        │
        │   - speakers                     │
        │   - engagements                  │
        │   - search_history               │
        └──────────────────────────────────┘
```

## Data Flow - Speaker Search

```
User Input
    │
    ▼
SearchBar Component (React)
    │
    ▼ query: "French climate experts"
API Call (POST /api/speakers/search)
    │
    ▼
FastAPI Route Handler
    │
    ▼
SpeakerService.search_speakers()
    │
    ├─► Natural Language Parsing
    │   - Extract keywords
    │   - Match against database fields
    │
    ├─► Apply Filters
    │   - Geography: France
    │   - Topics: Climate
    │   - Discipline: Environmental
    │
    ├─► Calculate Relevance Scores
    │   - Expertise match weight: 0.3
    │   - Topic match weight: 0.3
    │   - Geography match weight: 0.2
    │   - Language match weight: 0.1
    │
    ▼
SQLAlchemy Query Execution
    │
    ▼
PostgreSQL Full-Text Search + Filtering
    │
    ▼
Result Set (Sorted by Relevance)
    │
    ▼
JSON Response (SearchResult)
    │
    ▼
React SearchResults Component
    │
    ├─► Display Speaker Cards
    │   - Name, Biography
    │   - Expertise Tags
    │   - Relevance Score
    │   - Geography
    │
    └─► User Clicks "View Profile"
        │
        ▼
        API Call (GET /api/profiles/{id})
        │
        ▼
        SpeakerService.get_speaker_by_id()
        + EngagementService.get_speaker_engagements()
        │
        ▼
        Full Profile + Engagement History
        │
        ▼
        ProfileView Component
        │
        └─► Display Complete Information
            - Bio, Expertise, Topics
            - Prior Engagements with Feedback
            - Contact Options
```

## Component Structure

### Backend Components

#### Models (ORM Layer)
- **Speaker**: Core speaker information
  - id, name, email, biography
  - JSON arrays: expertise, topics, geography, languages
  - availability_status, timestamps

- **Engagement**: Event participation history
  - speaker_id (FK), event details
  - audience size, feedback rating
  - notes, created_at

- **SearchHistory**: Analytics
  - query, filters, results_count
  - created_at (for trending analysis)

#### Services (Business Logic)
- **SpeakerService**
  - `search_speakers(query, filters, limit, offset)` - Main search
  - `get_speaker_by_id(id)` - Single speaker lookup
  - `calculate_relevance_score(speaker, query)` - Scoring algorithm
  - `list_all_speakers(limit, offset)` - Pagination

- **EngagementService**
  - `get_speaker_engagements(speaker_id)` - Engagement history
  - `create_engagement(speaker_id, data)` - Record events

#### Routes
- `/api/speakers/search` - POST - Search with NLP query
- `/api/speakers/` - GET - List all speakers
- `/api/profiles/{id}` - GET - Full profile with history
- `/health` - GET - Service health check

### Frontend Components

#### Pages/Views
- **App.tsx** - Main container, state management
- **SearchBar.tsx** - Natural language input + filters
- **SearchResults.tsx** - Results grid
- **SpeakerCard.tsx** - Individual speaker card in results
- **SpeakerProfileView.tsx** - Full profile page

#### Services
- **services.ts** - API client functions
  - `speakerApi.search(query)`
  - `speakerApi.list(limit, offset)`
  - `speakerApi.getProfile(id)`

- **api.ts** - Axios HTTP client
- **config.ts** - API configuration

## Database Schema

### speakers table
```sql
id (UUID PK)
first_name (VARCHAR)
last_name (VARCHAR)
email (VARCHAR UNIQUE INDEX)
biography (TEXT)
profile_image_url (VARCHAR)
expertise (JSONB) - ["AI", "ML", "Data Science"]
discipline (JSONB) - ["Computer Science"]
topics (JSONB) - ["AI Ethics", "ML Trends"]
audience_types (JSONB) - ["Tech Companies", "Startups"]
geography (JSONB) - ["India", "Asia"]
languages (JSONB) - ["English", "Hindi"]
availability_status (ENUM)
created_at (TIMESTAMP)
updated_at (TIMESTAMP)
```

### engagements table
```sql
id (UUID PK)
speaker_id (UUID FK -> speakers)
event_name (VARCHAR)
event_date (TIMESTAMP)
audience_size (INT)
topic (VARCHAR)
feedback_rating (INT 1-5)
notes (TEXT)
created_at (TIMESTAMP)
```

### search_history table
```sql
id (UUID PK)
query (TEXT)
filters (JSONB)
results_count (INT)
created_at (TIMESTAMP INDEX)
```

## Scaling Considerations

### Short Term (MVP)
- Current setup: OK for <10k speakers
- Database: Single PostgreSQL instance
- Search: Simple SQL LIKE queries

### Medium Term (10k-100k speakers)
- Add Elasticsearch for full-text search
- Implement caching layer (Redis)
- Database read replicas
- API rate limiting

### Long Term (100k+ speakers)
- Distributed database (sharding)
- Advanced NLP with ML models
- Real-time search indexing
- Multi-region deployment

## Security Considerations

### Current Implementation
- CORS enabled for all origins (restrict in production)
- No authentication (add JWT/OAuth)
- No input validation (add stricter validation)

### Production Checklist
- [ ] Implement authentication
- [ ] Add rate limiting
- [ ] Validate all inputs with Joi/Pydantic
- [ ] Implement API versioning
- [ ] Add audit logging
- [ ] Set up error tracking (Sentry)
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS only
- [ ] Implement CORS restrictions

## Technology Stack Justification

| Component | Technology | Why |
|-----------|-----------|-----|
| Backend | FastAPI | Fast, modern Python framework; Async support; Auto API docs |
| Frontend | React + Vite | Modern UX; Hot reload; Excellent ecosystem |
| Database | PostgreSQL | JSONB support; Full-text search; Mature; Scalable |
| API | REST | Simple, well-understood; Good for CRUD operations |
| ORM | SQLAlchemy | Python standard; Flexible; Great query builder |
| Schema Validation | Pydantic | Type hints; Auto documentation; Serialization |

## Development Workflow

1. **Feature Branch** - Create feature branch from `dev`
2. **Local Development** - Make changes, test locally
3. **API Testing** - Use FastAPI docs at `/docs`
4. **Frontend Testing** - Test in browser with dev tools
5. **Database Testing** - Verify schema changes
6. **Pull Request** - Create PR to `dev` for review
7. **Code Review** - Team review and feedback
8. **Merge** - Squash commit to `dev`
9. **Deployment** - Deploy from `dev` to staging, then production

## Monitoring & Analytics

### Metrics to Track
- Search query volume and trends
- Search result click-through rate
- Profile view conversion
- Engagement booking rate
- Speaker satisfaction scores

### Implementation
- Database: search_history table
- Analytics: Query /api/analytics endpoints
- Dashboards: Build with your favorite BI tool
