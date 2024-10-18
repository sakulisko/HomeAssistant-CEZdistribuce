"""Module containing the implementation of the CEZ Distribuce price sensor.

This is for the Home Assistant integration.
"""

from datetime import datetime, timedelta
import logging
from zoneinfo import ZoneInfo

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import Throttle

from .binary_sensor import MIN_TIME_BETWEEN_SCANS, isTurnOffParameter, isTurnOnParameter
from .config_flow import CezHDOConfig
from .continuous_measurement import ContinuousMeasurement
from .downloader import isHdo
from .response import ResponseData, day_to_cz_abbrev

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the CEZ Distribuce binary sensor from a config entry."""

    config = CezHDOConfig.from_json(dict(config_entry.data))

    entities = []
    entities.append(ConstantValueSensor(
        "low_tarif_price", config.low_tarif_price))
    entities.append(ConstantValueSensor(
        "high_tarif_price", config.high_tarif_price))
    entities.append(CezDistribucePrice(hass, config))
    async_add_entities(entities)


class CezDistribucePrice(SensorEntity):
    """Class representing the CEZ Distribuce price sensor."""

    def __init__(self, hass: HomeAssistant, cezHdoConfig: CezHDOConfig) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._name = cezHdoConfig.region + "_" + cezHdoConfig.command + "_price"
        self.region = cezHdoConfig.region
        self.command = cezHdoConfig.command
        self.low_tarif_price = cezHdoConfig.low_tarif_price
        self.high_tarif_price = cezHdoConfig.high_tarif_price
        self.responseJson: ResponseData | None = None
        self.last_update_success = False
        self.update()

    @property
    def name(self):
        "Sensor name."
        return self._name

    @property
    def icon(self):
        "Sensor icon."
        return "mdi:cash"

    @property
    def native_value(self):
        "Return the current price based on the tariff."
        if self.responseJson and isHdo(self.responseJson):
            other_sensor_state = self.hass.states.get('sensor.low_tarif_price')
        else:
            other_sensor_state = self.hass.states.get(
                'sensor.high_tarif_price')
        return other_sensor_state.state

    @property
    def native_unit_of_measurement(self):
        "Currency."
        return "Kč/kWh"

    @property
    def extra_state_attributes(self):
        "Additional attributes."
        attributes = {}
        tzinfo = ZoneInfo(self.hass.config.time_zone)
        now = datetime.now(tzinfo)
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        for hour in range(48):
            hour_time = start_time + timedelta(hours=hour)
            hour_str = hour_time.isoformat()
            is_on = self._is_tariff_on(now, hour)
            attributes[hour_str] = (
                self.low_tarif_price if is_on else self.high_tarif_price
            )
        return attributes

    def _is_tariff_on(self, now, hour):
        is_on = False
        for data_entry in self.responseJson.data:
            if data_entry.isDayInRange(day_to_cz_abbrev(now.weekday())):
                timesDict = data_entry.timesList()
                for key, value in timesDict.items():
                    hour_time = datetime.strptime(value, "%H:%M").time()
                    if hour_time.hour == hour:
                        if isTurnOnParameter(key):
                            is_on = True
                        elif isTurnOffParameter(key):
                            is_on = False
        return is_on

    @property
    def should_poll(self):
        "Is pooled sensor."
        return True

    @property
    def available(self):
        "Is available, based on latest data read."
        return self.last_update_success

    @property
    def device_class(self):
        "No device class."
        return ""

    @property
    def unique_id(self):
        "Unique name."
        return "cezdistribuce_" + self._name

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self) -> None:
        "Update sensor."
        _LOGGER.debug("Update data for code %s in region %s",
                      self.command, self.region)
        if self.command in ContinuousMeasurement.isContinuousCode():
            self.responseJson = ContinuousMeasurement.getCode(self.command)
            _LOGGER.debug(
                "Region %s read local data: %s", self.command, self.responseJson
            )
            self.last_update_success = True
            return


class ConstantValueSensor(SensorEntity):
    """Class representing a sensor with a constant value."""

    def __init__(self, name: str, value: float) -> None:
        """Initialize the sensor."""
        self._name = name
        self._value = value

    @property
    def name(self):
        "Sensor name."
        return self._name

    @property
    def icon(self):
        "Sensor icon."
        return "mdi:cash"

    @property
    def native_value(self):
        "Return the constant value."
        return self._value

    @property
    def should_poll(self):
        "No polling needed for constant value."
        return False

    @property
    def available(self):
        "Always available."
        return True

    @property
    def device_class(self):
        "No device class."
        return ""

    @property
    def unique_id(self):
        "Unique name."
        return "constant_value_" + self._name

    @property
    def native_unit_of_measurement(self):
        "Currency."
        return "Kč/kWh"
