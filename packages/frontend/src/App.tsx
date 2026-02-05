import React, { useState } from 'react';
import { Mic } from 'lucide-react';
import { SearchBar } from './components/SearchBar';
import { SearchResults } from './components/SearchResults';
import { SpeakerProfileView } from './components/SpeakerProfileView';
import { speakerApi, Speaker, SearchQuery } from './services';
import './App.css';

function App() {
  const [speakers, setSpeakers] = useState<Speaker[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [selectedSpeaker, setSelectedSpeaker] = useState<Speaker | null>(null);
  const [currentOffset, setCurrentOffset] = useState(0);
  const [lastQuery, setLastQuery] = useState<SearchQuery | null>(null);

  const handleSearch = async (query: SearchQuery) => {
    try {
      setLoading(true);
      setCurrentOffset(0);
      const response = await speakerApi.search({ ...query, offset: 0 });
      setSpeakers(response.data.speakers);
      setTotal(response.data.total);
      setLastQuery(query);
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadMore = async () => {
    if (!lastQuery) return;
    try {
      setLoading(true);
      const newOffset = currentOffset + (lastQuery.limit || 10);
      const response = await speakerApi.search({ ...lastQuery, offset: newOffset });
      setSpeakers([...speakers, ...response.data.speakers]);
      setCurrentOffset(newOffset);
    } catch (error) {
      console.error('Load more error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (selectedSpeaker) {
    return (
      <SpeakerProfileView
        speakerId={selectedSpeaker.id}
        onBack={() => setSelectedSpeaker(null)}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-neutral-50 to-white">
      {/* Navigation Header */}
      <header className="bg-white border-b border-neutral-200 shadow-sm sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-blue-600 to-cyan-600 p-3 rounded-lg">
              <Mic size={32} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-neutral-900">Meno Match</h1>
              <p className="text-sm text-neutral-500">Expert Speaker Network</p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="mb-16 text-center max-w-3xl mx-auto">
          <h2 className="text-5xl font-bold text-neutral-900 mb-4">Find Your Perfect Speaker</h2>
          <p className="text-xl text-neutral-600 mb-2">Search our global network of expert speakers for your event</p>
          <p className="text-base text-neutral-500">Powered by intelligent matching and natural language search</p>
        </div>

        {/* Search Section */}
        <div className="bg-white rounded-xl shadow-md border border-neutral-200 p-10 mb-12">
          <SearchBar onSearch={handleSearch} loading={loading} />
        </div>

        {/* Features Info */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-xl p-8 border border-neutral-200 hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-xl font-bold text-neutral-900 mb-3">Smart Search</h3>
            <p className="text-base text-neutral-600">Natural language queries with relevance ranking to find the perfect match</p>
          </div>
          <div className="bg-white rounded-xl p-8 border border-neutral-200 hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4">🌍</div>
            <h3 className="text-xl font-bold text-neutral-900 mb-3">Global Reach</h3>
            <p className="text-base text-neutral-600">Discover speakers from around the world across all industries and expertise</p>
          </div>
          <div className="bg-white rounded-xl p-8 border border-neutral-200 hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold text-neutral-900 mb-3">Smart Filtering</h3>
            <p className="text-base text-neutral-600">Advanced filters by expertise, language, geography, and audience type</p>
          </div>
        </div>

        {/* Results Section */}
        {speakers.length > 0 || loading ? (
          <div className="bg-white rounded-xl shadow-md border border-neutral-200 p-10">
            <SearchResults
              speakers={speakers}
              total={total}
              loading={loading}
              onSpeakerSelect={setSelectedSpeaker}
              onLoadMore={handleLoadMore}
            />
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-md border border-neutral-200 p-16 text-center">
            <div className="text-6xl mb-6">🎤</div>
            <h3 className="text-2xl font-bold text-neutral-900 mb-3">Ready to find speakers?</h3>
            <p className="text-lg text-neutral-600">
              Try searching for speakers by topic, expertise, geography, or any natural language query.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
