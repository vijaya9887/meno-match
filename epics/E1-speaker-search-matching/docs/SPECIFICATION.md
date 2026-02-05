# Epic 1: Speaker Search & Intelligent Matching

## Features (MVPs)

- **M1: Natural Language Search** - Users can search for speakers using natural language rather than predefined fields
  - Example: "Show me French climate experts" or "AI speakers for tech conferences"
  - Implementation: `/api/speakers/search` endpoint with NLP-like text matching

- **M2: Global Discovery** - Users can discover speakers beyond their personal network or country
  - Implementation: Database contains speakers from multiple countries/disciplines
  - Pagination and browsing support

- **M4: Relevance Ranking** - Users can see speakers ranked by relevance to their stated need
  - Implementation: Relevance scoring algorithm based on query matches
  - Higher scores for direct expertise matches

- **M5: Advanced Filtering** - Users can filter speakers by expertise, discipline, topic, audience type, geography, languages
  - Faceted search interface
  - Multi-select filters

- **M6: Minimal Input Queries** - Users can search using high-level input without a full requirements list
  - Single or two-word queries work effectively
  - Example: "French speakers" returns all French speakers

- **M7: Direct Profile Access** - Users can open a consolidated speaker profile directly from search results
  - Click-to-view profiles
  - Single view with all relevant information

- **M8: Core Context Display** - Users can see core context in profiles (expertise, prior engagement, feedback)
  - Engagement history with ratings
  - Audience statistics
  - Topic history

- **M9: Manual Selection** - Users can make the final selection themselves, supported but not replaced by the tool
  - Clear contact options
  - No auto-selection

## Architecture

### Backend (Python/FastAPI)
- **Service Layer**: Business logic for search, scoring, filtering
- **Database Layer**: PostgreSQL with SQLAlchemy ORM
- **API Routes**: RESTful endpoints for search and profiles
- **Models**: Speaker, Engagement, SearchHistory

### Frontend (React/TypeScript)
- **Search Component**: Natural language input with optional filters
- **Results Display**: Speaker cards with relevance scores
- **Profile View**: Consolidated speaker information
- **Responsive Design**: Mobile-friendly UI

### Database Schema
- `speakers`: Core speaker information with JSON arrays for expertise, topics, etc.
- `engagements`: Historical event data for each speaker
- `search_history`: Analytics tracking

## API Endpoints

### Search
- `POST /api/speakers/search`
  - Request: `SearchQuery` with natural language query and optional filters
  - Response: `SearchResult` with ranked speakers

### List
- `GET /api/speakers?limit=10&offset=0`
  - Response: Paginated speaker list

### Profile
- `GET /api/profiles/{speaker_id}`
  - Response: `SpeakerProfile` with engagement history

## Next Steps for Team

1. **Data Engineer**: Expand speaker dataset, implement advanced matching algorithms
2. **Architect**: Scale search performance (add Elasticsearch for full-text search), implement caching
3. **UI Engineer**: Enhance UX with autocomplete, advanced filtering UI, profile refinements

## Setup Instructions

See [Setup Guide](./SETUP.md)
