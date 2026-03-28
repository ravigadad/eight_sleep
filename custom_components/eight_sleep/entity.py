"""Base entity for Eight Sleep."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EightSleepCoordinator


class EightSleepEntity(CoordinatorEntity[EightSleepCoordinator]):
    """Base entity for Eight Sleep devices."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: EightSleepCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.session.user_id)},
            name="Eight Sleep Pod",
            manufacturer="Eight Sleep",
        )
