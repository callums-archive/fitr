from datetime import (
    datetime,
    date,
    time
)

import time

from pytz import (
    timezone,
    utc
)


def parse_date(date_str):
    """Parses ISO formated date string to datatime object.

    Args:
        date_str: ISO formtted string %Y-%m-%d.

    Returns:
        datetime object

    """
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def parse_time(time_str):
    """Parses time string to time object.

    Args:
        time_str: time string %H:%M.

    Returns:
        time object

    """
    return time.strptime(time_str, '%H:%M')

def parse_datetime(date_str):
    """Parses ISO formated datetime string to datatime object.

    Args:
        date_str: ISO formtted string %Y-%m-%d %H:%M.

    Returns:
        datetime object

    """
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M')

def age_higher(birth_date, age):
    """Compairs birthdate to current date to check for a valid age or higher

    Args:
        birth_date: birthdate(date/datetime obj)
        age: required age(date/datetime obj)

    Returns:
        boolean

    """
    today = date.today()
    if isinstance(birth_date, datetime):
        today = birth_date.date()

    delta = today - birth_date
    if (delta.days / 365) >= age:
        return True
    return False

def age_lower(birth_date, age):
    """Compairs birthdate to current date to check for a valid age or lower

    Args:
        birth_date: birthdate(date/datetime obj)
        age: required age(date/datetime obj)

    Returns:
        boolean

    """
    today = date.today()
    if isinstance(birth_date, datetime):
        today = birth_date.date()

    delta = today - birth_date
    if (delta.days / 365) <= age:
        return True
    return False

def age(birth_date):
    """Get current age

    Args:
        birth_date: birthdate(date/datetime obj)
        age: required age(date/datetime obj)

    Returns:
        boolean

    """
    today = date.today()
    if isinstance(birth_date, datetime):
        today = birth_date.date()

    delta = today - birth_date
    return {
        "days": delta.days,
        "years": int(delta.days / 365)
    }

def cast_string(obj, cast_opt, tz="Africa/Johannesburg"):
    """Converts datetime, time and date objects to formatted ISO strings

    Args:
        obj: date/datetime/time obj
        cast_opt:
            dts - date time seconds
            dt - date time
            d - date
            ts - time seconds
            t - time
        tz: desired timezone

    Returns:
        boolean

    """
    obj = obj.replace(tzinfo=utc).astimezone(timezone(tz))
    if cast_opt == "dts":
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif cast_opt == "dt":
        return obj.strftime("%Y-%m-%d %H:%M")
    elif cast_opt == "d":
        return obj.strftime("%Y-%m-%d")
    elif cast_opt == "ts":
        return obj.strftime("%H:%M:%S")
    elif cast_opt == "t":
        return obj.strftime("%H:%M")
