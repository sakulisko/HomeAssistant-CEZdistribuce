"""data for continuous measurement.

Source data: https://www.cezdistribuce.cz/file/edee/distribuce/cezdistribuce_pasmaplatnostintavt_prubehove_mereni.pdf
Database form: 2024-03-19
"""

import logging

from .response import DataEntry, ResponseData

_LOGGER = logging.getLogger(__name__)


class ContinuousMeasurement:
    "hold data for this type of measurement."

    @staticmethod
    def isContinuousCode():
        "List all codes in defined in this type."
        return ContinuousMeasurement.CODES.keys()

    @staticmethod
    def getCode(code: str) -> ResponseData | None:
        "Return specific dict for code or empty dict if code not exists."
        return ContinuousMeasurement.CODES.get(code)

    AKU8V1: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="19:00",
        CAS_VYP_2="21:00",
    )
    AKU8V2: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="5:00",
        CAS_ZAP_2="18:00",
        CAS_VYP_2="20:00",
        CAS_ZAP_3="23:00",
        CAS_VYP_3="23:59",
    )
    AKU8V3: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="4:00",
        CAS_ZAP_2="17:00",
        CAS_VYP_2="19:00",
        CAS_ZAP_3="22:00",
        CAS_VYP_3="23:59",
    )
    AKU8V4: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="22:00",
        CAS_VYP_2="23:59",
    )
    AKU8V5: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="1:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="18:00",
        CAS_VYP_2="21:00",
    )
    AKU8V6: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="3:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="15:00",
        CAS_VYP_2="18:00",
        CAS_ZAP_3="21:00",
        CAS_VYP_3="23:00",
    )
    EMOV1: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="2:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="22:00",
        CAS_VYP_2="23:00",
    )
    AKU16V1: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="8:00",
        CAS_ZAP_2="13:00",
        CAS_VYP_2="16:00",
        CAS_ZAP_3="19:00",
        CAS_VYP_3="23:59",
    )
    PTV1: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="9:00",
        CAS_ZAP_2="10:00",
        CAS_VYP_2="11:00",
        CAS_ZAP_3="12:00",
        CAS_VYP_3="13:00",
        CAS_ZAP_4="14:00",
        CAS_VYP_4="16:00",
        CAS_ZAP_5="17:00",
        CAS_VYP_5="23:59",
    )
    PTV2: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="7:00",
        CAS_VYP_2="9:00",
        CAS_ZAP_3="10:00",
        CAS_VYP_3="13:00",
        CAS_ZAP_4="14:00",
        CAS_VYP_4="16:00",
        CAS_ZAP_5="17:00",
        CAS_VYP_5="23:59",
    )
    PTV3: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="8:00",
        CAS_ZAP_2="9:00",
        CAS_VYP_2="12:00",
        CAS_ZAP_3="13:00",
        CAS_VYP_3="15:00",
        CAS_ZAP_4="16:00",
        CAS_VYP_4="19:00",
        CAS_ZAP_5="20:00",
        CAS_VYP_5="23:59",
    )
    PTV4: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="10:00",
        CAS_ZAP_2="11:00",
        CAS_VYP_2="12:00",
        CAS_ZAP_3="13:00",
        CAS_VYP_3="14:00",
        CAS_ZAP_4="15:00",
        CAS_VYP_4="17:00",
        CAS_ZAP_5="18:00",
        CAS_VYP_5="23:59",
    )
    EVV1: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="7:00",
        CAS_VYP_2="9:00",
        CAS_ZAP_3="10:00",
        CAS_VYP_3="13:00",
        CAS_ZAP_4="14:00",
        CAS_VYP_4="16:00",
        CAS_ZAP_5="17:00",
        CAS_VYP_5="23:59",
    )
    EVV2: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="8:00",
        CAS_ZAP_2="9:00",
        CAS_VYP_2="12:00",
        CAS_ZAP_3="13:00",
        CAS_VYP_3="15:00",
        CAS_ZAP_4="16:00",
        CAS_VYP_4="19:00",
        CAS_ZAP_5="20:00",
        CAS_VYP_5="23:59",
    )
    EVV3: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="10:00",
        CAS_ZAP_2="11:00",
        CAS_VYP_2="12:00",
        CAS_ZAP_3="13:00",
        CAS_VYP_3="14:00",
        CAS_ZAP_4="15:00",
        CAS_VYP_4="17:00",
        CAS_ZAP_5="18:00",
        CAS_VYP_5="23:59",
    )
    TCV1: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="9:00",
        CAS_ZAP_2="10:00",
        CAS_VYP_2="12:00",
        CAS_ZAP_3="13:00",
        CAS_VYP_3="23:59",
    )
    CHLV1: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="3:00",
        CAS_VYP_1="23:00",
    )
    CHLV2: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="4:00",
        CAS_ZAP_2="6:00",
        CAS_VYP_2="22:00",
    )
    CHLV3: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="4:30",
        CAS_ZAP_2="8:30",
        CAS_VYP_2="23:59",
    )
    CHLV4: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="14:00",
        CAS_ZAP_2="18:00",
        CAS_VYP_2="23:59",
    )
    ZAV1_WORK: DataEntry = DataEntry(
        PLATNOST="Po - Pa",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="10:00",
        CAS_VYP_2="23:59",
    )
    ZAV1_WEEK: DataEntry = DataEntry(
        PLATNOST="So - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="23:59",
    )
    ZAV2_WORK: DataEntry = DataEntry(
        PLATNOST="Po - Pa",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="3:00",
        CAS_ZAP_2="7:00",
        CAS_VYP_2="23:59",
    )
    ZAV2_WEEK: DataEntry = DataEntry(
        PLATNOST="So - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="23:59",
    )
    VIKV1_1: DataEntry = DataEntry(
        PLATNOST="Pa - Pa",
        CAS_ZAP_1="12:00",
        CAS_VYP_1="23:59",
    )
    VIKV1_2: DataEntry = DataEntry(
        PLATNOST="So - So",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="23:59",
    )
    VIKV1_3: DataEntry = DataEntry(
        PLATNOST="Ne - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="22:00",
    )
    VYRV1: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="6:00",
        CAS_ZAP_2="10:00",
        CAS_VYP_2="16:00",
        CAS_ZAP_3="20:00",
        CAS_VYP_3="23:59",
    )
    VYRV2: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="7:00",
        CAS_ZAP_2="15:00",
        CAS_VYP_2="23:59",
    )
    VYRV3: DataEntry = DataEntry(
        PLATNOST="Po - Ne",
        CAS_ZAP_1="0:00",
        CAS_VYP_1="7:00",
        CAS_ZAP_2="10:00",
        CAS_VYP_2="18:00",
        CAS_ZAP_3="23:00",
        CAS_VYP_3="23:59",
    )

    # define global data with all continuous measurements
    CODES: dict[str, ResponseData] = {
        "AKU8V1": ResponseData([AKU8V1]),
        "AKU8V2": ResponseData([AKU8V2]),
        "AKU8V3": ResponseData([AKU8V3]),
        "AKU8V4": ResponseData([AKU8V4]),
        "AKU8V5": ResponseData([AKU8V5]),
        "AKU8V6": ResponseData([AKU8V6]),
        "EMOV1": ResponseData([EMOV1]),
        "AKU16V1": ResponseData([AKU16V1]),
        "PTV1": ResponseData([PTV1]),
        "PTV2": ResponseData([PTV2]),
        "PTV3": ResponseData([PTV3]),
        "PTV4": ResponseData([PTV4]),
        "EVV1": ResponseData([EVV1]),
        "EVV2": ResponseData([EVV2]),
        "EVV3": ResponseData([EVV3]),
        "TCV1": ResponseData([TCV1]),
        "CHLV1": ResponseData([CHLV1]),
        "CHLV2": ResponseData([CHLV2]),
        "CHLV3": ResponseData([CHLV3]),
        "CHLV4": ResponseData([CHLV4]),
        "ZAV1": ResponseData([ZAV1_WORK, ZAV1_WEEK]),
        "ZAV2": ResponseData([ZAV2_WORK, ZAV2_WEEK]),
        "VIKV1": ResponseData([VIKV1_1, VIKV1_2, VIKV1_3]),
        "VYRV1": ResponseData([VYRV1]),
        "VYRV2": ResponseData([VYRV2]),
        "VYRV3": ResponseData([VYRV3]),
    }
