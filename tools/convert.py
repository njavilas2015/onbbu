from datetime import datetime, timezone


def ms_to_date(value: str | int | None) -> str:
    if value is None:
        return None
    
    if isinstance(value, str):
        value = int(value)
    
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()
