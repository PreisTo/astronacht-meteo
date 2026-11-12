import logging
from datetime import datetime

import numpy as np

import requests

log = logging.getLogger(__name__)


class GeosphereAPI:
    """
    Generic class for accessing the API of Geosphere Austria

    Needs to be subclassed.
    Subclasses must provide dtype, mode and resource_id
    """

    host = "https://dataset.api.hub.geosphere.at"
    version = "v1"

    def __init__(self):
        self._check_init_parameters()
        self._url = (
            f"{self.host}/{self.version}/{self.dtype}/{self.mode}/{self.resource_id}"
        )

    def _check_init_parameters(self):
        assert self.dtype is not None
        assert self.mode is not None
        assert self.resource_id is not None

    def _query(self, query_string) -> dict:
        res = requests.get(self._url + "?" + query_string)
        if res.status_code != 200:
            log.error(res)
            raise ValueError

        return res.json()

    def _query_dict(self, params: dict) -> dict:
        res = requests.get(self._url, params=params)
        if res.status_code != 200:
            log.error(self._url)
            log.error(params)
            log.error(res)
            raise ValueError

        return res.json()

    def get_metadata(self) -> None:
        res = requests.get(self._url + "/metadata")
        if res.status_code != 200:
            raise ValueError(
                f"The request failed - got status code {res.status_code}"
                f" on url {self._url}"
            )
        self._metadata = res.json()

    @property
    def metadata(self) -> dict:
        """Returns the metadata for the dataset."""
        if not hasattr(self, "_metadata"):
            self.get_metadata()
        return self._metadata

    @property
    def parameters(self) -> dict:
        """Returns a list of available parameters for the dataset."""
        return self.metadata["parameters"]


class GeosphereForecast(GeosphereAPI):
    default_parameters = ()

    def __init__(self, dtype="timeseries"):
        self.dtype = dtype
        self._last_query = {}
        super().__init__()

    def get_timeseries_data(
        self,
        parameters=None,
        position="47.26435136748764,11.342491131078917",  # VFH
    ) -> tuple[str, dict]:
        if parameters is None:
            parameters = list(self.default_parameters)
        params = {
            "parameters": parameters,
            "lat_lon": position,
            "forecast_offset": 0,
        }
        query_key = str(params.items())
        if query_key not in self._last_query:
            res = self._query_dict(params)
        else:
            res = self._last_query[query_key]
        self._last_query[query_key] = res
        data = {}
        for parameter in parameters:
            data[parameter] = np.array(
                res["features"][0]["properties"]["parameters"][parameter]["data"],
                dtype=float,
            )
        data["times"] = [datetime.fromisoformat(i) for i in res["timestamps"]]
        data["reference_time"] = datetime.fromisoformat(
            res["reference_time"]
        ).astimezone(tz=None)
        return query_key, data

    @property
    def last_query(self) -> dict | None:
        if not hasattr(self, "_last_query"):
            log.info("No query has been run yet - last_query is empty")
            return None
        return self._last_query
