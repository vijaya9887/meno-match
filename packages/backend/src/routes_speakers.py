from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import SearchQuery, SearchResult, SpeakerResponse
from src.services import SpeakerService
from src.database import get_db

router = APIRouter(prefix="/api/speakers", tags=["speakers"])

@router.post("/search", response_model=SearchResult)
async def search_speakers(
    search_query: SearchQuery,
    db: Session = Depends(get_db)
):
    """
    Search for speakers using natural language query.
    
    Features:
    - M1: Natural language search
    - M2: Discover speakers globally
    - M4: Ranked by relevance
    - M5: Filter by expertise, discipline, topic, geography, etc.
    - M6: High-level queries (e.g., "Show me French speakers")
    """
    service = SpeakerService(db)
    speakers, total = service.search_speakers(
        natural_language_query=search_query.natural_language_query,
        filters=search_query.filters,
        limit=search_query.limit,
        offset=search_query.offset
    )
    
    # M4: Add relevance scoring
    speakers_with_scores = []
    for speaker in speakers:
        speaker_dict = {
            "id": speaker.id,
            "first_name": speaker.first_name,
            "last_name": speaker.last_name,
            "email": speaker.email,
            "biography": speaker.biography,
            "profile_image_url": speaker.profile_image_url,
            "expertise": speaker.expertise,
            "discipline": speaker.discipline,
            "topics": speaker.topics,
            "audience_types": speaker.audience_types,
            "geography": speaker.geography,
            "languages": speaker.languages,
            "availability_status": speaker.availability_status,
            "created_at": speaker.created_at,
            "updated_at": speaker.updated_at,
            "relevance_score": calculate_relevance_score(speaker, search_query)
        }
        speakers_with_scores.append(SpeakerResponse(**speaker_dict))
    
    # Sort by relevance score descending
    speakers_with_scores.sort(key=lambda x: x.relevance_score or 0, reverse=True)
    
    return SearchResult(
        speakers=speakers_with_scores,
        total=total,
        limit=search_query.limit,
        offset=search_query.offset
    )

@router.get("/", response_model=SearchResult)
async def list_speakers(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all speakers with pagination"""
    service = SpeakerService(db)
    speakers, total = service.list_all_speakers(limit=limit, offset=offset)
    
    speaker_responses = [
        SpeakerResponse(
            id=s.id,
            first_name=s.first_name,
            last_name=s.last_name,
            email=s.email,
            biography=s.biography,
            profile_image_url=s.profile_image_url,
            expertise=s.expertise,
            discipline=s.discipline,
            topics=s.topics,
            audience_types=s.audience_types,
            geography=s.geography,
            languages=s.languages,
            availability_status=s.availability_status,
            created_at=s.created_at,
            updated_at=s.updated_at,
        )
        for s in speakers
    ]
    
    return SearchResult(
        speakers=speaker_responses,
        total=total,
        limit=limit,
        offset=offset
    )

def calculate_relevance_score(speaker, search_query: SearchQuery) -> float:
    """
    Calculate relevance score based on match quality.
    
    M4: Speakers ranked by relevance to stated need
    """
    score = 0.0
    query_lower = search_query.natural_language_query.lower()
    
    # Check expertise match
    expertise_matches = sum(1 for exp in speaker.expertise if exp.lower() in query_lower)
    score += expertise_matches * 0.3
    
    # Check topics match
    topic_matches = sum(1 for topic in speaker.topics if topic.lower() in query_lower)
    score += topic_matches * 0.3
    
    # Check filters
    if search_query.filters:
        if search_query.filters.geography:
            geography_matches = sum(1 for geo in search_query.filters.geography if geo in speaker.geography)
            score += geography_matches * 0.2
        
        if search_query.filters.languages:
            language_matches = sum(1 for lang in search_query.filters.languages if lang in speaker.languages)
            score += language_matches * 0.1
    
    return min(score, 100.0)  # Cap at 100
