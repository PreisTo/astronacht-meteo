from .geosphere_hub import GeosphereAPI


class AROME(GeosphereAPI):
    resource_id = "nwp-v1-1h-2500m"
    mode = "forecast"

    def __init__(self, dtype="timeseries"):
        self.dtype = dtype
        super().__init__()
