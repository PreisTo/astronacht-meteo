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
        self._start_time = start_time
        self._day = day
        if duration is not None:
            self._stop_time = self._start_time + duration
        if stop_time is not None:
            duration = self._stop_time - self._start_time
        self._duration = duration
        self._timezone = timezone

    @property
    def timezone(self):
        return self._timezone

    @property
    def day(self):
        return self._day

    @property
    def start_time(self):
        return self._start_time

    @property
    def stop_time(self):
        return self._stop_time

    @property
    def duration(self):
        return self._duration

    @classmethod
    def from_dict(cls, config_dict: dict, location: Location):
        # TODO: this is a mess

        if config_dict["day"].lower() == "today":
            day = datetime.today().strftime("%d.%m.%Y")
        elif config_dict["day"].lower() == "tomorrow":
            day = (datetime.today() + timedelta(days=1)).strfimte("%d.%m.%Y")
        else:
            try:
                datetime.strptime(config_dict["day"], "%d.%m.%Y")
                day = config_dict["day"]
            except Exception as e:
                raise TypeError(
                    "The day must be either today, tomorrow or a date "
                    + "specified by dd.mm.yy"
                ) from e

        if config_dict["start_time"].lower() == "earliest":
            raise NotImplementedError
        else:
            try:
                datetime.strptime(config_dict["start_time"], "%H:%M")
                start_time = config_dict["start_time"]

            except Exception as e:
                raise TypeError(
                    "The start_time must be either earliest or" + "specified by hh:mm"
                ) from e

        if "stop_time" in config_dict.keys():
            if config_dict["stop_time"].lower() == "latest":
                raise NotImplementedError
            else:
                try:
                    datetime.strptime("%H:%M", config_dict["stop_time"])
                    stop_time = config_dict["stop_time"]

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
        start_time = day + "-" + start_time
        if stop_time is not None:
            stop_time = day + "-" + stop_time
            if duration is not None:
                duration = datetime.strptime(
                    stop_time, "%d.%m.%Y-%H:%M"
                ) - datetime.strptime(start_time, "%d.%m.%Y-%H:%M")
        elif duration is not None:
            stop_time = datetime.strptime(start_time, "%d.%m.%Y-%H:%M") + duration
        start_time = datetime.strptime(start_time, "%d.%m.%Y-%H:%M")

        if "timezone" in config_dict.keys():
            timezone = pytz.timezone(config_dict["timezone"])
        else:
            timezone = pytz.timezone("Europe/Vienna")
        start_time = start_time.replace(tzinfo=timezone)
        stop_time = stop_time.replace(tzinfo=timezone)

        return cls(
            day=day,
            start_time=start_time,
            stop_time=stop_time,
            duration=duration,
            timezone=timezone,
        )
