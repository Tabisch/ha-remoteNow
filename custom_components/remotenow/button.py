from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from RemoteNowApiWrapper import RemoteNowApi, keys

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities(
        [
            RemoteNowButton(entry.runtime_data, key=keys.keyVolumeUp),
            RemoteNowButton(entry.runtime_data, key=keys.keyVolumeDown),
            RemoteNowButton(entry.runtime_data, key=keys.keyMute),
            RemoteNowButton(entry.runtime_data, key=keys.keyPower),
            RemoteNowButton(entry.runtime_data, key=keys.keyUp),
            RemoteNowButton(entry.runtime_data, key=keys.keyDown),
            RemoteNowButton(entry.runtime_data, key=keys.keyLeft),
            RemoteNowButton(entry.runtime_data, key=keys.keyRight),
            RemoteNowButton(entry.runtime_data, key=keys.keyReturn),
            RemoteNowButton(entry.runtime_data, key=keys.keyMenu),
            RemoteNowButton(entry.runtime_data, key=keys.keyExit),
            RemoteNowButton(entry.runtime_data, key=keys.keyOk),
            RemoteNowButton(entry.runtime_data, key=keys.keyHome),
            RemoteNowButton(entry.runtime_data, key=keys.keyForward),
            RemoteNowButton(entry.runtime_data, key=keys.keyBack),
            RemoteNowButton(entry.runtime_data, key=keys.keyStop),
            RemoteNowButton(entry.runtime_data, key=keys.keyPlay),
            RemoteNowButton(entry.runtime_data, key=keys.keyPause),
            RemoteNowButton(entry.runtime_data, key=keys.key0),
            RemoteNowButton(entry.runtime_data, key=keys.key1),
            RemoteNowButton(entry.runtime_data, key=keys.key2),
            RemoteNowButton(entry.runtime_data, key=keys.key3),
            RemoteNowButton(entry.runtime_data, key=keys.key4),
            RemoteNowButton(entry.runtime_data, key=keys.key5),
            RemoteNowButton(entry.runtime_data, key=keys.key6),
            RemoteNowButton(entry.runtime_data, key=keys.key7),
            RemoteNowButton(entry.runtime_data, key=keys.key8),
            RemoteNowButton(entry.runtime_data, key=keys.key9),
            RemoteNowButton(entry.runtime_data, key=keys.keySubtitle),
        ]
    )


class RemoteNowButton(ButtonEntity):
    # Implement one of these methods.

    def __init__(self, api: RemoteNowApi, key: str) -> None:
        self._api = api

        self._vendor = self._api.getVendor()
        self._uniqueDeviceId = self._api.getUniqueDeviceId()
        self._boardVersion = self._api.getBoardVersion()
        self._sw_version = self._api.getSoftwareVersion()
        self._attributename = key

        self._name = self._attributename.split("_")[1]

    @property
    def name(self) -> str:
        return self._name

    @property
    def unique_id(self) -> str:
        return f"{self._uniqueDeviceId}_{self._attributename}"

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
