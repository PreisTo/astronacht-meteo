from datetime import datetime, timedelta

import astropy.units as u
import numpy as np

from astronacht_meteo.geosphere_api import Ensemble, Nowcast
from astronacht_meteo.io.plot_timeseries import get_weather_plot
from astronacht_meteo.location import Location
from astronacht_meteo.utils.formula import magnus_formula

# TODO:method that gets values for an input time


class Weather:
    def __init__(self, location: Location, date=None):
        self._location = location
        self._ensemble = Ensemble()
        self._get_data_from_ensemble()
        self._date = date
        if self._date is not None:
            dn = datetime.now()
            dn = dn.replace(tzinfo=self._date.timezone)
            if self._date.start_time - dn < timedelta(hours=3):
                self._nowcast = Nowcast()
                self._get_data_from_nowcast()

    def _get_data_from_ensemble(self):
        # Use the median forecast for each parameter.
        parameters = [
            "tcc_p50",
            "tcc_p10",
            "tcc_p90",
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
        self._dewpoint = (
            magnus_formula(self._temperature.value, self._relative_humidity.value)
            * u.Celsius
        )
        self._times = data["times"]
        self._ref_time = data["reference_time"]
        self._wind = np.sqrt(
            np.power(data["10u_p50"], 2) + np.power(data["10v_p50"], 2)
        ) * u.Unit("m/s")
        self._clouds_ensemble = (
            np.array([data["tcc_p10"], data["tcc_p50"], data["tcc_p90"]]) * u.percent
        )
        self._times_ensemble = data["times"]

    def _get_data_from_nowcast(self):
        # clouds, surface pressure, temperature 2m, rel. humidity 2m
        parameters = [
            "rh2m",
            "t2m",
            "td",
        ]
        _query_key, data = self._nowcast.get_timeseries_data(
            parameters=parameters,
            position=f"{self._location.lat},{self._location.lon}",
        )
        assert data is not None
        self._temperature_nc = data["t2m"] * u.Celsius
        self._relative_humidity_nc = data["rh2m"] * u.percent
        self._dew_point_nc = data["td"] * u.Celsius
        self._times_nc = data["times"]
        self._ref_time_nc = data["reference_time"]

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
    def dewpoint(self):
        return self._dewpoint

    @property
    def dewpoint_nc(self):
        if hasattr(self, "_dew_point_nc"):
            return self._dew_point_nc
        else:
            return None

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
        self,
        ax,
        parameter="clouds_ensemble",
        title=False,
        label=None,
        color="grey",
        **kwargs,
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

    def plot_nowcast_parameter(
        self, ax, parameter="dewpoint", title=False, label=None, color="lightblue"
    ):
        ax.plot(
            self._times_nc, self._dew_point_nc, label="Dewpoint Nowcast", color=color
        )
        ymin, ymax = ax.get_ylim()
        if ymin > np.min(self._dew_point_nc).value:
            if np.min(self._dew_point_nc).value > 0:
                ymin = 0.9 * np.min(self._dew_point_nc).value
            else:
                ymin = -np.abs(np.min(self._dew_point_nc)).value * 1.1
        if ymax < np.max(self._dew_point_nc).value:
            if np.max(self._dew_point_nc).value > 0:
                ymax = 1.1 * np.max(self._dew_point_nc).value
            else:
                ymax = -np.abs(np.min(self._dew_point_nc)).value * 0.9
        ax.set_ylim(ymin, ymax)

        return ax
