from .location import Location
from datetime import datetime
import pytz
from typing import Optional


class Date:
    def __init__(self, day: datetime, start_time, duration, stop_time):
        pass

    @classmethod
    def from_dict(cls, config_dict: dict, location: Location):
        if config_dict["day"] == "today":
            day = datetime.today()
        elif config_dict["day"] == "tomorrow":
            day = datetime.day
        else:
            try:
                day = datetime.strptime("%d.%m.%y", config_dict["day"])
            except Exception as e:
                raise TypeError(
                    "The day must be either today, tomorrow or a date specified by dd.mm.yy"
                ) from e
        return cls(day)
