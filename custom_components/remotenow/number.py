from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from RemoteNowApiWrapper import RemoteNowApi

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([RemoteNowVolumeNumber(entry.runtime_data, entry.data)])


class RemoteNowVolumeNumber(NumberEntity, RemoteNowApi):
    # Implement one of these methods.

    def __init__(self, api: RemoteNowApi, entryData: dict) -> None:
        self._api = api

        self._vendor = entryData["vendor"]
        self._uniqueDeviceId = entryData["uniqueDeviceId"]
        self._boardVersion = entryData["boardVersion"]
        self._sw_version = self._api.getSoftwareVersion()
        self._attributename = "volume"

        self._name = "Volume"
        self._available = api.get_Connected()
        self._state = 0

        self._api.register_handle_on_connected(self._isAvailable)
        self._api.register_handle_on_disconnected(self._isUnavailable)

        self._api.register_handle_on_volumeChange(self.updateValue)

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> int:
        return self._state

    @property
    def unique_id(self) -> str:
        return f"{self._uniqueDeviceId}_{self._attributename}"

    @property
    def available(self) -> str:
        return self._available

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._uniqueDeviceId)
            },
            "manufacturer": self._vendor,
            "model": self._boardVersion,
            "sw_version": self._sw_version,
        }

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._api.changeVolume(int(value))

    def updateValue(self, payload) -> None:
        """Update"""

        print(payload)

        self._state = payload["volume_value"]
        self.schedule_update_ha_state()

    def _isAvailable(self) -> None:
        self._available = True
        self.schedule_update_ha_state()

    def _isUnavailable(self) -> None:
        self._available = False
        self.schedule_update_ha_state()
