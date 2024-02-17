"""DataUpdateCoordinator for the Lidl Plus integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from lidlplus import LidlPlusApi

from ..const import DOMAIN
from ..domain import convert_lidl_plus_coupons, LidlPlusData

__all__ = [
    "LidlPlusDataUpdateCoordinator"
]

_LOGGER = logging.getLogger(__name__)


class LidlPlusDataUpdateCoordinator(DataUpdateCoordinator[LidlPlusData]):
    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, lidl: LidlPlusApi) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=90))
        self.lidl = lidl

    async def _async_update_data(self) -> LidlPlusData:
        try:
            coupon_result = await self.hass.async_add_executor_job(self.lidl.coupons)
        except Exception as e:
            raise UpdateFailed("Unable to connect and retrieve data from Lidl Plus") from e

        coupons = convert_lidl_plus_coupons(coupon_result)
        return LidlPlusData(coupons=coupons)
