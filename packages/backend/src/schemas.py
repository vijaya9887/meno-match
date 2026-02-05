from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

# Speaker schemas
class SpeakerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    biography: Optional[str] = None
    profile_image_url: Optional[str] = None
    expertise: List[str] = []
    discipline: List[str] = []
    topics: List[str] = []
    audience_types: List[str] = []
    geography: List[str] = []
    languages: List[str] = []
    availability_status: str = "available"

class SpeakerCreate(SpeakerBase):
    pass

class SpeakerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    biography: Optional[str] = None
    profile_image_url: Optional[str] = None
    expertise: Optional[List[str]] = None
    discipline: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    audience_types: Optional[List[str]] = None
    geography: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    availability_status: Optional[str] = None

class SpeakerResponse(SpeakerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    relevance_score: Optional[float] = None
    
    class Config:
        from_attributes = True

# Engagement schemas
class EngagementBase(BaseModel):
    event_name: str
    event_date: datetime
    audience_size: Optional[int] = None
    topic: Optional[str] = None
    feedback_rating: Optional[int] = None
    notes: Optional[str] = None

class EngagementCreate(EngagementBase):
    speaker_id: UUID

class EngagementResponse(EngagementBase):
    id: UUID
    speaker_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

# Speaker Profile
class SpeakerProfile(BaseModel):
    speaker: SpeakerResponse
    engagement_history: List[EngagementResponse] = []
    
    class Config:
        from_attributes = True

# Search schemas
class SearchFilters(BaseModel):
    expertise: Optional[List[str]] = None
    discipline: Optional[List[str]] = None
    topic: Optional[List[str]] = None
    audience_type: Optional[List[str]] = None
    geography: Optional[List[str]] = None
    languages: Optional[List[str]] = None

class SearchQuery(BaseModel):
    natural_language_query: str
    filters: Optional[SearchFilters] = None
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)

class SearchResult(BaseModel):
    speakers: List[SpeakerResponse]
    total: int
    limit: int
    offset: int

# Generic response
class ApiResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
