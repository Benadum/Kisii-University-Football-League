// frontend/src/App.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

import StandingsTable from './components/StandingsTable';
import TopScorersList from './components/TopScorersList';
import FixturesList from './components/FixturesList';
import ResultsList from './components/ResultsList';

function App() {
  const [standings, setStandings] = useState([]);
  const [scorers, setScorers] = useState([]);
  const [fixtures, setFixtures] = useState([]);
  const [results, setResults] = useState([]);
  const [theme, setTheme] = useState('light');

  // DEBUG [1]: LOGGING THE STATE ON EVERY RENDER
  // This will show us if the 'standings' state ever changes from an empty array.
  console.log("Component Rendered. Current standings state:", standings);

   useEffect(() => {
        const fetchData = async () => {
          try {
            // THE FIX IS HERE: Use the environment variable for all URLs
            const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

            const standingsReq = axios.get(`${baseUrl}/api/standings/`);
            const scorersReq = axios.get(`${baseUrl}/api/top-scorers/`);
            const fixturesReq = axios.get(`${baseUrl}/api/fixtures/`);
            const resultsReq = axios.get(`${baseUrl}/api/results/`);
        const [standingsRes, scorersRes, fixturesRes, resultsRes] = await Promise.all([
          standingsReq,
          scorersReq,
          fixturesReq,
          resultsReq,
        ]);

        // DEBUG [2]: LOGGING THE DATA RECEIVED FROM THE API
        // This will show us the exact data that came back from the server.
        console.log("API call successful. Data received:", standingsRes.data);

        // This is where the state should be updated.
        setStandings(standingsRes.data);
        setScorers(scorersRes.data);
        setFixtures(fixturesRes.data);
        setResults(resultsRes.data);

      } catch (error) {
        // DEBUG [3]: LOGGING ANY ERROR THAT OCCURS
        console.error("CRITICAL ERROR in fetchData:", error);
      }
    };

    fetchData();
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
  };

  return (
    <div className={`app-container ${theme}`}>
      <button onClick={toggleTheme} className="theme-toggle-button">
        Toggle {theme === 'light' ? 'Dark' : 'Light'} Mode
      </button>
      
      <h1>Kisii University Premier League</h1>

      <div className="main-layout">
        <main>
          {/* We are passing the 'standings' state to the 'standings' prop */}
          <StandingsTable standings={standings} />
        </main>
        <aside className="sidebar">
          <TopScorersList scorers={scorers} />
          <FixturesList fixtures={fixtures} />
          <ResultsList results={results} />
        </aside>
      </div>
    </div>
  );
}

export default App;