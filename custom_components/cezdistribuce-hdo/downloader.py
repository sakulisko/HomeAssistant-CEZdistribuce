"""Helper download functions."""

import datetime

# python 3.9+
from zoneinfo import ZoneInfo

import aiohttp
from aiohttp import ClientTimeout

from .config_flow import CEZ_REGIONS_CZ
from .response import ResponseData, day_to_cz_abbrev

BASE_URL = "https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/"
CEZ_TIMEZONE = ZoneInfo("Europe/Prague")


def getCorrectRegionName(region) -> str | None:
    "Validate region."
    region = region.lower()
    for x in CEZ_REGIONS_CZ:
        if x in region:
            return x
    return None


def isCorrectRegionName(region) -> bool:
    "Validate region."
    return (region.lower()) in CEZ_REGIONS_CZ


def getRequestUrl(region: str, code: str) -> str:
    "Create request URI."
    corrected_region = getCorrectRegionName(region) or ""
    return BASE_URL + corrected_region + "?&code=" + code.upper()


def timeInRange(start, end, x):
    "Is time in range."
    if start <= end:
        return start <= x <= end
    return start <= x or x <= end


def parseTime(date_time_str):
    "Parse time from source data."
    if not date_time_str:
        return datetime.time(0, 0)
    return datetime.datetime.strptime(date_time_str, "%H:%M").time()


async def async_get_cez_hdo_data(region: str, code: str):
    "Download data from CEZ."
    async with (
        aiohttp.ClientSession() as session,
        session.get(getRequestUrl(region, code), timeout=ClientTimeout()) as response,
    ):
        if response.status == 200:
            return await response.json()
        # raise Exception(f"Error getting data from CEZ. Status code: {response.status}")
        return None


def isHdo(jsonCalendar: ResponseData):
    """Find out if the HDO is enabled for the current timestamp.

    :param jsonCalendar: JSON with calendar schedule from CEZ
    :param daytime: relevant time in "Europe/Prague" timezone to check if HDO is on or not
    :return: bool
    """
    daytime = datetime.datetime.now(tz=CEZ_TIMEZONE)

    for entry in jsonCalendar.data:
        if entry.isDayInRange(day_to_cz_abbrev(daytime.weekday())):
            for start, end in entry.timeRanges():
                startTime = parseTime(start)
                endTime = parseTime(end)
                if timeInRange(startTime, endTime, daytime.time()):
                    return True

    return False
