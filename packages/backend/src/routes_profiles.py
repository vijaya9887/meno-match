from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import SpeakerProfile, EngagementResponse
from src.services import SpeakerService, EngagementService
from src.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/profiles", tags=["profiles"])

@router.get("/{speaker_id}", response_model=SpeakerProfile)
async def get_speaker_profile(
    speaker_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get consolidated speaker profile.
    
    Features:
    - M7: Open consolidated speaker profile from search results
    - M8: See core context (expertise, prior engagement)
    """
    speaker_service = SpeakerService(db)
    speaker = speaker_service.get_speaker_by_id(speaker_id)
    
    if not speaker:
        raise HTTPException(status_code=404, detail="Speaker not found")
    
    engagement_service = EngagementService(db)
    engagements = engagement_service.get_speaker_engagements(speaker_id)
    
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
    }
    
    engagement_responses = [
        EngagementResponse(
            id=e.id,
            event_name=e.event_name,
            event_date=e.event_date,
            audience_size=e.audience_size,
            topic=e.topic,
            feedback_rating=e.feedback_rating,
            notes=e.notes,
            speaker_id=e.speaker_id,
            created_at=e.created_at,
        )
        for e in engagements
    ]
    
    from src.schemas import SpeakerResponse
    return SpeakerProfile(
        speaker=SpeakerResponse(**speaker_dict),
        engagement_history=engagement_responses
    )
