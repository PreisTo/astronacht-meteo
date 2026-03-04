from astronacht_meteo.geosphere_api.arome import AROME
from astronacht_meteo.location import Location


class Weather:
    def __init__(self, location: Location):
        self._location = location
        self._arome = AROME()

    def _get_data_from_arome(self):
        # clouds
        parameters = [
            "tcc",
            "sp",
            "t2m",
            "rh2m",
        ]
        response = self._arome.get_timeseries_data(
            parameters=parameters,
            position=f"{self._location.lat},{self._location.lat}",
        )
        assert response is not None

    @property
    def clouds(self):
        pass

    @property
    def relative_humidity(self):
        pass

    @property
    def wind(self):
        pass

    @property
    def pressure(self):
        pass
