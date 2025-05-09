from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.orchestrator import ( 
    orchestrate_dispute_resolution, get_or_create_orchestrator_agent, 
    EmployeeDisputeResolutionRequest
)


app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check point
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/start_dispute_resolution")
async def start_dispute_resolution(dispute_request: EmployeeDisputeResolutionRequest):
    """
    Endpoint to start the dispute resolution process.
    """
    try:
        # Call the orchestrator agent to handle the dispute resolution
        result = await orchestrate_dispute_resolution(dispute_request)
        return result
    except Exception as e:
        return {"error": str(e)}
    return {"status": "failed"}