import api from './api';
import { API_ENDPOINTS } from './config';

export interface Speaker {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  biography?: string;
  profile_image_url?: string;
  expertise: string[];
  discipline: string[];
  topics: string[];
  audience_types: string[];
  geography: string[];
  languages: string[];
  availability_status: string;
  relevance_score?: number;
  created_at: string;
  updated_at: string;
}

export interface SearchQuery {
  natural_language_query: string;
  filters?: {
    expertise?: string[];
    discipline?: string[];
    topic?: string[];
    audience_type?: string[];
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

export interface Engagement {
  id: string;
  event_name: string;
  event_date: string;
  audience_size?: number;
  topic?: string;
  feedback_rating?: number;
  notes?: string;
  speaker_id: string;
  created_at: string;
}

export interface SpeakerProfile {
  speaker: Speaker;
  engagement_history: Engagement[];
}

export const speakerApi = {
  search: (query: SearchQuery) =>
    api.post<SearchResult>(API_ENDPOINTS.SPEAKERS_SEARCH, query),

  list: (limit = 10, offset = 0) =>
    api.get<SearchResult>(API_ENDPOINTS.SPEAKERS_LIST, {
      params: { limit, offset },
    }),

  getProfile: (speakerId: string) =>
    api.get<SpeakerProfile>(API_ENDPOINTS.SPEAKER_PROFILE(speakerId)),
};
