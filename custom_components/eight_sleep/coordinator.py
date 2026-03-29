"""Data update coordinator for Eight Sleep."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from eight_sleep_client import Session
from eight_sleep_client.api.exceptions import EightSleepError
from eight_sleep_client.models.alarm import Alarm

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)


class EightSleepCoordinator(DataUpdateCoordinator[list[Alarm]]):
    """Fetches data from the Eight Sleep API."""

    def __init__(self, hass: HomeAssistant, session: Session, config_entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.session = session
        self.config_entry = config_entry
        self._previous_alarm_ids: set[str] = set()

    async def _async_update_data(self) -> list[Alarm]:
        """Fetch alarms from the API."""
        try:
            alarms = await self.session.alarms.all()
        except EightSleepError as err:
            raise UpdateFailed(f"Error fetching Eight Sleep data: {err}") from err

        current_ids = {a.id for a in alarms}
        if stale_ids := self._previous_alarm_ids - current_ids:
            device_registry = dr.async_get(self.hass)
            for alarm_id in stale_ids:
                device = device_registry.async_get_device(identifiers={(DOMAIN, alarm_id)})
                if device:
                    device_registry.async_update_device(
                        device_id=device.id,
                        remove_config_entry_id=self.config_entry.entry_id,
                    )
        self._previous_alarm_ids = current_ids

        return alarms
