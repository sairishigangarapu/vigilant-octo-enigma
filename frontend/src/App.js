// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import UrlInput from './components/UrlInput';
import LoadingIndicator from './components/LoadingIndicator';
import ReportCard from './components/ReportCard';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async (url) => {
    setIsLoading(true);
    setReportData(null);
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        video_url: url,
      });
      setReportData(response.data);
    } catch (err) {
      setError('Analysis failed. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen flex flex-col items-center p-8 font-sans">
      <h1 className="text-5xl font-bold mb-2">Vigil AI <span className="text-blue-400">Lite</span></h1>
      <p className="text-gray-400 mb-8">Your co-pilot for navigating the truth in video.</p>
      <UrlInput onAnalyze={handleAnalyze} isLoading={isLoading} />
      {isLoading && <LoadingIndicator />}
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {reportData && <ReportCard data={reportData} />}
    </div>
  );
}

export default App;
