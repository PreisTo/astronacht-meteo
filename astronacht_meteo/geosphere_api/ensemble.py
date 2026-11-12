from .geosphere_hub import GeosphereForecast


class Ensemble(GeosphereForecast):
    """
    The Geosphere Austria ensemble forecast:
    https://data.hub.geosphere.at/dataset/ensemble-v2-1h-1km
    """

    resource_id = "ensemble-v2-1h-1km"
    mode = "forecast"
    default_parameters = ("tcc_p50",)
