from datetime import datetime, timezone
from pathlib import Path

def file_last_modification_date(filename: str) -> datetime.timestamp:
    path = Path(filename)
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)