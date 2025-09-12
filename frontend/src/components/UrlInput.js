// src/components/UrlInput.js
import React, { useState } from 'react';

export default function UrlInput({ onAnalyze, isLoading }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url) {
      onAnalyze(url);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl">
      <div className="flex flex-col md:flex-row w-full gap-2">
        <div className="flex-grow">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter a YouTube or video URL..."
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
            required
          />
        </div>
        <button
          type="submit"
          disabled={isLoading || !url}
          className="px-6 py-3 bg-blue-600 rounded-lg font-semibold hover:bg-blue-500 transition-colors disabled:bg-gray-700 disabled:text-gray-400"
        >
          Analyze
        </button>
      </div>
    </form>
  );
}
