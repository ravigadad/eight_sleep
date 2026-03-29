"""Sensor platform for Eight Sleep."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import EightSleepCoordinator
from .entity import EightSleepEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Eight Sleep sensors."""
    coordinator: EightSleepCoordinator = entry.runtime_data
    async_add_entities([NextAlarmSensor(coordinator)])


class NextAlarmSensor(EightSleepEntity, SensorEntity):
    """Sensor showing the next alarm time."""

    _attr_name = "Next alarm"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator: EightSleepCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.session.user_id}_next_alarm"

    @property
    def native_value(self) -> datetime | None:
        """Return the next alarm timestamp."""
        alarms = self.coordinator.data
        if not alarms:
            return None

        upcoming = [a for a in alarms if a.enabled and a.next_timestamp]
        if not upcoming:
            return None

        soonest = min(upcoming, key=lambda a: a.next_timestamp)
        return soonest.next_timestamp
