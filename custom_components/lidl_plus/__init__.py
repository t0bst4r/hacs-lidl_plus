"""The Bring! integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from lidlplus import LidlPlusApi

from .const import DOMAIN
from .data import LidlPlusDataUpdateCoordinator
from .flow import CONF_TOKEN, CONF_LANGUAGE, CONF_COUNTRY_CODE

PLATFORMS: list[Platform] = [Platform.TODO]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    token = entry.data[CONF_TOKEN]
    country_code = entry.data[CONF_COUNTRY_CODE]
    language = entry.data[CONF_LANGUAGE]

    lidl = LidlPlusApi(language, country_code, token)
    coordinator = LidlPlusDataUpdateCoordinator(hass, lidl)

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
