from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config import settings
from src.models import Base
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(settings.database_url, echo=settings.debug)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Dependency injection for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database tables created")

def seed_db():
    """Seed database with sample speakers"""
    from src.models import Speaker, AvailabilityStatus
    
    db = SessionLocal()
    
    mock_speakers = [
        {
            "first_name": "Marie",
            "last_name": "Dubois",
            "email": "marie.dubois@example.com",
            "biography": "Expert in sustainable development and climate policy with 15+ years of international experience",
            "expertise": ["sustainable development", "climate policy", "international relations"],
            "discipline": ["environmental science", "policy"],
            "topics": ["climate change", "sustainability", "green energy"],
            "audience_types": ["corporate", "academic", "government"],
            "geography": ["France", "Europe", "Africa"],
            "languages": ["French", "English", "Spanish"],
        },
        {
            "first_name": "Dr. Priya",
            "last_name": "Sharma",
            "email": "priya.sharma@example.com",
            "biography": "Leading AI and machine learning researcher, speaker at tech conferences worldwide",
            "expertise": ["artificial intelligence", "machine learning", "data science"],
            "discipline": ["computer science", "technology"],
            "topics": ["AI ethics", "machine learning trends", "digital transformation"],
            "audience_types": ["tech companies", "startups", "academic"],
            "geography": ["India", "Asia", "Global"],
            "languages": ["English", "Hindi"],
        },
        {
            "first_name": "João",
            "last_name": "Silva",
            "email": "joao.silva@example.com",
            "biography": "Social entrepreneur focusing on impact-driven business models in Latin America",
            "expertise": ["social entrepreneurship", "impact investing", "business development"],
            "discipline": ["business", "social impact"],
            "topics": ["social impact", "entrepreneurship", "sustainable business"],
            "audience_types": ["startups", "NGOs", "investors"],
            "geography": ["Brazil", "Latin America", "Portugal"],
            "languages": ["Portuguese", "English", "Spanish"],
        },
        {
            "first_name": "Dr. Emma",
            "last_name": "Johnson",
            "email": "emma.johnson@example.com",
            "biography": "Healthcare innovation leader specializing in digital health transformation",
            "expertise": ["healthcare innovation", "digital health", "medical technology"],
            "discipline": ["healthcare", "medical"],
            "topics": ["digital health", "telemedicine", "healthcare innovation"],
            "audience_types": ["hospitals", "pharma companies", "health tech"],
            "geography": ["UK", "Europe", "North America"],
            "languages": ["English"],
        },
        {
            "first_name": "Kenji",
            "last_name": "Tanaka",
            "email": "kenji.tanaka@example.com",
            "biography": "Cultural ambassador and expert in cross-cultural business communication",
            "expertise": ["cross-cultural communication", "business strategy", "organizational development"],
            "discipline": ["business", "culture"],
            "topics": ["cultural intelligence", "global teams", "business communication"],
            "audience_types": ["multinational corporations", "consulting firms"],
            "geography": ["Japan", "Asia", "Global"],
            "languages": ["Japanese", "English", "Mandarin"],
        },
    ]
    
    try:
        for speaker_data in mock_speakers:
            existing = db.query(Speaker).filter(Speaker.email == speaker_data["email"]).first()
            if not existing:
                speaker = Speaker(**speaker_data)
                db.add(speaker)
        
        db.commit()
        logger.info("✓ Database seeded with speakers")
    except Exception as e:
        logger.error(f"Seeding error: {e}")
        db.rollback()
    finally:
        db.close()
