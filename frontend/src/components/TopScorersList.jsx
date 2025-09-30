// frontend/src/components/TopScorersList.jsx
import React from 'react';

// We will still expect a 'scorers' prop
const TopScorersList = ({ scorers }) => {
  
  // Create a safe, guaranteed array.
  // If 'scorers' is a valid array, use it. Otherwise, use an empty array.
  const scorersList = Array.isArray(scorers) ? scorers : [];

  return (
    <div className="info-card">
      <h3>Top Scorers</h3>
      <ol className="list-container">
        {/* Now, we only check the length of our guaranteed array */}
        {scorersList.length === 0 ? (
          <li className="list-item-placeholder">No scorers yet.</li>
        ) : (
          // We can now safely map over scorersList
          scorersList.map((player, index) => (
            <li key={player.id} className="list-item">
              <span>
                <strong>{index + 1}. {player.first_name} {player.last_name}</strong> 
                {player.team && ` (${player.team.name})`}
              </span>
              <span>{player.goals}</span>
            </li>
          ))
        )}
      </ol>
    </div>
  );
};

export default TopScorersList;