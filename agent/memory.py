import json
import os
from datetime import datetime
from typing import Dict

# Store memory in project root /agent_memory/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(BASE_DIR, "..", "agent_memory")
MEMORY_FILE = os.path.join(MEMORY_DIR, "events.jsonl")

# Ensure directory exists
os.makedirs(MEMORY_DIR, exist_ok=True)

def store_event(event: Dict):
    """
    Append an event to agent memory (JSONL).
    """
    event["stored_at"] = datetime.utcnow().isoformat()

    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def load_events(limit: int = 10):
    """
    Load last N events from memory.
    """
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    events = [json.loads(line) for line in lines[-limit:]]
    return events
