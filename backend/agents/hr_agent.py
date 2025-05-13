from utils.openai_client import client
from agents.orchestrator import EmployeeDisputeResolutionRequest

async def run_hr_agent(dispute_request:EmployeeDisputeResolutionRequest, report_id: str, thread_id: str):
    print(f"🔊 [HR Agent] Would connect employee for report {report_id} on thread {thread_id}", flush=True)