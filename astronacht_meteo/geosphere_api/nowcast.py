from .geosphere_hub import GeosphereAPI


class Nowcast(GeosphereAPI):
    resource_id = "nowcast-v1-15min-1km"
    mode = "forecast"

    def __init__(self, dtype="timeseries"):
        self.dtype = dtype
        self._last_query = {}
        super().__init__()
