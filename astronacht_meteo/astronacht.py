from typing import Union
from .date import Date
from .location import Location
from astronacht_meteo.weather import Weather
from astronacht_meteo.utils.config import load_config
from pathlib import Path


class Astronacht:
    """
    The Astronacht itself.
    It holds all the relevant functions and objects like date and location

    It'll e.g. query the weather APIs to get the forecast
    """

    def __init__(self, date=None, location="Technik") -> None:
        self._weather = Weather(location)

    @classmethod
    def from_config(cls, config_file: Union[Path, str]):
        config_dict = load_config(config_file)
        location = Location.from_dict(config_dict["location"])
        date = Date.from_config(config_dict["date"], location)

        return cls(date=date, location=location)
