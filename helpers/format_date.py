from datetime import datetime, timedelta, timezone


def format_time_ago(date: datetime):
    date = date.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    difference = now - date

    if difference >= timedelta(days=1):
        return f"{difference.days}d"
    else:
        return date.strftime("%I:%M %p")
