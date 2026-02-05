import React, { useState, useEffect } from 'react';
import { ArrowLeft, MapPin, Globe, Award, MessageSquare, Calendar } from 'lucide-react';
import { speakerApi, SpeakerProfile } from '../services';

interface SpeakerProfileViewProps {
  speakerId: string;
  onBack: () => void;
}

export const SpeakerProfileView: React.FC<SpeakerProfileViewProps> = ({ speakerId, onBack }) => {
  const [profile, setProfile] = useState<SpeakerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        setLoading(true);
        const response = await speakerApi.getProfile(speakerId);
        setProfile(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to load speaker profile');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, [speakerId]);

  if (loading) {
    return (
      <div className="p-6">
        <button onClick={onBack} className="text-blue-600 hover:text-blue-800 mb-4 flex items-center gap-2">
          <ArrowLeft size={20} /> Back
        </button>
        <div className="text-center py-12">Loading profile...</div>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="p-6">
        <button onClick={onBack} className="text-blue-600 hover:text-blue-800 mb-4 flex items-center gap-2">
          <ArrowLeft size={20} /> Back
        </button>
        <div className="text-center py-12 text-red-600">{error || 'Profile not found'}</div>
      </div>
    );
  }

  const { speaker, engagement_history } = profile;

  return (
    <div className="p-6 max-w-4xl">
      <button onClick={onBack} className="text-blue-600 hover:text-blue-800 mb-6 flex items-center gap-2">
        <ArrowLeft size={20} /> Back to Results
      </button>

      <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {speaker.first_name} {speaker.last_name}
        </h1>
        <p className="text-gray-600 mb-6">{speaker.biography}</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Expertise</h3>
            <div className="flex flex-wrap gap-2">
              {speaker.expertise.map((exp) => (
                <span key={exp} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                  {exp}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Topics</h3>
            <div className="flex flex-wrap gap-2">
              {speaker.topics.map((topic) => (
                <span key={topic} className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">
                  {topic}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Geography</h3>
            <div className="flex items-center gap-2">
              <MapPin size={20} className="text-gray-500" />
              <span>{speaker.geography.join(', ')}</span>
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Languages</h3>
            <div className="flex flex-wrap gap-2">
              {speaker.languages.map((lang) => (
                <span key={lang} className="bg-gray-200 text-gray-800 px-3 py-1 rounded text-sm">
                  {lang}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Audience Types</h3>
            <div className="flex flex-wrap gap-2">
              {speaker.audience_types.map((type) => (
                <span key={type} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                  {type}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Availability</h3>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium ${
                speaker.availability_status === 'available'
                  ? 'bg-green-100 text-green-800'
                  : speaker.availability_status === 'busy'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-red-100 text-red-800'
              }`}
            >
              {speaker.availability_status.charAt(0).toUpperCase() + speaker.availability_status.slice(1)}
            </span>
          </div>
        </div>
      </div>

      {engagement_history.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Prior Engagements</h2>
          <div className="space-y-4">
            {engagement_history.map((engagement) => (
              <div key={engagement.id} className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-900">{engagement.event_name}</h3>
                  {engagement.feedback_rating && (
                    <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
                      ⭐ {engagement.feedback_rating}/5
                    </span>
                  )}
                </div>
                <p className="text-gray-600 text-sm mt-1">{engagement.topic}</p>
                {engagement.audience_size && (
                  <p className="text-gray-500 text-sm">Audience: {engagement.audience_size} people</p>
                )}
                {engagement.notes && <p className="text-gray-500 text-sm mt-2">{engagement.notes}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Contact & Next Steps</h3>
        <p className="text-gray-700 mb-4">
          Ready to book this speaker? You can make the final selection yourself. Click below to get in touch.
        </p>
        <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
          Contact Speaker
        </button>
      </div>
    </div>
  );
};
