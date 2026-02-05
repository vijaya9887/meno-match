from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_, or_, text, cast, String
from sqlalchemy.dialects.postgresql import JSON, JSONB
from src.models import Speaker, Engagement, SearchHistory
from src.schemas import SpeakerCreate, SpeakerUpdate, SearchFilters
from typing import List, Optional
from uuid import UUID

class SpeakerService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_speaker_by_id(self, speaker_id: UUID) -> Optional[Speaker]:
        return self.db.query(Speaker).filter(Speaker.id == speaker_id).first()
    
    def get_speaker_by_email(self, email: str) -> Optional[Speaker]:
        return self.db.query(Speaker).filter(Speaker.email == email).first()
    
    def create_speaker(self, speaker_data: SpeakerCreate) -> Speaker:
        db_speaker = Speaker(**speaker_data.dict())
        self.db.add(db_speaker)
        self.db.commit()
        self.db.refresh(db_speaker)
        return db_speaker
    
    def update_speaker(self, speaker_id: UUID, speaker_data: SpeakerUpdate) -> Optional[Speaker]:
        db_speaker = self.get_speaker_by_id(speaker_id)
        if not db_speaker:
            return None
        
        update_data = speaker_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_speaker, field, value)
        
        self.db.commit()
        self.db.refresh(db_speaker)
        return db_speaker
    
    def list_all_speakers(self, limit: int = 10, offset: int = 0) -> tuple[List[Speaker], int]:
        total = self.db.query(Speaker).count()
        speakers = self.db.query(Speaker).limit(limit).offset(offset).all()
        return speakers, total
    
    def search_speakers(
        self, 
        natural_language_query: str, 
        filters: Optional[SearchFilters] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[Speaker], int]:
        """
        MVP: Simple speaker search by expertise keywords
        Returns all speakers, optionally filtered by expertise
        """
        query = self.db.query(Speaker)
        
        # MVP: For query like "AI", search for it in expertise/topics JSON as text
        if natural_language_query:
            search_keywords = natural_language_query.lower().split()
            # Search expertise/topics using like on the JSON text representation
            or_conditions = []
            for keyword in search_keywords:
                or_conditions.append(text(f"speakers.expertise::text ILIKE '%{keyword}%'"))
                or_conditions.append(text(f"speakers.topics::text ILIKE '%{keyword}%'"))
            
            if or_conditions:
                query = query.filter(or_(or_conditions[0], *or_conditions[1:]))
        
        # Apply filters
        if filters:
            if filters.expertise:
                query = query.filter(Speaker.expertise.op('@>')(cast(filters.expertise, JSONB)))
            if filters.discipline:
                query = query.filter(Speaker.discipline.op('@>')(cast(filters.discipline, JSONB)))
            if filters.topic:
                query = query.filter(Speaker.topics.op('@>')(cast(filters.topic, JSONB)))
            if filters.audience_type:
                query = query.filter(Speaker.audience_types.op('@>')(cast(filters.audience_type, JSONB)))
            if filters.geography:
                query = query.filter(Speaker.geography.op('@>')(cast(filters.geography, JSONB)))
            if filters.languages:
                query = query.filter(Speaker.languages.op('@>')(cast(filters.languages, JSONB)))
        
        total = query.count()
        speakers = query.limit(limit).offset(offset).all()
        
        # Log search for analytics
        self._log_search(natural_language_query, filters, total)
        
        return speakers, total
    
    def _log_search(self, query: str, filters: Optional[SearchFilters], results_count: int):
        """Log search queries for analytics"""
        search_history = SearchHistory(
            query=query,
            filters=filters.dict() if filters else None,
            results_count=results_count
        )
        self.db.add(search_history)
        self.db.commit()


class EngagementService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_engagement(self, speaker_id: UUID, engagement_data: dict) -> Engagement:
        db_engagement = Engagement(speaker_id=speaker_id, **engagement_data)
        self.db.add(db_engagement)
        self.db.commit()
        self.db.refresh(db_engagement)
        return db_engagement
    
    def get_speaker_engagements(self, speaker_id: UUID) -> List[Engagement]:
        """Get engagement history for a speaker"""
        return self.db.query(Engagement).filter(Engagement.speaker_id == speaker_id).all()
