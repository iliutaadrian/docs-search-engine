"use client"
import { Search } from '@/components/search';
import { indexDocs } from '@/lib/search';
import { useEffect } from 'react';

export default function Home() {
  useEffect(() => {
    indexDocs();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center pt-12 px-4">
      <h1 className="text-6xl font-bold mb-8">
        <span className="text-orange-500">GG</span> Docs
      </h1>
      <div className="w-full max-w-2xl">
        <Search />
      </div>
    </div>
  );
}