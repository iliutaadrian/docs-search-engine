"use client"
import React, { useState, useCallback } from 'react';
import { search, SearchResult } from '../lib/search';

export function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);

  const handleSearch = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    const searchResults = search(query);
    setResults(searchResults);
  }, [query]);

  return (
    <div>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search documentation"
          className="w-full py-3 px-4 pr-12 text-lg bg-gray-800 border border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-orange-500 text-white placeholder-gray-400"
        />
        <button type="submit" className="mt-2 px-4 py-2 bg-orange-500 text-white rounded-full">
          Search
        </button>
      </form>
      <div className="mt-4">
        {results.map((result, index) => (
          <div key={index} className="mb-4 p-4 bg-gray-800 rounded-lg">
            <h3 className="text-xl font-semibold text-orange-500">{result.title}</h3>
            <p className="mt-2 text-gray-300" dangerouslySetInnerHTML={{ __html: result.highlight }} />
          </div>
        ))}
      </div>
    </div>
  );
}