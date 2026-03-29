"""Eight Sleep integration for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.httpx_client import get_async_client

from eight_sleep_client import Session
from eight_sleep_client.api.exceptions import AuthenticationError, ConnectionError

from .const import DOMAIN, PLATFORMS
from .coordinator import EightSleepCoordinator

type EightSleepConfigEntry = ConfigEntry[EightSleepCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: EightSleepConfigEntry) -> bool:
    """Set up Eight Sleep from a config entry."""
    http = get_async_client(hass)

    try:
        session = await Session.create(
            http,
            email=entry.data["email"],
            password=entry.data["password"],
        )
    except AuthenticationError as err:
        raise ConfigEntryAuthFailed("Invalid credentials") from err
    except ConnectionError as err:
        raise ConfigEntryNotReady("Cannot connect to Eight Sleep") from err

    coordinator = EightSleepCoordinator(hass, session, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: EightSleepConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_remove_config_entry_device(
    hass: HomeAssistant,
    config_entry: EightSleepConfigEntry,
    device_entry: dr.DeviceEntry,
) -> bool:
    """Allow removal of a device if the alarm no longer exists."""
    coordinator = config_entry.runtime_data
    current_ids = {a.id for a in coordinator.data}
    return not any(
        identifier[1] in current_ids
        for identifier in device_entry.identifiers
        if identifier[0] == DOMAIN
    )
