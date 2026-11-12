from .geosphere_hub import GeosphereForecast


class NWPV2(GeosphereForecast):
    resource_id = "nwp-v2-1h-1km"
    mode = "forecast"
    default_parameters = ("tcc",)
