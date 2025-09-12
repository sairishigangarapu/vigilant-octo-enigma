// src/components/ReportCard.js
import React from 'react';

export default function ReportCard({ data }) {
  if (!data || !data.report) return null;

  const isFactCheck = data.source === 'Google Fact-Check Database';
  const report = data.report;

  // Helper function to render risk level badge
  const renderRiskBadge = (riskLevel) => {
    const colors = {
      'Low Risk': 'bg-green-600',
      'Medium Risk': 'bg-yellow-600',
      'High Risk': 'bg-red-600'
    };
    
    return (
      <span className={`${colors[riskLevel] || 'bg-gray-600'} text-white px-3 py-1 rounded-full text-sm font-medium`}>
        {riskLevel}
      </span>
    );
  };

  return (
    <div className="mt-8 w-full max-w-4xl bg-gray-800 rounded-lg p-6 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">
          {isFactCheck ? 'Fact-Check Result' : 'Vigil AI Analysis'}
        </h2>
        {!isFactCheck && report.risk_level && renderRiskBadge(report.risk_level)}
      </div>
      
      {isFactCheck ? (
        // Render Google Fact Check result
        <div>
          <div className="bg-gray-700 p-4 rounded-lg mb-4">
            <h3 className="font-bold mb-2">Claim</h3>
            <p>{report.text || 'No claim text available'}</p>
            
            {report.claimant && (
              <p className="mt-2 text-gray-400">
                Claimed by: <span className="text-white">{report.claimant}</span>
              </p>
            )}
          </div>
          
          {report.rating && (
            <div className="bg-gray-700 p-4 rounded-lg mb-4">
              <h3 className="font-bold mb-2">Rating</h3>
              <div className="flex items-center">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  report.rating.toLowerCase().includes('false') ? 'bg-red-600' : 
                  report.rating.toLowerCase().includes('true') ? 'bg-green-600' : 'bg-yellow-600'
                }`}>
                  {report.rating}
                </span>
              </div>
            </div>
          )}
          
          {report.url && (
            <div className="mt-4">
              <a 
                href={report.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300"
              >
                Read the full fact-check →
              </a>
            </div>
          )}
        </div>
      ) : (
        // Render Gemini Analysis result
        <div>
          {report.summary && (
            <div className="bg-gray-700 p-4 rounded-lg mb-4">
              <h3 className="font-bold mb-2">Summary</h3>
              <p>{report.summary}</p>
            </div>
          )}
          
          {report.context_check && (
            <div className="bg-gray-700 p-4 rounded-lg mb-4">
              <h3 className="font-bold mb-2">Context Check</h3>
              <div className="flex items-center mb-2">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  report.context_check.status.includes('No') ? 'bg-yellow-600' : 'bg-blue-600'
                }`}>
                  {report.context_check.status}
                </span>
              </div>
              <p>{report.context_check.details}</p>
            </div>
          )}
          
          {report.claim_verification && (
            <div className="bg-gray-700 p-4 rounded-lg mb-4">
              <h3 className="font-bold mb-2">Claim Verification</h3>
              <div className="flex items-center mb-2">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  report.claim_verification.status.toLowerCase().includes('corroborated') ? 'bg-green-600' : 
                  report.claim_verification.status.toLowerCase().includes('refuted') ? 'bg-red-600' : 'bg-yellow-600'
                }`}>
                  {report.claim_verification.status}
                </span>
              </div>
              <p>{report.claim_verification.details}</p>
            </div>
          )}
          
          {report.visual_red_flags && report.visual_red_flags.length > 0 && (
            <div className="bg-gray-700 p-4 rounded-lg">
              <h3 className="font-bold mb-2">Visual Red Flags</h3>
              <ul className="list-disc pl-5 space-y-1">
                {report.visual_red_flags.map((flag, index) => (
                  <li key={index}>{flag}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
