// frontend/src/components/ResultsList.jsx
import React from 'react';

const ResultsList = ({ results }) => {
  // Create a safe, guaranteed array.
  const resultsList = Array.isArray(results) ? results : [];

  return (
    <div className="info-card">
      <h3>Recent Results</h3>
      <ul className="list-container">
        {/* Check the length of our guaranteed array */}
        {resultsList.length === 0 ? (
          <li className="list-item-placeholder">No recent results available.</li>
        ) : (
          // Safely map over the guaranteed array
          resultsList.map((match) => (
            <li key={match.id} className="list-item match-item">
                <span>{match.home_team.name}</span>
                <strong className="match-score">{match.home_score} - {match.away_score}</strong>
                <span>{match.away_team.name}</span>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default ResultsList;