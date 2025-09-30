// frontend/src/components/StandingsTable.jsx
import React from 'react';
import TeamForm from './TeamForm';

const StandingsTable = ({ standings }) => {
  if (!standings || !standings.length) {
    return (
      <div className="standings-container">
        <p>Loading standings or no teams available.</p>
      </div>
    );
  }

  return (
    <div className="standings-container">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th className="logo-header"></th>
            <th>Team</th>
            <th>Captain</th>
            <th>MP</th>
            <th>W</th>
            <th>D</th>
            <th>L</th>
            <th>GF</th>
            <th>GA</th>
            <th>GD</th>
            <th>Pts</th>
            <th>Form</th>
          </tr>
        </thead>
        <tbody>
          {standings.map((team, index) => (
            <tr key={team.id}>
            <td className="logo-cell">
        {team.logo ? (
            <img 
                // THE FIX IS HERE: Use the environment variable
                src={`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}${team.logo}`} 
                alt={team.name} 
                className="team-logo" 
            />
        ) : (
            <div className="team-logo-placeholder"></div>
        )}
    </td>
              <td className="team-name-cell">{team.name}</td>
              <td className="captain-name">
                {team.captain ? `${team.captain.first_name} ${team.captain.last_name}` : 'N/A'}
              </td>
              <td>{team.matches_played}</td>
              <td>{team.wins}</td>
              <td>{team.draws}</td>
              <td>{team.losses}</td>
              <td>{team.goals_for}</td>
              <td>{team.goals_against}</td>
              <td>{team.goal_difference}</td>
              <td><strong>{team.points}</strong></td>
              <td>
                <TeamForm teamId={team.id} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StandingsTable;