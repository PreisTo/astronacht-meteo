from datetime import datetime, timezone
from typing import Optional

import pytz

from .location import Location


class Date:
    def __init__(
        self,
        day: datetime,
        start_time,
        duration: Optional[datetime] = None,
        stop_time: Optional[datetime] = None,
        timezone: Optional[timezone] = pytz.timezone("Europe/Vienna"),
    ):
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
                    "The day must be either today, tomorrow or a date "
                    + "specified by dd.mm.yy"
                ) from e
        return cls(day)
