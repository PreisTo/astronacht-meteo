import logging
from typing import Optional

import astropy.units as u
from astroplan import Observer

log = logging.getLogger(__name__)


class Location:
    def __init__(self, lon, lat, name: Optional = None, elevation=None, **kwargs):
        self._lon = lon
        self._lat = lat
        self._name = name
        self._elevation = elevation
        self._observer = Observer(
            longitude=lon * u.deg, latitude=lat * u.deg, name=self._name, **kwargs
        )

    def set_weather_conditions(self):
        raise NotImplementedError

    @property
    def observer(self) -> Observer:
        return self._observer

    @property
    def lon(self):
        return self._lon

    @property
    def lat(self):
        return self._lat

    @classmethod
    def from_dict(cls, config_dict: dict):
        if "name" in config_dict.keys():
            name = config_dict["name"]
            config_dict.pop("name")
            if name.lower() in _known_locations.keys():
                if len(config_dict.keys()) < 2:
                    log.warning(
                        f"Only have name '{name}' in location config"
                        + " corresponding to a knwon location - will use it"
                    )
                    return _known_locations[name.lower()]
        else:
            name = None

        if "elevation" in config_dict.keys():
            elevation = config_dict["elevation"]
            config_dict.pop("elevation")
        else:
            elevation = None
        lon = config_dict["lon"]
        lat = config_dict["lat"]
        config_dict.pop("lon")
        config_dict.pop("lat")
        return cls(lon, lat, name, elevation, **config_dict)


_known_locations = {
    "technik": Location(
        lon=11.342491131078917, lat=47.26435136748764, name="Technik", elevation=600
    ),
    "reith": Location(lat=47.300188, lon=11.203271, name="Reith", elevation=1140),
    "hafelekar": Location(lat=47.312657, lon=11.383711, name="Reith", elevation=2282),
}
