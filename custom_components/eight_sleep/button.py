"""Button platform for Eight Sleep."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
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
    """Set up Eight Sleep buttons."""
    coordinator: EightSleepCoordinator = entry.runtime_data
    known_ids: set[str] = set()

    @callback
    def _async_add_new_alarms() -> None:
        current_ids = {a.id for a in coordinator.data}
        new_ids = current_ids - known_ids
        if new_ids:
            known_ids.update(new_ids)
            entities = []
            for alarm_id in new_ids:
                entities.append(AlarmSnoozeButton(coordinator, alarm_id))
                entities.append(AlarmDismissButton(coordinator, alarm_id))
            async_add_entities(entities)

    _async_add_new_alarms()
    entry.async_on_unload(coordinator.async_add_listener(_async_add_new_alarms))


class AlarmSnoozeButton(EightSleepAlarmEntity, ButtonEntity):
    """Button to snooze a ringing alarm."""

    _attr_name = "Snooze"
    _attr_icon = "mdi:alarm-snooze"

    def __init__(self, coordinator: EightSleepCoordinator, alarm_id: str) -> None:
        super().__init__(coordinator, alarm_id)
        self._attr_unique_id = f"{alarm_id}_snooze"

    async def async_press(self) -> None:
        await self._alarm.snooze()
        await self.coordinator.async_request_refresh()


class AlarmDismissButton(EightSleepAlarmEntity, ButtonEntity):
    """Button to dismiss or stop a ringing alarm."""

    _attr_name = "Dismiss"
    _attr_icon = "mdi:alarm-off"

    def __init__(self, coordinator: EightSleepCoordinator, alarm_id: str) -> None:
        super().__init__(coordinator, alarm_id)
        self._attr_unique_id = f"{alarm_id}_dismiss"

    async def async_press(self) -> None:
        await self._alarm.dismiss()
        await self.coordinator.async_request_refresh()
