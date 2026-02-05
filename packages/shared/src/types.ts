// Shared types for E1: Speaker Search & Intelligent Matching

export interface Speaker {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  biography: string;
  profileImageUrl?: string;
  expertise: string[];
  discipline: string[];
  topics: string[];
  audienceTypes: string[];
  geography: string[];
  languages: string[];
  priorEngagements?: number;
  relevanceScore?: number;
  availabilityStatus: 'available' | 'busy' | 'unavailable';
  createdAt: Date;
  updatedAt: Date;
}

export interface SearchQuery {
  naturalLanguageQuery: string;
  filters?: {
    expertise?: string[];
    discipline?: string[];
    topic?: string[];
    audienceType?: string[];
    geography?: string[];
    languages?: string[];
  };
  limit?: number;
  offset?: number;
}

export interface SearchResult {
  speakers: Speaker[];
  total: number;
  limit: number;
  offset: number;
}

export interface SpeakerProfile {
  speaker: Speaker;
  engagementHistory: Engagement[];
  references?: string[];
  mediaLinks?: string[];
}

export interface Engagement {
  id: string;
  speakerId: string;
  eventName: string;
  eventDate: Date;
  audience: number;
  topic: string;
  feedback?: number; // rating 1-5
  notes?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: Date;
}
