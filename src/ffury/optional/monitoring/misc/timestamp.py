from datetime import (
    datetime,
    timedelta,
    timezone
)
from typing import Tuple

def timestamp_now_timedelta(days=1) -> Tuple[float, float]:
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=days)
    return yesterday.timestamp(), now.timestamp()

def timestamp_now() -> float:
    now = datetime.now(timezone.utc)
    return now.timestamp()

def date_from_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts)
