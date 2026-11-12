import astropy.units as u
import numpy as np

from astronacht_meteo.geosphere_api.ensemble import Ensemble
from astronacht_meteo.io.plot_timeseries import get_weather_plot
from astronacht_meteo.location import Location

# TODO:method that gets values for an input time


class Weather:
    def __init__(self, location: Location, date=None):
        self._location = location
        self._ensemble = Ensemble()
        self._get_data_from_ensemble()
        self._date = date

    def _get_data_from_ensemble(self):
        # Use the median forecast for each parameter.
        parameters = [
            "tcc_p50",
            "msl_p50",
            "2t_p50",
            "2r_p50",
            "10u_p50",
            "10v_p50",
        ]
        _, data = self._ensemble.get_timeseries_data(
            parameters=parameters,
            position=f"{self._location.lat},{self._location.lon}",
        )
        assert data is not None
        self._clouds = data["tcc_p50"] * u.percent
        self._pressure = data["msl_p50"] * u.Pa
        self._temperature = data["2t_p50"] * u.Celsius
        self._relative_humidity = data["2r_p50"] * u.percent
        self._times = data["times"]
        self._ref_time = data["reference_time"]
        self._wind = np.sqrt(
            np.power(data["10u_p50"], 2) + np.power(data["10v_p50"], 2)
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
