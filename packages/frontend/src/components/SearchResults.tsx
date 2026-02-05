import React, { useState } from 'react';
import { SpeakerCard } from './SpeakerCard';
import { Speaker, SearchQuery } from '../services';

interface SearchResultsProps {
  speakers: Speaker[];
  total: number;
  loading: boolean;
  onSpeakerSelect: (speaker: Speaker) => void;
  onLoadMore?: () => void;
}

export const SearchResults: React.FC<SearchResultsProps> = ({
  speakers,
  total,
  loading,
  onSpeakerSelect,
  onLoadMore,
}) => {
  if (loading && speakers.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p className="text-xl text-neutral-600 font-medium">Searching speakers...</p>
      </div>
    );
  }

  if (speakers.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="text-5xl mb-4">🔍</div>
        <p className="text-xl text-neutral-600 font-medium">No speakers found</p>
        <p className="text-neutral-500 mt-2">Try a different search or adjust your filters</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-lg text-neutral-700 font-semibold">
        Found <span className="text-blue-600 text-2xl font-bold">{total}</span> speaker{total !== 1 ? 's' : ''}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {speakers.map((speaker) => (
          <SpeakerCard key={speaker.id} speaker={speaker} onSelect={onSpeakerSelect} />
        ))}
      </div>

      {speakers.length < total && (
        <div className="pt-4">
          <button
            onClick={onLoadMore}
            disabled={loading}
            className="w-full py-4 px-6 border-2 border-blue-600 text-blue-600 font-bold text-lg rounded-lg hover:bg-blue-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Loading more speakers...' : `Load More (${speakers.length}/${total})`}
          </button>
        </div>
      )}
    </div>
  );
};
