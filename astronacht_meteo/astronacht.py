from typing import Union
from .date import Date
from .location import Location
from astronacht_meteo.geosphere_api.arome import AROME
from .targets.targets import GoodTargets
from astronacht_meteo.utils.config import load_config
from pathlib import Path


class Astronacht:
    """
    The Astronacht itself.
    It holds all the relevant functions and objects like date and location

    It'll query the weather APIs to get the forecast
    """

    def __init__(self, date=None, location="Technik") -> None:
        self._arome = AROME()

    @classmethod
    def from_config(cls, config_file: Union[Path, str]):
        config_dict = load_config(config_file)
        date = Date.from_config(config_dict["date"])
        location = Location.from_dict(config_dict["location"])
        if config_dict["targets"]["auto"]:
            good_targets = GoodTargets.from_dict()

        return cls(date=date, location=location)
