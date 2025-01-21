from datetime import datetime, timezone

def timestamp_now() -> float:
    now = datetime.now(timezone.utc)
    return now.timestamp()

def date_from_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts)
