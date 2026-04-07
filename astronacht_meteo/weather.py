import astropy.units as u
import numpy as np
from datetime import datetime, timedelta


from astronacht_meteo.geosphere_api import AROME, Nowcast, Ensemble
from astronacht_meteo.io.plot_timeseries import get_weather_plot
from astronacht_meteo.location import Location

# TODO:method that gets values for an input time


class Weather:
    def __init__(self, location: Location, date=None):
        self._location = location
        self._arome = AROME()
        self._ensemble = Ensemble()
        self._get_data_from_arome()
        self._get_data_from_ensemble()
        self._date = date
        if self._date is not None:
            dn = datetime.now()
            dn = dn.replace(tzinfo=self._date.timezone)
            if self._date.start_time - dn < timedelta(hours=3):
                self._nowcast = Nowcast()
                self._get_data_from_nowcast()

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

    def _get_data_from_ensemble(self):
        # clouds, surface pressure, temperature 2m, rel. humidity 2m
        parameters = [
            "tcc_p10",
            "tcc_p50",
            "tcc_p90",
            #            "mnt2m_p10",
            #            "mnt2m_p50",
            #            "mnt2m_p90",
            #            "mxt2m_p10",
            #            "mxt2m_p50",
            #            "mxt2m_p90",
            #            "u10m_p10",
            #            "u10m_p50",
            #            "u10m_p90",
            #            "v10m_p10",
            #            "v10m_p50",
            #            "v10m_p90",
        ]
        query_key, data = self._ensemble.get_timeseries_data(
            parameters=parameters,
            position=f"{self._location.lat},{self._location.lon}",
        )
        assert data is not None
        self._clouds_ensemble = (
            np.array([data["tcc_p10"], data["tcc_p50"], data["tcc_p90"]])
            * 100
            * u.percent
        )
        #        self._temperature = data["t2m"] * u.Celsius
        #        self._relative_humidity = data["rh2m"] * u.percent
        self._times_ensemble = data["times"]
        #        self._ref_time = data["reference_time"]
        #        self._wind = np.sqrt(
        #            np.power(data["u10m"], 2) + np.power(data["v10m"], 2)
        #        ) * u.Unit("m/s")

    def _get_data_from_nowcast(self):
        # clouds, surface pressure, temperature 2m, rel. humidity 2m
        parameters = []
        query_key, data = self._nowcast.get_timeseries_data(
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
    def clouds_ensemble(self):
        return self._clouds_ensemble

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

    def plot_parameter(self, ax=None, parameter="clouds", **kwargs):
        ax = get_weather_plot(
            self, ax=ax, parameter=parameter, date=self._date, **kwargs
        )
        return ax

    def plot_ensemble_parameter(
        self, ax, parameter="clouds_ensemble", title=False, label=None, color="grey"
    ):
        ax.plot(
            self._times_ensemble, self._clouds_ensemble[1], label=label, color=color
        )
        ax.fill_between(
            self._times_ensemble,
            self._clouds_ensemble[0],
            self._clouds_ensemble[2],
            label=label,
            color=color,
            alpha=0.2,
        )

        return ax
