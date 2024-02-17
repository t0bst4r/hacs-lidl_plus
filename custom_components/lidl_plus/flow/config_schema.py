import voluptuous as vol
from homeassistant.const import CONF_TOKEN, CONF_COUNTRY_CODE, CONF_LANGUAGE
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType, CountrySelector, \
    CountrySelectorConfig, LanguageSelector, LanguageSelectorConfig

__all__ = [
    "config_schema",
    "CONF_TOKEN",
    "CONF_COUNTRY_CODE",
    "CONF_LANGUAGE"
]

config_schema = vol.Schema(
    {
        vol.Required(CONF_TOKEN): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD)),
        vol.Required(CONF_COUNTRY_CODE, default="DE"): CountrySelector(CountrySelectorConfig()),
        vol.Required(CONF_LANGUAGE, default="de"): LanguageSelector(LanguageSelectorConfig()),
    }
)
