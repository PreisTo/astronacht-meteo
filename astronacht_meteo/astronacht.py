import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from astronacht_meteo.geosphere_api.arome import AROME
from datetime import datetime, timedelta
import pytz


class Astronacht:
    def __init__(self, date=None, time=None, location="Technik") -> None:
        self._create_date(date, time)
        self._arome = AROME()

    def _create_date(self, date, time) -> None:
        tz = pytz.timezone("Europe/Vienna")
        self._observation_time = None
        if date is None and time is None:
            date = datetime.date(datetime.today())
            time = "19:00"
        elif date is not None and time is None:
            raise NotImplementedError()
        elif date is not None and time is not None:
            raise NotImplementedError()

        temp_date = datetime.strptime(
            datetime.date(datetime.today()).strftime("%y%m%d") + "-" + time,
            "%y%m%d-%H:%M",
        )
        temp_date = tz.localize(temp_date)

        temp_date += timedelta(days=2 - temp_date.weekday())
        self._observation_time = temp_date

    def get_cloud_plot(self) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
        meta_info = self._arome.get_timeseries_data()  # just the defaults here

        fig, ax = plt.subplots(1, layout="constrained")

        ax.plot(self._arome._times, self._arome._data)

        ax = self._add_observation_start_stop(ax)
        ax = self._add_sunset_sunrise(ax)

        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%m-%d %H:%M", tz=pytz.timezone("Europe/Vienna"))
        )
        ax.tick_params(axis="x", labelrotation=60)
        ax.set_xlabel("Time")
        ax.set_ylabel("Cloudcover [Percentage]")
        ref_time = pytz.UTC.localize(
            datetime.strptime(
                self._arome._last_query[meta_info]["reference_time"],
                "%Y-%m-%dT%H:%M+00:00",
            )
        ).astimezone(pytz.timezone("Europe/Vienna"))

        ax.set_title("Last update from " + f"{ref_time}" + "UTC")
        ax.legend()

        return fig, ax

    def _add_sunset_sunrise(self, ax: mpl.axes.Axes) -> mpl.axes.Axes:
        ax.vlines(
            self._observation_time,
            0,
            1,
            linestyles="dashed",
            label="Astronacht Beginn",
            colors="red",
        )
        return ax

    def _add_observation_start_stop(self, ax: mpl.axes.Axes) -> mpl.axes.Axes:

        return ax
