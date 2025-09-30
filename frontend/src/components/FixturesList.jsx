// frontend/src/components/FixturesList.jsx
import React from 'react';

const formatDate = (dateString) => {
    const options = { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

const FixturesList = ({ fixtures }) => {
  // Create a safe, guaranteed array.
  const fixturesList = Array.isArray(fixtures) ? fixtures : [];

  return (
    <div className="info-card">
      <h3>Upcoming Fixtures</h3>
      <ul className="list-container">
        {/* Check the length of our guaranteed array */}
        {fixturesList.length === 0 ? (
          <li className="list-item-placeholder">No upcoming fixtures scheduled.</li>
        ) : (
          // Safely map over the guaranteed array
          fixturesList.map((match) => (
            <li key={match.id} className="list-item match-item">
                <span>{match.home_team.name} vs {match.away_team.name}</span>
                <span className="match-date">{formatDate(match.match_date)}</span>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default FixturesList;