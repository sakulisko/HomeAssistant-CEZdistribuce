"""The Cez HDO integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .config_flow import CezHDOConfig

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

type CezHDOConfigEntry = ConfigEntry[CezHDOConfig]


async def async_setup_entry(hass: HomeAssistant, entry: CezHDOConfigEntry) -> bool:
    """Set up Cez HDO from a config entry."""

    entry.runtime_data = CezHDOConfig.from_json(data=dict(entry.data))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: CezHDOConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
