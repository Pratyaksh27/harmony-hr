from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from agents.orchestrator import ( 
    orchestrate_dispute_resolution, get_or_create_orchestrator_agent, 
    EmployeeDisputeResolutionRequest
)
from agents.hr_agent import run_hr_agent
from utils.report_context import start_report_context


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
    print(f"🔊 [Main] Starting dispute resolution for employee {dispute_request.employee_id}")
    try:
        context = start_report_context()
        report_id = context["report_id"]
        thread_id = context["thread_id"]
        # Call the orchestrator agent to handle the dispute resolution
        orchestrator_task = asyncio.create_task(
            orchestrate_dispute_resolution(
                dispute_request=dispute_request,
                report_id=report_id,
                thread_id=thread_id
            )
        )

        hr_task = asyncio.create_task(
            run_hr_agent(
                dispute_request=dispute_request,
                report_id=report_id,
                thread_id=thread_id,
            )
        )

        await asyncio.gather(orchestrator_task, hr_task)
        
        return {
            "status":"starting",
            "report_id": report_id,
            "thread_id": thread_id,
        }
    except Exception as e:
        return {"error": str(e)}
    