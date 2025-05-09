import os
import time
import uuid
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ORCHESTRATOR_AGENT_CACHE_FILE = "orchestrator_assistant_cache.json"

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
    # Simulate connecting to the HR voice agent
    print(f"Connecting employee {employee_id} to HR voice agent for report {report_id}...")
    # Here implement the actual connection logic
    return f"Connected employee {employee_id} to HR voice agent for report {report_id}."


# ---------------------------
# 3. Register or Load Assistant
# ---------------------------
def get_or_create_orchestrator_agent():
    if os.path.exists(ORCHESTRATOR_AGENT_CACHE_FILE):
        with open(ORCHESTRATOR_AGENT_CACHE_FILE, "r") as f:
            return json.load(f)["orchestrator_agent_id"]
    orchestrator_agent = client.beta.assistants.create(
        name="Orchestrator",
        description="An assistant that orchestrates the dispute resolution process. When given a report ID and employee IDs," \
        "it will connect the requesting employee to the voice HR agent",
        model="gpt-4-turbo",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "connect_to_hr_voice_agent",
                    "description": "Connects the employee to the HR voice agent for dispute resolution.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "report_id": {
                                "type": "string",
                                "description": "The report ID for the dispute resolution.",
                            },
                            "employee_id": {
                                "type": "string",
                                "description": "The employee ID to connect to the HR voice agent.",
                            },
                        },
                        "required": ["report_id", "employee_id"],
                    },
                },
            },
        ],
    )
    with open(ORCHESTRATOR_AGENT_CACHE_FILE, "w") as f:
        json.dump({"orchestrator_agent_id": orchestrator_agent.id}, f)
    
    return orchestrator_agent.id

# ---------------------------
# 4. Main Orchestration Logic
# ---------------------------
async def orchestrate_dispute_resolution(dispute_request: EmployeeDisputeResolutionRequest):
    # Get or create the orchestrator agent
    orchestrator_agent_id = get_or_create_orchestrator_agent()
    # Create a unique conversation ID for this dispute resolution
    report_id = str(uuid.uuid4())

    orchestrator_thread = client.beta.threads.create()
    
    client.beta.threads.messages.create(
        thread_id=orchestrator_thread.id,
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
        thread_id=orchestrator_thread.id,
    )

    # Wait for the orchestrator agent to finish processing
    while True:
        run_status = client.beta.threads.runs.retrieve(orchestrator_run.id, thread_id=orchestrator_thread.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            raise Exception("Orchestrator agent failed to process the request.")
        elif run_status.status == "requires_action":
            break
        time.sleep(1)
    print(f"Orchestrator run status: {run_status.status}")
        
    tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
    tool_outputs = []

    for call in tool_calls:
        if call.function.name == "connect_to_hr_voice_agent":
            args = json.loads(call.function.arguments)
            result = connect_to_hr_voice_agent(report_id, args["employee_id"])
            tool_outputs.append(result)

    return {
        "report_id": report_id,
        "thread_id": orchestrator_thread.id,
        "orchestrator_run_id": orchestrator_run.id,
        "employee_id": dispute_request.employee_id,
        "other_party_id": dispute_request.other_party_id,
        "witness_id": dispute_request.witness_id,
        "tool_outputs": tool_outputs,
        "status": "completed",
        "message": "Connected to HR voice agent successfully.",
    }
