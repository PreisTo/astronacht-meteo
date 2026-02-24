import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from astronacht_meteo.geosphere_api.arome import AROME


class Astronacht:
    def __init__(self, date="today", time="19:00", location="Technik"):
        self._create_date()
        self._arome = AROME()

    def get_cloud_plot(self):
        meta_info = self._arome.get_timeseries_data()  # just the defaults here

        fig, ax = plt.subplots(1, layout="constrained")

        ax.plot(self._arome._times + np.timedelta64(1, "h"), self._arome._data)

        ax = self._add_observation_start_stop()
        ax = self._add_sunset_sunrise()

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.tick_params(axis="x", labelrotation=60)
        ax.set_xlabel("Time")
        ax.set_ylabel("Cloudcover [Percentage]")
        ax.set_title(
            "Last update from "
            + f'{np.datetime64(self._arome._last_query[meta_info]["reference_time"])}'
            + "UTC"
        )
        return fig, ax

    def _add_sunset_sunrise(self, ax):
        pass

    def _add_observation_start_stop(self, ax):
        pass
