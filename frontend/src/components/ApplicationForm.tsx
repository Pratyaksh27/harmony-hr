import { useState } from 'react';
import '../App.css'; // reuse existing styles

function ApplicationForm() {
  const [employeeId, setEmployeeId] = useState('');
  const [otherPartyId, setOtherPartyId] = useState('');
  const [witnessId, setWitnessId] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Submitting case:', { employeeId, otherPartyId, witnessId });
    // TODO: call backend API

    const payload = {
      employee_id: employeeId,
      other_party_id: otherPartyId,
      witness_id: witnessId || null
    };

    try{
      const response = await fetch('http://localhost:8000/start_dispute_resolution', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Failed to start dispute resolution process');
      }

      const data = await response.json();
      console.log('Dispute started successfully:', data);
    } catch (error) {
      console.error('Error submitting case:', error);
      alert(`Error starting dispute resolution process. Please try again. ${error}`);
    }
  };

  return (
    <form className="form-card" onSubmit={handleSubmit}>
      <label>
        Your Employee ID<span className="required">*</span>:
        <input
          type="text"
          value={employeeId}
          onChange={(e) => setEmployeeId(e.target.value)}
          required
        />
      </label>

      <label>
        Other Party's Employee ID<span className="required">*</span>:
        <input
          type="text"
          value={otherPartyId}
          onChange={(e) => setOtherPartyId(e.target.value)}
          required
        />
      </label>

      <label>
        Witness' Employee ID (Optional):
        <input
          type="text"
          value={witnessId}
          onChange={(e) => setWitnessId(e.target.value)}
        />
      </label>

      <button type="submit">Start Case</button>
    </form>
  );
}

export default ApplicationForm;
