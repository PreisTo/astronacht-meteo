from typing import Optional

import astropy.units as u
from astroplan import Observer


class Location:
    # TODO: add types
    def __init__(self, lon, lat, name: Optional = None, elevation=None, **kwargs):
        self._lon = lon
        self._lat = lat
        self._name = name
        self._elevation = elevation
        self._observer = Observer(longitude=lon * u.deg, latitude=lat * u.deg, **kwargs)

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
        if "elevation" in config_dict.keys():
            elevation = config_dict["elevation"] * u.m
            config_dict.pop("elevation")
        else:
            elevation = None

        lon = config_dict["lon"] * u.deg
        lat = config_dict["lat"] * u.deg
        config_dict.pop("lon")
        config_dict.pop("lat")
        if "name" in config_dict.keys():
            name = config_dict["keys"]
            config_dict.pop("name")
        else:
            name = None
        return cls(lon, lat, name, elevation, **config_dict)
