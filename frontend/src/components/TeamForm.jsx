// frontend/src/components/TeamForm.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TeamForm = ({ teamId }) => {
  const [form, setForm] = useState([]);

   useEffect(() => {
        if (!teamId) return;

        const fetchForm = async () => {
          try {
            // THE FIX IS HERE: Use the environment variable
            const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
            const response = await axios.get(`${baseUrl}/api/teams/${teamId}/form/`);
            setForm(response.data);
          } catch (error) {
            console.error(`Error fetching form for team ${teamId}:`, error);
          }
        };

        fetchForm();
    }, [teamId]);

  // Helper function to get the right CSS class for each result
  const getFormClass = (result) => {
    if (result === 'W') return 'form-win';
    if (result === 'D') return 'form-draw';
    if (result === 'L') return 'form-loss';
    return '';
  };

  return (
    <div className="form-container">
      {form.map((result, index) => (
        <div key={index} className={`form-box ${getFormClass(result)}`}>
          {result}
        </div>
      ))}
    </div>
  );
};

export default TeamForm;