from datetime import datetime, timezone


class TimeMethodsMixin:
    _SERVER_TIMEZONE = timezone.utc

    def get_current_time(self) -> datetime:
        """Get current time in Server Timezone (UTC)."""
        return datetime.now(self._SERVER_TIMEZONE)

    def get_current_time_iso(self) -> str:
        """Get current time in Server Timezone (UTC) and ISO format."""
        return self.get_current_time().isoformat()

    def get_time_from_timestamp(self, timestamp: int) -> datetime:
        """Get datetime from timestamp in Server Timezone (UTC)."""
        return datetime.fromtimestamp(timestamp, tz=self._SERVER_TIMEZONE)
