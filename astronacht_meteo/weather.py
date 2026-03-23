import astropy.units as u
import numpy as np

from astronacht_meteo.geosphere_api.arome import AROME
from astronacht_meteo.io.plot_timeseries import get_weather_plot
from astronacht_meteo.location import Location


class Weather:
    def __init__(self, location: Location, date=None):
        self._location = location
        self._arome = AROME()
        self._get_data_from_arome()
        self._date = date

    def _get_data_from_arome(self):
        # clouds, surface pressure, temperature 2m, rel. humidity 2m
        parameters = [
            "tcc",
            "sp",
            "t2m",
            "rh2m",
            "u10m",
            "v10m",
        ]
        query_key, data = self._arome.get_timeseries_data(
            parameters=parameters,
            position=f"{self._location.lat},{self._location.lon}",
        )
        assert data is not None
        self._clouds = data["tcc"] * 100 * u.percent
        self._pressure = data["sp"] * u.Pa
        self._temperature = data["t2m"] * u.Celsius
        self._relative_humidity = data["rh2m"] * u.percent
        self._times = data["times"]
        self._ref_time = data["reference_time"]
        self._wind = np.sqrt(
            np.power(data["u10m"], 2) + np.power(data["v10m"], 2)
        ) * u.Unit("m/s")

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
        return self._pressure.to(u.Unit("hPa"))

    @property
    def wind(self):
        return self._wind

    @property
    def times(self):
        return self._times

    @property
    def ref_time(self):
        return self._ref_time

    def plot_parameter(self, ax=None, parameter="clouds", title=False):
        ax = get_weather_plot(
            self, ax=ax, parameter=parameter, title=title, date=self._date
        )
        return ax
