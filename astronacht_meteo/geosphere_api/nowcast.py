from datetime import datetime

import numpy as np

from .geosphere_hub import GeosphereAPI


class Nowcast(GeosphereAPI):
    resource_id = "nowcast-v1-15min-1km"
    mode = "forecast"

    def __init__(self, dtype="timeseries"):
        self.dtype = dtype
        self._last_query = {}
        super().__init__()

    def get_timeseries_data(
        self,
        parameters=["td"],
        position="47.26435136748764,11.342491131078917",  # VFH
    ):
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
