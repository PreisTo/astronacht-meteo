import requests


class GeosphereAPI:
    host = "https://dataset.api.hub.geosphere.at"
    version = "v1"

    def __init__(self):
        self._check_parameters()
        self._url = (
            f"{self.host}/{self.version}/{self.dtype}/{self.mode}/{self.resource_id}"
        )
        pass

    def _check_parameters(self):
        assert self.dtype is not None
        assert self.mode is not None
        assert self.resource_id is not None

    def _query(self, query_string):
        res = requests.get(self._url + "?" + query_string)
        print(res.status_code)
        print(res.json())

    def get_metadata(self):
        res = requests.get(self._url + "/metadata")
        if res.status_code != 200:
            raise ValueError(f"The request failed - got status code {res.status_code}")
        self._metadata = res.json()

    @property
    def metadata(self):
        """Returns the metadata for the dataset."""
        if not hasattr(self, "_metadata"):
            self.get_metadata()
        return self._metadata

    @property
    def parameters(self):
        """Returns a list of available parameters for the dataset."""
        return self.metadata["parameters"]
