import logging
from datetime import datetime
from typing import Tuple

import numpy as np

from .geosphere_hub import GeosphereAPI

log = logging.getLogger(__name__)


class AROME(GeosphereAPI):
    """
    The AROME high resolution model:
    Application of Research to Operations at MEsoscale
    https://data.hub.geosphere.at/dataset/nwp-v1-1h-2500m
    """

    resource_id = "nwp-v1-1h-2500m"
    mode = "forecast"

    def __init__(self, dtype="timeseries"):
        self.dtype = dtype
        self._last_query = {}
        super().__init__()

    def get_timeseries_data(
        self,
        parameters=["tcc"],
        position="47.26435136748764,11.342491131078917",  # VFH
    ) -> Tuple[str, dict]:
        params = {
            "parameters": parameters,
            "lat_lon": position,
            "forecast_offset": 0,
        }
        if not str(params.items()) in self._last_query.keys():
            res = self._query_dict(params)
        else:
            res = self._last_query[str(params.items())]
        self._last_query[str(params.items())] = res
        data = {}
        for i, p in enumerate(parameters):
            data[p] = np.array(
                res["features"][0]["properties"]["parameters"][p]["data"],
                dtype=float,
            )
        times = [datetime.fromisoformat(i) for i in res["timestamps"]]
        data["times"] = times
        data["reference_time"] = datetime.fromisoformat(
            res["reference_time"]
        ).astimezone(tz=None)
        return str(params.items()), data

    @property
    def last_query(self) -> dict | None:
        """
        Returns the last_query dict.
        Caution - the keys are dicts
        """
        # TODO: store in some cache file?
        if not hasattr(self, "_last_query"):
            log.info("No query has been run yet - last_query is empty")
            return None
        return self._last_query
