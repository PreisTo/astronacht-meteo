import logging

import numpy as np

from astronacht_meteo.utils.distance import angular_distance_fast_rad

from .geosphere_hub import GeosphereAPI

log = logging.getLogger(__name__)


class TAWES(GeosphereAPI):
    resource_id = "tawes-v1-10min"
    mode = "current"

    def __init__(self, dtype="station"):
        self.dtype = dtype
        self._last_query = {}
        super().__init__()

    def get_closest_station(self, lon, lat):
        stations = self.metadata["stations"]
        lon = np.deg2rad(lon)
        lat = np.deg2rad(lat)
        lons = np.empty(len(stations), dtype=float)
        lats = np.empty(len(stations), dtype=float)
        ids = np.empty(len(stations), dtype=str)

        for i, s in enumerate(stations):
            lons[i] = float(s["lon"])
            lats[i] = float(s["lat"])
            ids[i] = s["id"]
        lons = np.deg2rad(lons)
        lats = np.deg2rad(lats)
        distances = np.abs(angular_distance_fast_rad(lon, lat, lons, lats))
        ids_sorted = np.argsort(distances)
        log.warning(
            "The closes stations to you are "
            + [stations[i]["name"] for i in ids_sorted[:3]]
        )
        self._closest_station = stations[ids_sorted[0]]
        self._near_stations = stations[ids_sorted[:3]]

    def get_current_data(self, parameters=[], position=None, station=None):
        if position is None and station is None and not hasattr(self, "_station"):

            pass
