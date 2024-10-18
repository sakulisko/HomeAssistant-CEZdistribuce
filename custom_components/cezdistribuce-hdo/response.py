"""Module provides classes and functions to handle and parse response data.

Classes:
    DataEntry: A data class representing an entry with various attributes.
    DayOfWeek: An enumeration of days of the week.
    ResponseData: A data class that holds a list of DataEntry objects.

Functions:
    day_to_cz_abbrev(day: int) -> DayOfWeek: Convert weekday number to Czech abbreviation.
    parse_json(json_string: str) -> ResponseData: Parse a JSON string into a ResponseData object.
    to_json(response_data: ResponseData) -> str: Convert a ResponseData object to a JSON string.
"""

from dataclasses import dataclass
from enum import Enum
import json


class DayOfWeek(Enum):
    """An enumeration representing the days of the week with their corresponding abbreviations.

    Attributes:
        MONDAY (str): Abbreviation for Monday ("Po").
        TUESDAY (str): Abbreviation for Tuesday ("Ut").
        WEDNESDAY (str): Abbreviation for Wednesday ("St").
        THURSDAY (str): Abbreviation for Thursday ("Ct").
        FRIDAY (str): Abbreviation for Friday ("Pa").
        SATURDAY (str): Abbreviation for Saturday ("So").
        SUNDAY (str): Abbreviation for Sunday ("Ne").

    Methods:
        ordinal() -> int:
            Returns the ordinal position of the day within the week, where Monday is 0 and Sunday is 6.

    """

    MONDAY = "Po"
    TUESDAY = "Ut"
    WEDNESDAY = "St"
    THURSDAY = "Ct"
    FRIDAY = "Pa"
    SATURDAY = "So"
    SUNDAY = "Ne"

    def ordinal(self):
        """Return the ordinal (index) of the current instance within the DayOfWeek enumeration.

        The method converts the DayOfWeek enumeration into a list and finds the index of the current instance.

        Returns:
            int: The zero-based index of the current instance in the DayOfWeek enumeration.

        """
        members = list(DayOfWeek)
        return members.index(self)


@dataclass
class DataEntry:
    """A class to represent a data entry with various attributes and methods to process time ranges and validity.

    Attributes:
        ID (int | None): The ID of the data entry.
        VALID_FROM (str | None): The start date of validity.
        VALID_TO (str | None): The end date of validity.
        DUMP_ID (int | None): The dump ID associated with the data entry.
        POVEL (str | None): The POVEL code.
        KOD (str | None): The KOD code.
        KOD_POVELU (str | None): The KOD_POVELU code.
        SAZBA (str | None): The SAZBA code.
        INFO (str | None): Additional information.
        PLATNOST (str | None): The validity period.
        DOBA (str | None): The duration.
        CAS_ZAP_1 to CAS_ZAP_10 (str | None): Start times for different periods.
        CAS_VYP_1 to CAS_VYP_10 (str | None): End times for different periods.
        DATE_OF_ENTRY (str | None): The date of entry.
        DESCRIPTION (str | None): The description of the data entry.

    Methods:
        timesList() -> dict[str, str]:
            Returns a dictionary of start and end times that are not None.

        timeRanges() -> list[tuple[str, str]]:
            Returns a list of tuples containing start and end times that are both not None.

        isDayInRange(day: str) -> bool:
            Checks if a given day is within the validity range specified by PLATNOST.

    """

    PLATNOST: str
    ID: int | None = None
    VALID_FROM: str | None = None
    VALID_TO: str | None = None
    DUMP_ID: int | None = None
    POVEL: str | None = None
    KOD: str | None = None
    KOD_POVELU: str | None = None
    SAZBA: str | None = None
    INFO: str | None = None
    DOBA: str | None = None
    CAS_ZAP_1: str | None = None
    CAS_VYP_1: str | None = None
    CAS_ZAP_2: str | None = None
    CAS_VYP_2: str | None = None
    CAS_ZAP_3: str | None = None
    CAS_VYP_3: str | None = None
    CAS_ZAP_4: str | None = None
    CAS_VYP_4: str | None = None
    CAS_ZAP_5: str | None = None
    CAS_VYP_5: str | None = None
    CAS_ZAP_6: str | None = None
    CAS_VYP_6: str | None = None
    CAS_ZAP_7: str | None = None
    CAS_VYP_7: str | None = None
    CAS_ZAP_8: str | None = None
    CAS_VYP_8: str | None = None
    CAS_ZAP_9: str | None = None
    CAS_VYP_9: str | None = None
    CAS_ZAP_10: str | None = None
    CAS_VYP_10: str | None = None
    DATE_OF_ENTRY: str | None = None
    DESCRIPTION: str | None = None

    def timesList(self) -> dict[str, str]:
        """Generate a dictionary of start and end times.

        This method iterates over a predefined range of indices (1 to 10) and retrieves
        the start and end times associated with each index from the instance attributes.
        It then constructs a dictionary where the keys are the attribute names and the
        values are the corresponding times.

        Returns:
            dict[str, str]: A dictionary containing the start and end times. The keys
            are in the format "CAS_ZAP_{i}" for start times and "CAS_VYP_{i}" for end times,
            where {i} is the index.

        """
        times = {}
        for i in range(1, 11):
            start_time = getattr(self, f"CAS_ZAP_{i}")
            end_time = getattr(self, f"CAS_VYP_{i}")
            if start_time is not None:
                times[f"CAS_ZAP_{i}"] = start_time
            if end_time is not None:
                times[f"CAS_VYP_{i}"] = end_time
        return times

    def timeRanges(self) -> list[tuple[str, str]]:
        """Generate a list of time ranges based on instance attributes.

        This method iterates over a predefined range of indices (1 to 10) and
        retrieves the start and end times from the instance attributes named
        'CAS_ZAP_i' and 'CAS_VYP_i' respectively, where 'i' is the current index.
        If both start and end times are not None, they are added as a tuple to
        the list of ranges.

        Returns:
            list[tuple[str, str]]: A list of tuples, each containing a start
            time and an end time as strings.

        """
        ranges = []
        for i in range(1, 11):
            start_time = getattr(self, f"CAS_ZAP_{i}")
            end_time = getattr(self, f"CAS_VYP_{i}")
            if start_time is not None and end_time is not None:
                ranges.append((start_time, end_time))
        return ranges

    def isDayInRange(self, day: DayOfWeek) -> bool:
        """Check if a given day is within the range specified by the PLATNOST attribute.

        Args:
            day (str): The day to check, represented as a string.

        Returns:
            bool: True if the day is within the range, False otherwise.

        """
        day_range = self.PLATNOST.split(" - ")
        start = DayOfWeek(day_range[0]).ordinal()
        end = DayOfWeek(day_range[1]).ordinal()
        current = day.ordinal()
        return start <= current <= end


def day_to_cz_abbrev(day: int) -> DayOfWeek:
    """Convert weekday number to Czech abbreviation."""
    days = {
        0: DayOfWeek.MONDAY,
        1: DayOfWeek.TUESDAY,
        2: DayOfWeek.WEDNESDAY,
        3: DayOfWeek.THURSDAY,
        4: DayOfWeek.FRIDAY,
        5: DayOfWeek.SATURDAY,
        6: DayOfWeek.SUNDAY,
    }
    return days.get(day, DayOfWeek.MONDAY)


@dataclass
class ResponseData:
    """ResponseData is a data class that holds a list of DataEntry objects.

    Attributes:
        data (List[DataEntry]): A list of DataEntry objects.

    """

    data: list[DataEntry]


def parse_json(json_string: str) -> ResponseData:
    """Parse a JSON string and convert it into a ResponseData object.

    Args:
        json_string (str): The JSON string to be parsed.

    Returns:
        ResponseData: An object containing the parsed data entries.

    Raises:
        KeyError: If the expected keys are not found in the JSON data.
        json.JSONDecodeError: If the JSON string is not properly formatted.

    """
    json_data = json.loads(json_string)
    data_entries = [
        DataEntry(
            **{k if k != "primaryKey" else "primary_key": v for k, v in entry.items()}
        )
        for entry in json_data["data"]
    ]
    return ResponseData(data=data_entries)


def to_json(response_data: ResponseData) -> str:
    """Convert a ResponseData object to a JSON string.

    Args:
        response_data (ResponseData): The ResponseData object to be converted.

    Returns:
        str: The JSON string representation of the ResponseData object.

    """
    return json.dumps(
        response_data, default=lambda o: o.__dict__, ensure_ascii=False, indent=4
    )


# Example usage
# response_data = parse_json('response.json')
# for entry in response_data.data:
#     print(entry)
