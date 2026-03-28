"""Config flow for Eight Sleep integration."""

from __future__ import annotations

import httpx
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.httpx_client import get_async_client

from eight_sleep_client import Session
from eight_sleep_client.api.exceptions import AuthenticationError, ConnectionError

from .const import DOMAIN


class EightSleepConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eight Sleep."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                http = get_async_client(self.hass)
                session = await Session.create(
                    http,
                    email=user_input["email"],
                    password=user_input["password"],
                )
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except (ConnectionError, httpx.HTTPError):
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(session.user_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input["email"],
                    data={
                        "email": user_input["email"],
                        "password": user_input["password"],
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("email"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )
