"""Base entities for Eight Sleep."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from eight_sleep_client.models.alarm import Alarm

from .const import DOMAIN
from .coordinator import EightSleepCoordinator


class EightSleepEntity(CoordinatorEntity[EightSleepCoordinator]):
    """Base entity for the Eight Sleep Pod device."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: EightSleepCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.session.user_id)},
            name="Eight Sleep Pod",
            manufacturer="Eight Sleep",
        )


class EightSleepAlarmEntity(CoordinatorEntity[EightSleepCoordinator]):
    """Base entity for an individual alarm device."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: EightSleepCoordinator, alarm_id: str) -> None:
        super().__init__(coordinator)
        self._alarm_id = alarm_id
        alarm = self._alarm
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, alarm_id)},
            name=self._device_name(alarm),
            manufacturer="Eight Sleep",
            via_device=(DOMAIN, coordinator.session.user_id),
        )

    @property
    def _alarm(self) -> Alarm | None:
        """Find this alarm in the coordinator's current data."""
        for alarm in self.coordinator.data:
            if alarm.id == self._alarm_id:
                return alarm
        return None

    @staticmethod
    def _device_name(alarm: Alarm) -> str:
        """Generate a human-readable device name from alarm data."""
        time = alarm.time[:5]  # strip seconds — "08:30:00" → "08:30"
        days = alarm.repeat.days
        if not days:
            return f"One-time {time} Alarm"
        day_set = set(days)
        weekdays = {"monday", "tuesday", "wednesday", "thursday", "friday"}
        weekends = {"saturday", "sunday"}
        if day_set == weekdays | weekends:
            return f"Daily {time} Alarm"
        if day_set == weekdays:
            return f"Weekday {time} Alarm"
        if day_set == weekends:
            return f"Weekend {time} Alarm"
        if len(days) == 1:
            return f"{days[0].capitalize()} {time} Alarm"
        return f"Multi-day {time} Alarm"
