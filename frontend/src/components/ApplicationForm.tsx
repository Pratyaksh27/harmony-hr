import { useState } from 'react';
import '../App.css'; // reuse existing styles
import { startDisputeResolution } from '../api/startDispute';

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

    try {
      const response = await startDisputeResolution(payload);
      console.log('Case started successfully:', response);
    } catch (error) {
      console.error('ApplicationFrom.ts: Error starting case:', error);
      alert('ApplicationFrom.ts: Failed to start case. Please try again.');
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
