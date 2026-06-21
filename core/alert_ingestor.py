def parse_alert_to_goal(alert_text):
    # Simple heuristic parser: if user adds an explicit goal line, use it
    if isinstance(alert_text, str) and "Add goal:" in alert_text:
        try:
            return alert_text.split("Add goal:", 1)[1].strip()
        except Exception:
            pass

    # Otherwise, synthesize a concise investigative goal
    short = alert_text
    if isinstance(short, str) and len(short) > 120:
        short = short[:117] + "..."
    return f"Investigate alert: {short}"


def parse_alert_payload(alert_payload, source="generic"):
    if isinstance(alert_payload, dict):
        if source.lower() == "prometheus":
            return alert_payload.get("message") or alert_payload.get("summary") or str(alert_payload)
        if source.lower() == "pagerduty":
            event = alert_payload.get("event", {})
            return event.get("summary") or event.get("description") or str(alert_payload)
        if source.lower() == "datadog":
            return alert_payload.get("title") or alert_payload.get("text") or str(alert_payload)
        if "alerts" in alert_payload and isinstance(alert_payload["alerts"], list):
            top = alert_payload["alerts"][0]
            return top.get("annotations", {}).get("description") or top.get("annotations", {}).get("summary") or str(top)
        if "summary" in alert_payload:
            return alert_payload.get("summary")
        if "message" in alert_payload:
            return alert_payload.get("message")
        if "title" in alert_payload:
            return alert_payload.get("title")
    return str(alert_payload)


def ingest_alert(system, alert_text, priority=7):
    if isinstance(alert_text, dict):
        alert_text = parse_alert_payload(alert_text)

    goal_text = parse_alert_to_goal(alert_text)
    try:
        system.kernel.add_goal(goal_text, priority=priority)
        try:
            system.save_self_model()
        except Exception:
            pass
        return {"status": "ok", "goal": goal_text}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def ingest_structured_alert(system, source, payload, priority=7):
    alert_text = parse_alert_payload(payload, source=source)
    return ingest_alert(system, alert_text, priority=priority)
