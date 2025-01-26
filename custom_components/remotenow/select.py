import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from RemoteNowApiWrapper import RemoteNowApi

from homeassistant.components.select import SelectEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities(
        [
            RemoteNowSourceSelect(entry.runtime_data, entry.data),
            RemoteNowChannelSelect(entry.runtime_data, entry.data),
        ],
    )


class RemoteNowSourceSelect(SelectEntity, RemoteNowApi):
    # Implement one of these methods.

    def __init__(self, api: RemoteNowApi, entryData: dict) -> None:
        self._api = api

        self._vendor = entryData["vendor"]
        self._uniqueDeviceId = entryData["uniqueDeviceId"]
        self._boardVersion = entryData["boardVersion"]
        self._sw_version = self._api.getSoftwareVersion()
        self._attributename = "source"

        self._name = "Source"
        self._available = api.get_Connected()

        self._current_option = ""
        self._options = []

        self._sources = []

        self._api.register_handle_on_connected(self._isAvailable)
        self._api.register_handle_on_disconnected(self._isUnavailable)

        self._api.register_handle_on_SourceList(self._updateSourceList)
        self._api.register_handle_on_state(self._updateCurrentOption)

        if self._available:
            self._api.getSourceList()

    @property
    def name(self) -> str:
        return self._name

    @property
    def current_option(self) -> int:
        return self._current_option

    @property
    def options(self) -> int:
        return self._options

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

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        for source in self._sources:
            if source["displayname"] == option:
                self._api.changeSource(sourceId=source["sourceid"])

    def _updateSourceList(self, payload):
        newSources = []
        self._sources = payload

        for source in payload:
            newSources.append(source["displayname"])

        self._options = newSources
        self.schedule_update_ha_state()

    def _updateCurrentOption(self, payload: dict) -> None:
        """Update"""
        print(payload)

        if "displayname" not in payload.keys():
            return

        self._current_option = payload["displayname"]
        self.schedule_update_ha_state()

    def _isAvailable(self) -> None:
        self._available = True
        self._api.getSourceList()
        self.schedule_update_ha_state()

    def _isUnavailable(self) -> None:
        self._available = False
        self.schedule_update_ha_state()


class RemoteNowChannelSelect(SelectEntity, RemoteNowApi):
    # Implement one of these methods.

    def __init__(self, api: RemoteNowApi, entryData: dict) -> None:
        self._api = api

        self._vendor = entryData["vendor"]
        self._uniqueDeviceId = entryData["uniqueDeviceId"]
        self._boardVersion = entryData["boardVersion"]
        self._sw_version = self._api.getSoftwareVersion()
        self._attributename = "channel"

        self._name = "Channel"
        self._available = api.get_Connected()

        self._current_option = ""
        self._options = []

        self._channels = []

        self._api.register_handle_on_connected(self._isAvailable)
        self._api.register_handle_on_disconnected(self._isUnavailable)

        self._api.register_handle_on_channelList(self._updateChannelList)
        self._api.register_handle_on_state(self._updateCurrentOption)

        # Remove ASTRA hardcoding
        if self._available:
            self._api.getChannelList(
                list_para="sl1039d34d-3a91-47f4-9805-a44bed1d832b",
                list_name="ASTRA1 19.2°E",
            )

    @property
    def name(self) -> str:
        return self._name

    @property
    def current_option(self) -> int:
        return self._current_option

    @property
    def options(self) -> int:
        return self._options

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

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        for channel in self._channels:
            if channel["channel_name"] == option:
                self._api.changeChannel(channel_param=channel["channel_param"])

    def _updateChannelList(self, payload):
        newChannels = []
        self._channels = payload["list"]

        for channel in self._channels:
            newChannels.append(channel["channel_name"])

        self._options = newChannels
        self.schedule_update_ha_state()

    def _updateCurrentOption(self, payload: dict) -> None:
        """Update"""
        print(payload)

        if "channel_name" not in payload.keys():
            return

        self._current_option = payload["channel_name"]
        self.schedule_update_ha_state()

    def _isAvailable(self) -> None:
        self._available = True
        self._api.getChannelList(
            list_para="sl1039d34d-3a91-47f4-9805-a44bed1d832b",
            list_name="ASTRA1 19.2°E",
        )
        self.schedule_update_ha_state()

    def _isUnavailable(self) -> None:
        self._available = False
        self.schedule_update_ha_state()
