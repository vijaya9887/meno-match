export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';

export const API_ENDPOINTS = {
  HEALTH: '/health',
  SPEAKERS_SEARCH: '/api/speakers/search',
  SPEAKERS_LIST: '/api/speakers',
  SPEAKER_PROFILE: (id: string) => `/api/profiles/${id}`,
};
