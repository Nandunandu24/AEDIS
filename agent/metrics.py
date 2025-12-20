from datetime import datetime
from typing import List, Dict

def sla_metrics(events: List[Dict]) -> Dict:
    """
    Computes SLA statistics from stored agent events.
    """

    if not events:
        return {
            "total_cases": 0,
            "sla_breach_rate": "0%"
        }

    total = len(events)
    breached = 0

    for event in events:
        sla = event.get("sla")
        if sla and sla.get("breached"):
            breached += 1

    breach_rate = round((breached / total) * 100, 2)

    return {
        "total_cases": total,
        "sla_breach_rate": f"{breach_rate}%"
    }
