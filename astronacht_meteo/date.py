from datetime import datetime, timedelta, timezone
from typing import Optional

import pytz

from .location import Location


class Date:
    def __init__(
        self,
        day: datetime,
        start_time: datetime,
        duration: Optional[timedelta] = None,
        stop_time: Optional[datetime] = None,
        timezone: Optional[timezone] = pytz.timezone("Europe/Vienna"),
    ):
        # TODO: what todo if no duration or stop_time defined? Sunrise?
        self._day = day
        self._start_time = start_time
        if duration is not None:
            self._stop_time = self._start_time + duration
        if stop_time is not None:
            self._stop_time = stop_time
            duration = self._stop_time - self._start_time
        self._duration = duration
        self._start_time.replace(tzinfo=timezone)
        self._stop_time.replace(tzinfo=timezone)
        self._timezone = timezone

    @property
    def day(self):
        return self._day

    @property
    def start_time(self):
        return self._start_time

    @property
    def stop_time(self):
        return self._stop_time

    @classmethod
    def from_dict(cls, config_dict: dict, location: Location):

        if config_dict["day"].lower() == "today":
            day = datetime.today()
        elif config_dict["day"].lower() == "tomorrow":
            day = datetime.day
        else:
            try:
                day = datetime.strptime("%d.%m.%y", config_dict["day"])
            except Exception as e:
                raise TypeError(
                    "The day must be either today, tomorrow or a date "
                    + "specified by dd.mm.yy"
                ) from e

        if config_dict["start_time"].lower() == "earliest":
            raise NotImplementedError
        else:
            try:
                start_time = datetime.strptime("%H:%M", config_dict["start_time"])

            except Exception as e:
                raise TypeError(
                    "The start_time must be either earliest or" + "specified by hh:mm"
                ) from e

        if "start_time" in config_dict.keys():
            if config_dict["stop_time"].lower() == "latest":
                raise NotImplementedError
            else:
                try:
                    stop_time = datetime.strptime("%H:%M", config_dict["stop_time"])

                except Exception as e:
                    raise TypeError(
                        "The stop_time must be either latest or" + "specified by hh:mm"
                    ) from e
        else:
            stop_time = None

        if "duration" in config_dict.keys():
            duration = timedelta(minutes=float(config_dict["duration"]))
        else:
            duration = None

        if "timezone" in config_dict.keys():
            timezone = pytz.timezone(config_dict["timezone"])
        else:
            timezone = pytz.timezone("Europe/Vienna")

        return cls(
            day=day,
            start_time=start_time,
            stop_time=stop_time,
            duration=duration,
            timezone=timezone,
        )
