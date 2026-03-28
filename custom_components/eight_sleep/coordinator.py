"""Data update coordinator for Eight Sleep."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from eight_sleep_client import Session
from eight_sleep_client.api.exceptions import EightSleepError
from eight_sleep_client.models.alarm import Alarm

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)


class EightSleepCoordinator(DataUpdateCoordinator[list[Alarm]]):
    """Fetches data from the Eight Sleep API."""

    def __init__(self, hass: HomeAssistant, session: Session) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.session = session

    async def _async_update_data(self) -> list[Alarm]:
        """Fetch alarms from the API."""
        try:
            return await self.session.alarms.all()
        except EightSleepError as err:
            raise UpdateFailed(f"Error fetching Eight Sleep data: {err}") from err
