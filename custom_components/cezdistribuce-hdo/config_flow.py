"""Config flow for Cez HDO integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig

from .const import DOMAIN
from .continuous_measurement import ContinuousMeasurement

_LOGGER = logging.getLogger(__name__)

CEZ_REGIONS_CZ = ["zapad", "sever", "stred", "vychod", "morava"]
CONF_COMMAND_CODE = "command"
CONF_REGION = "region"

CEZ_HDO_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_COMMAND_CODE): str,
        vol.Required(CONF_REGION): SelectSelector(
            SelectSelectorConfig(options=CEZ_REGIONS_CZ,
                                 translation_key="region")
        ),
    }
)

# Define a new schema for the tarif prices step
CONF_LOW_TARIF_PRICE = "low_tarif_price"
CONF_HIGH_TARIF_PRICE = "high_tarif_price"

TARIF_PRICES_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_LOW_TARIF_PRICE): vol.Coerce(float),
        vol.Required(CONF_HIGH_TARIF_PRICE): vol.Coerce(float),
    }
)


class PlaceholderHub:
    """Placeholder class to make tests pass.

    TODO Remove this placeholder class and replace with things from your PyPI package.
    """

    def __init__(self, host: str) -> None:
        """Initialize."""
        self.host = host


async def validate_hdo_config(
    hass: HomeAssistant, data: dict[str, Any]
) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data[CONF_USERNAME], data[CONF_PASSWORD]
    # )

    # hub = PlaceholderHub(data[CONF_HOST])

    # if not await hub.authenticate(data[CONF_USERNAME], data[CONF_PASSWORD]):
    #     raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    for key, value in data.items():
        _LOGGER.info("Key: %s, Value: %s", key, value)

    command = data[CONF_COMMAND_CODE]
    region = data[CONF_REGION]
    if command in ContinuousMeasurement.CODES:
        # Local data
        if (region is not None) and (region in CEZ_REGIONS_CZ):
            return {CONF_COMMAND_CODE: command, CONF_REGION: region}

    # response = await

    if not command or not region:
        raise ValueError("Invalid command or region")

    # Return info that you want to store in the config entry.
    return data


async def validate_price_config(
    hass: HomeAssistant, data: dict[str, Any]
) -> dict[str, Any]:
    """Validate the user input for price configuration."""

    for key, value in data.items():
        _LOGGER.info("Key: %s, Value: %s", key, value)

    # Return info that you want to store in the config entry.
    return data


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Cez HDO."""

    MAJOR_VERSION = 0
    MINOR_VERSION = 0
    BUGFIX_VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.hdo_config: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_hdo_config(self.hass, user_input)
                self.hdo_config = info
                return await self.async_step_tarif_prices()
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title="hdo config", data=user_input)

        return self.async_show_form(data_schema=CEZ_HDO_DATA_SCHEMA, errors=errors)

    async def async_step_tarif_prices(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the step to define prices for low and high tarrif."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_price_config(self.hass, user_input)
                self.hdo_config.update(info)
                return self.async_create_entry(title="Cez HDO", data=self.hdo_config)
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="tarif_prices", data_schema=TARIF_PRICES_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class CezHDOConfig:
    """Class to represent the Cez HDO configuration."""

    def __init__(
        self, command: str, region: str, low_tarif_price: float, high_tarif_price: float
    ) -> None:
        """Initialize the configuration."""
        self.command = command.upper()
        self.region = region
        self.low_tarif_price = low_tarif_price
        self.high_tarif_price = high_tarif_price

    def to_json(self) -> dict[str, Any]:
        """Convert the configuration to a JSON-serializable dictionary."""
        return {
            CONF_COMMAND_CODE: self.command,
            CONF_REGION: self.region,
            CONF_LOW_TARIF_PRICE: self.low_tarif_price,
            CONF_HIGH_TARIF_PRICE: self.high_tarif_price,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> CezHDOConfig:
        """Create a configuration instance from a JSON-serializable dictionary."""
        return cls(
            command=data[CONF_COMMAND_CODE],
            region=data[CONF_REGION],
            low_tarif_price=data[CONF_LOW_TARIF_PRICE],
            high_tarif_price=data[CONF_HIGH_TARIF_PRICE],
        )
