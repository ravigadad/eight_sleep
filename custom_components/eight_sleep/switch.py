"""Switch platform for Eight Sleep."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import EightSleepCoordinator
from .entity import EightSleepAlarmEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Eight Sleep switches."""
    coordinator: EightSleepCoordinator = entry.runtime_data
    known_ids: set[str] = set()

    @callback
    def _async_add_new_alarms() -> None:
        current_ids = {a.id for a in coordinator.data}
        new_ids = current_ids - known_ids
        if new_ids:
            known_ids.update(new_ids)
            async_add_entities(
                AlarmEnabledSwitch(coordinator, alarm_id)
                for alarm_id in new_ids
            )

    _async_add_new_alarms()
    entry.async_on_unload(coordinator.async_add_listener(_async_add_new_alarms))


class AlarmEnabledSwitch(EightSleepAlarmEntity, SwitchEntity):
    """Switch to enable/disable an alarm."""

    _attr_name = "Enabled"

    def __init__(self, coordinator: EightSleepCoordinator, alarm_id: str) -> None:
        super().__init__(coordinator, alarm_id)
        self._attr_unique_id = f"{alarm_id}_enabled"

    @property
    def is_on(self) -> bool | None:
        alarm = self._alarm
        return alarm.enabled if alarm else None

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._alarm.enable()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._alarm.disable()
        await self.coordinator.async_request_refresh()
