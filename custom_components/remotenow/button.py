import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from RemoteNowApiWrapper import RemoteNowApi, keys

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities(
        [
            RemoteNowButton(
                entry.runtime_data, key=keys.keyVolumeUp, entryData=entry.data
            ),
            RemoteNowButton(
                entry.runtime_data, key=keys.keyVolumeDown, entryData=entry.data
            ),
            RemoteNowButton(entry.runtime_data, key=keys.keyMute, entryData=entry.data),
            RemoteNowButton(
                entry.runtime_data, key=keys.keyPower, entryData=entry.data
            ),
            RemoteNowButton(entry.runtime_data, key=keys.keyUp, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.keyDown, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.keyLeft, entryData=entry.data),
            RemoteNowButton(
                entry.runtime_data, key=keys.keyRight, entryData=entry.data
            ),
            RemoteNowButton(
                entry.runtime_data, key=keys.keyReturn, entryData=entry.data
            ),
            RemoteNowButton(entry.runtime_data, key=keys.keyMenu, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.keyExit, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.keyOk, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.keyHome, entryData=entry.data),
            RemoteNowButton(
                entry.runtime_data, key=keys.keyForward, entryData=entry.data
            ),
            RemoteNowButton(entry.runtime_data, key=keys.keyBack, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.keyStop, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.keyPlay, entryData=entry.data),
            RemoteNowButton(
                entry.runtime_data, key=keys.keyPause, entryData=entry.data
            ),
            RemoteNowButton(entry.runtime_data, key=keys.key0, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key1, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key2, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key3, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key4, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key5, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key6, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key7, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key8, entryData=entry.data),
            RemoteNowButton(entry.runtime_data, key=keys.key9, entryData=entry.data),
            RemoteNowButton(
                entry.runtime_data, key=keys.keySubtitle, entryData=entry.data
            ),
        ]
    )


class RemoteNowButton(ButtonEntity):
    # Implement one of these methods.

    def __init__(self, api: RemoteNowApi, key: str, entryData: dict) -> None:
        self._api = api

        self._vendor = entryData["vendor"]
        self._uniqueDeviceId = entryData["uniqueDeviceId"]
        self._boardVersion = entryData["boardVersion"]
        self._sw_version = self._api.getSoftwareVersion()
        self._attributename = key

        self._name = self._attributename.split("_")[1]
        self._available = api.get_Connected()

        _LOGGER.error(self._available)

        self._api.register_handle_on_connected(self._isAvailable)
        self._api.register_handle_on_disconnected(self._isUnavailable)

    @property
    def name(self) -> str:
        return self._name

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

    def press(self) -> None:
        """Handle the button press."""
        self._api.sendKey(self._attributename)

    def _isAvailable(self) -> None:
        self._available = True
        self.schedule_update_ha_state()

    def _isUnavailable(self) -> None:
        self._available = False
        self.schedule_update_ha_state()
