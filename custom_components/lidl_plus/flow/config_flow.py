from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from lidlplus import LidlPlusApi

from .config_schema import config_schema, CONF_TOKEN, CONF_LANGUAGE, CONF_COUNTRY_CODE
from ..const import DOMAIN

__all__ = [
    "ConfigFlow"
]

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            lidl = LidlPlusApi(user_input[CONF_LANGUAGE], user_input[CONF_COUNTRY_CODE], user_input[CONF_TOKEN])

            try:
                loyalty_id = await self.hass.async_add_executor_job(lidl.loyalty_id)
            except Exception as e:
                _LOGGER.error("Configuration failed", extra={"error": e})
                errors["base"] = "invalid_auth"
            else:
                await self.async_set_unique_id(loyalty_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=loyalty_id, data=user_input)

        return self.async_show_form(step_id="user", data_schema=config_schema, errors=errors)
