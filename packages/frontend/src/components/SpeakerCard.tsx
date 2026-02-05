import React from 'react';
import { MapPin, Users, Globe, Award } from 'lucide-react';
import { Speaker } from '../services';

interface SpeakerCardProps {
  speaker: Speaker;
  onSelect?: (speaker: Speaker) => void;
}

export const SpeakerCard: React.FC<SpeakerCardProps> = ({ speaker, onSelect }) => {
  return (
    <div
      onClick={() => onSelect?.(speaker)}
      className="bg-white border-2 border-neutral-200 rounded-xl p-8 hover:shadow-xl hover:border-blue-300 transition-all cursor-pointer transform hover:scale-105 duration-200"
    >
      {speaker.relevance_score && (
        <div className="mb-4 flex items-center justify-between">
          <span className="text-xs font-bold text-neutral-500 uppercase tracking-wide">Match Score</span>
          <span className="bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 text-sm font-bold px-4 py-2 rounded-full">
            {speaker.relevance_score.toFixed(0)}%
          </span>
        </div>
      )}

      <h3 className="text-2xl font-bold text-neutral-900 mb-3">
        {speaker.first_name} {speaker.last_name}
      </h3>

      <p className="text-neutral-600 text-base mb-6 line-clamp-3">{speaker.biography}</p>

      <div className="space-y-4">
        {speaker.expertise.length > 0 && (
          <div>
            <p className="text-xs font-bold text-neutral-600 mb-2 uppercase tracking-wide">Expertise</p>
            <div className="flex flex-wrap gap-2">
              {speaker.expertise.slice(0, 4).map((exp) => (
                <span key={exp} className="bg-blue-100 text-blue-700 text-sm font-medium px-3 py-1 rounded-lg">
                  {exp}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="flex items-center gap-3 text-base text-neutral-700 font-medium">
          <Globe size={20} className="text-blue-600 flex-shrink-0" />
          <span>{speaker.geography.join(', ')}</span>
        </div>

        <div className="flex items-center gap-3 text-base text-neutral-700 font-medium">
          <Users size={20} className="text-blue-600 flex-shrink-0" />
          <span>{speaker.audience_types.join(', ')}</span>
        </div>

        <div className="flex flex-wrap gap-2">
          {speaker.languages.map((lang) => (
            <span key={lang} className="text-sm font-medium bg-neutral-100 text-neutral-700 px-3 py-2 rounded-lg">
              {lang}
            </span>
          ))}
        </div>
      </div>

      <button className="w-full mt-6 bg-gradient-to-r from-blue-600 to-blue-500 text-white font-bold py-3 rounded-lg hover:from-blue-700 hover:to-blue-600 transition-all shadow-md hover:shadow-lg">
        View Profile →
      </button>
    </div>
  );
};
