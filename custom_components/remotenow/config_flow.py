"""Config flow for the RemoteNow integration."""

from __future__ import annotations

import asyncio

import logging
from typing import Any

from RemoteNowApiWrapper import RemoteNowApi

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_CHOOSE, CONF_CODE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_HOST): str})
STEP_AUTH_DATA_SCHEMA = vol.Schema({vol.Required(CONF_CHOOSE): bool})
STEP_SENDAUTH_DATA_SCHEMA = vol.Schema({vol.Required(CONF_CODE): int})


class RemoteNowFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RemoteNow."""

    VERSION = 1

    entryData = {}
    api = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                self.api = RemoteNowApi(
                    hostname=user_input[CONF_HOST], identifer="homeassistant"
                )
                self.api.connect()

                # while not self.api.get_Connected():
                #     await asyncio.sleep(5)

            except Exception:
                _LOGGER.exception("Unexpected exception")
            else:
                self.entryData = {
                    "host": user_input[CONF_HOST],
                    "uniqueDeviceId": self.api.getUniqueDeviceId(),
                    "boardVersion": self.api.getBoardVersion(),
                    "vendor": self.api.getVendor(),
                }

                return await self.async_step_auth()

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_auth(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        self.api.getAuthCode()

        print("getAuthCode")

        errors: dict[str, str] = {}
        if user_input is not None:
            if user_input["choose"]:
                return await self.async_step_sendAuth()
            else:
                return self.async_create_entry(
                    title=self.entryData[CONF_HOST], data=self.entryData
                )

        return self.async_show_form(
            step_id="auth", data_schema=STEP_AUTH_DATA_SCHEMA, errors=errors
        )

    async def async_step_sendAuth(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        print("async_step_sendAuth")

        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                self.api.sendAuthenticationCode(user_input[CONF_CODE])
            except Exception:
                _LOGGER.exception("Unexpected exception")
            else:
                return self.async_create_entry(
                    title=self.entryData[CONF_HOST], data=self.entryData
                )

        return self.async_show_form(
            step_id="sendAuth", data_schema=STEP_SENDAUTH_DATA_SCHEMA, errors=errors
        )
