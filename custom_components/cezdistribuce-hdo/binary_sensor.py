"""CEZ Distribuce."""

__version__ = "0.2"

from datetime import datetime, timedelta
import logging
from zoneinfo import ZoneInfo

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import Throttle

from .config_flow import CezHDOConfig
from .continuous_measurement import ContinuousMeasurement
from .downloader import isHdo
from .response import ResponseData, day_to_cz_abbrev

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=3600)
_LOGGER = logging.getLogger(__name__)

CONF_REGION = "region"
CONF_CODE = "code"
CONF_NAME = "name"


# def setup_platform(hass, config, add_entities, discovery_info=None):
#     "setup platform"
#     name = config.get(CONF_NAME)
#     region = config.get(CONF_REGION)
#     code = config.get(CONF_CODE)

#     entities = []
#     entities.append(CezDistribuce(name, region, code))
#     add_entities(entities)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the CEZ Distribuce binary sensor from a config entry."""

    config = CezHDOConfig.from_json(dict(config_entry.data))

    entities = []
    entities.append(CezDistribuceTarifState(hass, config))
    async_add_entities(entities)


class CezDistribuceTarifState(BinarySensorEntity):
    "Sensor class."

    def __init__(self, hass: HomeAssistant, cezHdoConfig: CezHDOConfig) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._name = cezHdoConfig.region + "_" + cezHdoConfig.command
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
        return "mdi:power"

    @property
    def is_on(self):
        "Sensor on/off."
        return isHdo(self.responseJson)

    @property
    def extra_state_attributes(self):
        "Additional attributes."
        attributes = {}
        # attributes["response_json"] = to_json(self.responseJson)
        tzinfo = ZoneInfo(self.hass.config.time_zone)
        now = datetime.now(tzinfo)
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        # is_on = False
        for hour in range(48):
            hour_time = start_time + timedelta(hours=hour)
            hour_str = hour_time.isoformat()
            attributes[hour_str] = self._is_hour_on(hour_time, now)
        return attributes

    def _is_hour_on(self, hour: datetime, now: datetime) -> bool:
        """Determine if the sensor is on for a specific hour."""
        is_on = False
        for data_entry in self.responseJson.data:
            if data_entry.isDayInRange(day_to_cz_abbrev(now.weekday())):
                times_dict = data_entry.timeRanges()
                for start, end in times_dict:
                    start_time = datetime.strptime(start, "%H:%M").time()
                    end_time = datetime.strptime(end, "%H:%M").time()
                    is_on = start_time <= hour.time() < end_time
                    if is_on:
                        return is_on
                return is_on

        return False

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
        # REGION = "regionStred"
        # CODE = "A1B5DP6"
        _LOGGER.debug("Update data for code %s in region %s",
                      self.command, self.region)
        if self.command in ContinuousMeasurement.isContinuousCode():
            self.responseJson = ContinuousMeasurement.getCode(self.command)
            _LOGGER.debug(
                "Region %s read local data: %s", self.command, self.responseJson
            )
            self.last_update_success = True
            return

        # response = requests.get(getRequestUrl(self.region, self.code), timeout=30)
        # if response.status_code == 200:
        #     self.responseJson = parse_json(response.json())
        #     _LOGGER.debug("Region %s read data from web: %s", self.responseJson)
        #     self.last_update_success = True
        # else:
        #     _LOGGER.warning(
        #         "Error getting data from CEZ. Status code: %s",
        #         self.code,
        #         response.status_code,
        #     )
        #     self.last_update_success = False


def isTurnOnParameter(parameterName: str) -> bool:
    """Check if the parameter name indicates a turn-on action."""
    return parameterName.startswith("CAS_ZAP_")


def isTurnOffParameter(parameterName: str) -> bool:
    """Check if the parameter name indicates a turn-off action."""
    return parameterName.startswith("CAS_VYP_")
