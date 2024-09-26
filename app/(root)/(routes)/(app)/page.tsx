"use client";
import { useState } from 'react';
import { Search } from 'lucide-react';
import Link from 'next/link';

const hardcodedResults = [
  { 
    title: "GG Documentation Overview", 
    content: "Comprehensive guide to Golf Genius software features and functionality.",
    url: "/docs/gg-overview" 
  },
  { 
    title: "Setting Up Tournaments", 
    content: "Step-by-step instructions for creating and managing golf tournaments in GG.",
    url: "/docs/tournament-setup" 
  },
  { 
    title: "Scorekeeping with GG", 
    content: "Learn how to efficiently manage scores and leaderboards for your golf events.",
    url: "/docs/scorekeeping" 
  },
  { 
    title: "GG Mobile App Guide", 
    content: "Explore the features and benefits of the Golf Genius mobile application.",
    url: "/docs/mobile-app" 
  },
];

export default function Page() {
  const [searchQuery, setSearchQuery] = useState('');
  const [showResults, setShowResults] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setShowResults(true);
  };

  const highlightSearchTerm = (text: string, searchTerm: string) => {
    if (!searchTerm) return text;
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.split(regex).map((part, index) => 
      regex.test(part) ? <span key={index} className="bg-orange-500 text-white">{part}</span> : part
    );
  };

  return (
    <div className="min-h-screen text-white flex flex-col items-center pt-12 px-4">
      <h1 className="text-6xl font-bold mb-8">
        <span className="text-orange-500">GG</span> Docs
      </h1>

      <form onSubmit={handleSearch} className="w-full max-w-2xl mb-8 relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search documentation"
          className="w-full py-3 px-4 pr-12 text-lg bg-gray-800 border border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-orange-500 text-white placeholder-gray-400"
        />
        <button type="submit" className="absolute right-3 top-1/2 transform -translate-y-1/2">
          <Search className="h-6 w-6 text-gray-400" />
        </button>
      </form>

      {showResults && (
        <div className="w-full max-w-2xl">
          <h2 className="text-lg font-semibold mb-4 text-orange-500">Search Results:</h2>
          <ul className="space-y-6">
            {hardcodedResults.map((result, index) => (
              <li key={index} className="bg-gray-800 p-4 rounded-lg">
                <Link href={result.url} className="text-orange-500 hover:underline text-lg font-semibold">
                  {highlightSearchTerm(result.title, searchQuery)}
                </Link>
                <p className="text-gray-300 mt-2">
                  {highlightSearchTerm(result.content, searchQuery)}
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}

      <footer className="mt-auto py-4">
        <Link href="/about" className="text-sm text-gray-400 hover:text-white">About</Link>
      </footer>
    </div>
  );
}