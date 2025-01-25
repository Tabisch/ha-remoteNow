"""Config flow for the RemoteNow integration."""

from __future__ import annotations

import asyncio

import logging
from typing import Any

from RemoteNowApiWrapper import RemoteNowApi

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_HOST): str})


class RemoteNowFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RemoteNow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                api = RemoteNowApi(hostname=user_input[CONF_HOST])
                api.connect()

                while True:
                    if api.get_Connected():
                        break
                    else:
                        await asyncio.sleep(5)

            except Exception:
                _LOGGER.exception("Unexpected exception")
            else:
                entryData = {
                    "host": user_input[CONF_HOST],
                    "uniqueDeviceId": api.getUniqueDeviceId(),
                    "boardVersion": api.getBoardVersion(),
                    "vendor": api.getVendor(),
                }

                return self.async_create_entry(
                    title=user_input[CONF_HOST], data=entryData
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
