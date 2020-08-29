from datetime import datetime
import dateutil.parser


def arrayToString(stringlist): 
    if len(stringlist) == 0:
        return ""

    result = ""
    for oneString in stringlist: 
        result += (oneString + ",")

    return result


def stringToArray(stringValue):
    if stringValue is None or len(stringValue) == 0:
        return [""]

    if "," in stringValue:
        return stringValue.split(",")
    else:
        return [stringValue]


def format_datetime(date_str):
    format = "%Y-%m-%d"
    return datetime.strptime(date_str, format)


def dateTimeToString(dateTime):
    format="%Y-%m-%d"
    return dateTime.strftime(format)