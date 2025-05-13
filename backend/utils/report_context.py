import uuid
from utils.openai_client import client

def start_report_context():
    """
    Start a new report context
    """
    report_id = str(uuid.uuid4())
    thread = client.beta.threads.create()
    return {
        "report_id": report_id,
        "thread_id": thread.id,
    }


