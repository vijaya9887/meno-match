from sqlalchemy import Column, String, Text, DateTime, Integer, Enum as SQLEnum, create_engine, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"

class Speaker(Base):
    __tablename__ = "speakers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    biography = Column(Text)
    profile_image_url = Column(String(500))
    expertise = Column(JSONB, default=[])
    discipline = Column(JSONB, default=[])
    topics = Column(JSONB, default=[])
    audience_types = Column(JSONB, default=[])
    geography = Column(JSONB, default=[])
    languages = Column(JSONB, default=[])
    availability_status = Column(SQLEnum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    engagements = relationship("Engagement", back_populates="speaker", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Speaker {self.first_name} {self.last_name}>"


class Engagement(Base):
    __tablename__ = "engagements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    speaker_id = Column(UUID(as_uuid=True), ForeignKey("speakers.id", ondelete="CASCADE"), nullable=False)
    event_name = Column(String(255), nullable=False)
    event_date = Column(DateTime, nullable=False)
    audience_size = Column(Integer)
    topic = Column(String(255))
    feedback_rating = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    speaker = relationship("Speaker", back_populates="engagements")
    
    def __repr__(self):
        return f"<Engagement {self.event_name}>"


class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(Text, nullable=False)
    filters = Column(JSONB)
    results_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SearchHistory {self.query}>"
