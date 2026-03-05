from astronacht_meteo.geosphere_api.arome import AROME
from astronacht_meteo.location import Location


class Weather:
    def __init__(self, location: Location):
        self._location = location
        self._arome = AROME()
        self._get_data_from_arome()

    def _get_data_from_arome(self):
        # clouds, surface pressure, temperature 2m, rel. humidity 2m
        parameters = [
            "tcc",
            "sp",
            "t2m",
            "rh2m",
        ]
        query_key, data = self._arome.get_timeseries_data(
            parameters=parameters,
            position=f"{self._location.lat},{self._location.lat}",
        )
        assert data is not None
        self._clouds = data["tcc"]
        self._pressure = data["sp"]
        self._temperature = data["t2m"]
        self._relative_humidity = data["rh2m"]
        self._times = data["times"]

    @property
    def clouds(self):
        return self._clouds

    @property
    def relative_humidity(self):
        return self._relative_humidity

    @property
    def temperature(self):
        return self._temperature

    @property
    def pressure(self):
        return self._pressure

    @property
    def times(self):
        return self._times
