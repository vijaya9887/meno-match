import React, { useState } from 'react';
import { Search, MapPin, Users, Globe, MessageSquare } from 'lucide-react';
import { speakerApi, SearchQuery } from '../services';

interface SearchBarProps {
  onSearch: (query: SearchQuery) => void;
  loading?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch, loading = false }) => {
  const [query, setQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [geography, setGeography] = useState<string[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    onSearch({
      natural_language_query: query,
      filters: geography.length > 0 ? { geography } : undefined,
      limit: 10,
      offset: 0,
    });
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-lg font-semibold text-neutral-900 mb-3">Search Query</label>
          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., 'French climate experts' or 'AI speakers for tech conference'"
              className="w-full px-5 py-4 text-lg border-2 border-neutral-200 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-colors"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-blue-600 to-blue-500 text-white p-3 rounded-lg hover:from-blue-700 hover:to-blue-600 transition-all disabled:opacity-50"
              title="Search"
            >
              <Search size={24} />
            </button>
          </div>
        </div>

        <button
          type="button"
          onClick={() => setShowFilters(!showFilters)}
          className="inline-flex items-center gap-2 px-5 py-2 text-base font-semibold text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
        >
          {showFilters ? '▼' : '▶'} Advanced Filters
        </button>

        {showFilters && (
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-6 rounded-xl border border-blue-100 space-y-4">
            <div>
              <label className="block text-base font-semibold text-neutral-900 mb-3">Geography</label>
              <div className="flex flex-wrap gap-3">
                {['France', 'India', 'Brazil', 'UK', 'Japan', 'Global'].map((geo) => (
                  <button
                    key={geo}
                    type="button"
                    onClick={() =>
                      setGeography(
                        geography.includes(geo)
                          ? geography.filter((g) => g !== geo)
                          : [...geography, geo]
                      )
                    }
                    className={`px-4 py-2 rounded-lg font-medium text-base transition-all ${
                      geography.includes(geo)
                        ? 'bg-blue-600 text-white shadow-md hover:bg-blue-700'
                        : 'bg-white border-2 border-blue-200 text-neutral-700 hover:border-blue-400'
                    }`}
                  >
                    {geo}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </form>
    </div>
  );
};
