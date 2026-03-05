from pathlib import Path
from typing import Optional, Union

from astronacht_meteo.targets import Targets
from astronacht_meteo.utils.config import load_config
from astronacht_meteo.weather import Weather

from .date import Date
from .location import Location

_known_locations = {
    "technik": Location(
        lon=11.342491131078917, lat=47.26435136748764, name="Technik", elevation=600
    ),
    "reith": Location(lat=47.300188, lon=11.203271, name="Reith", elevation=1140),
}


class Astronacht:
    """
    The Astronacht itself.
    It holds all the relevant functions and objects like date and location

    It'll e.g. query the weather APIs to get the forecast
    """

    def __init__(
        self, date=None, location="Technik", targets: Optional[Targets] = None
    ) -> None:
        self._location = self._check_location(location)
        self._date = self._check_date(date)
        self._weather = Weather(location)
        self._targets = targets

    def _check_location(self, location: Union[Location, str]) -> Location:
        if isinstance(location, Location):
            return location
        elif isinstance(location, str):
            if location.lower() in _known_locations.keys():
                return _known_locations[location.lower()]
            else:
                raise ValueError(
                    f"{location} is not a known location... "
                    + f"I know about {_known_locations.keys()}"
                )
        else:
            raise NotImplementedError(
                "You need to provide location as either Location or str"
            )

    def _check_date(self, date: Union[Date, str]) -> Date:
        if isinstance(date, Date):
            return date
        elif isinstance(date, str):
            # TODO: implement from string in Date
            raise NotImplementedError("This is a todo... need to handle that in Date")
        else:
            raise NotImplementedError("You need to provide date as either Date or str")

    @classmethod
    def from_config(cls, config_file: Union[Path, str]):
        config_dict = load_config(config_file)
        location = Location.from_dict(config_dict["location"])
        date = Date.from_config(config_dict["date"], location)
        if "targets" in config_dict.keys():
            targets = Targets.from_config(config_dict["targets"])

        return cls(date=date, location=location, targets=targets)
