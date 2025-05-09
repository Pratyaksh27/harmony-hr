
export interface DisputeResolutionPayload {
    employee_id: string;
    other_party_id: string;
    witness_id: string | null;
  }

  
export async function startDisputeResolution(payload: DisputeResolutionPayload) {
    const apiUrl = import.meta.env.VITE_API_URL;

    const response = await fetch(`${apiUrl}/start_dispute_resolution`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    if(!response.ok) {
        const errorText = await response.text();
        throw new Error(`startDispute.ts : Failed to start dispute resolution process ${response.status}: ${errorText}`);
    }

    return await response.json();
}