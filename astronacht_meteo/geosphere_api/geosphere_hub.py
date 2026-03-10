import logging

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
        pass

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
            raise ValueError(f"The request failed - got status code {res.status_code}")
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
