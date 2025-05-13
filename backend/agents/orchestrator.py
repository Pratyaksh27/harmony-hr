import os
import time
import uuid
import json
# from dotenv import load_dotenv
# from openai import OpenAI
from pydantic import BaseModel
from utils.openai_client import client


ASSISTANT_CACHE_DIR = os.path.join(os.path.dirname(__file__), "agent_cache")
os.makedirs(ASSISTANT_CACHE_DIR, exist_ok=True)
# Cache file for the orchestrator agent

# ---------------------------
# 1. Input Model
# ---------------------------
class EmployeeDisputeResolutionRequest(BaseModel):
    employee_id: str
    other_party_id: str
    witness_id: str | None = None

# ---------------------------
# 2. Simulated Tool Function
# ---------------------------
def connect_to_hr_voice_agent(report_id: str, employee_id: str):
    # Simulate connecting to the HR voice agent.
    print(f"Connecting employee {employee_id} to HR voice agent for report {report_id}...")
    # Here implement the actual connection logic
    return f"Connected employee {employee_id} to HR voice agent for report {report_id}."


# ---------------------------
# 3. Register or Load Assistant
# ---------------------------
def get_or_create_orchestrator_agent():
    return get_or_create_agent(
        role="orchestrator",
        agent_config={
            "name": "Orchestrator Agent",
            "description": (
                "Orchestrates the dispute resolution process."
                "When given a report ID and employee IDs, it will connect the requesting employee to the voice HR agent."
            ),
            "model": "gpt-3.5-turbo",
            "tools": [],
        },
    )
    

# ---------------------------
# 4. Main Orchestration Logic.
# ---------------------------
async def orchestrate_dispute_resolution(dispute_request: EmployeeDisputeResolutionRequest, report_id: str, thread_id:str):
    orchestrator_agent_id = get_or_create_orchestrator_agent()
    report_id = report_id
    orchestrator_thread_id = thread_id
    
    client.beta.threads.messages.create(
        thread_id=orchestrator_thread_id,
        role="user",
        content=f"Connect employee {dispute_request.employee_id} to HR voice agent for report {report_id}.",
        metadata={
            "report_id": report_id,
            "employee_id": dispute_request.employee_id,
            "other_party_id": dispute_request.other_party_id,
            "witness_id": dispute_request.witness_id,
        },
    )

    orchestrator_run = client.beta.threads.runs.create(
        assistant_id=orchestrator_agent_id,
        thread_id=orchestrator_thread_id,
    )

    # Wait for the orchestrator agent to finish processing
    while True:
        run_status = client.beta.threads.runs.retrieve(orchestrator_run.id, thread_id=orchestrator_thread_id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            raise Exception("Orchestrator agent failed to process the request.")
        elif run_status.status == "requires_action":
            break
        time.sleep(0.5)  # Sleep for a second before checking again
    
    print(f"Orchestrator run status: {run_status.status}")

    return {
        "report_id": report_id,
        "thread_id": orchestrator_thread_id,
        "orchestrator_run_id": orchestrator_run.id,
        "employee_id": dispute_request.employee_id,
        "other_party_id": dispute_request.other_party_id,
        "witness_id": dispute_request.witness_id,
        "status": "completed",
        "message": "Connected to HR voice agent successfully.",
    }


# ------------------------------------
# 3. Register or Load a new Assistant
# ------------------------------------

def get_or_create_agent(role:str, agent_config:dict):
    """
    Get or create an assistant agent.
    """
    # Check if the agent already exists
    agent_cache_file = os.path.join(ASSISTANT_CACHE_DIR, f"{role}.json")
    if os.path.exists(agent_cache_file):
        with open(agent_cache_file, "r") as f:
            agent = json.load(f)
        print(f"Loaded {role} agent from cache.")
        return agent["assistant_id"]
    
    # Create a new agent
    agent = client.beta.assistants.create(**agent_config)
    
    # Save the assistant to the cache
    with open(agent_cache_file, "w") as f:
        json.dump({"assistant_id":agent.id}, f)
    
    return agent.id