from .geosphere_hub import GeosphereAPI
from datetime import datetime, timedelta
import numpy as np


class AROME(GeosphereAPI):
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
    ):
        params = {
            "parameters": parameters,
            "lat_lon": position,
            "forecast_offset": 0,
        }

        res = self._query_dict(params)
        self._last_query[str(params.items())] = res
        self._data = np.array(res["data"], dtype=float)
        self._times = res["timestamps"]
        return str(params.items())
