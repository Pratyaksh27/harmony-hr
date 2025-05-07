import { useState } from 'react';
import '../App.css'; // reuse existing styles

function ApplicationForm() {
  const [employeeId, setEmployeeId] = useState('');
  const [otherPartyId, setOtherPartyId] = useState('');
  const [witnessId, setWitnessId] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Submitting case:', { employeeId, otherPartyId, witnessId });
    // TODO: call backend API
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
