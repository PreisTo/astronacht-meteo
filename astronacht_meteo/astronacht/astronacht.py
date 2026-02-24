import matplotlib.pyplot as plt
from astronacht_meteo.geosphere_api.arome import AROME


class Astronacht:
    def __init__(self, date="today", location="Technik"):
        self._arome = AROME()

    def get_cloud_plot(self):
        meta_info = self._arome.get_timeseries_data()  # just the defaults here

        fig, ax = plt.subplots(1)
        ax.set_xlabel("Time")
        ax.set_ylabel("Cloudcover [Percentage]")
        ax.set_title(self._arome._last_query[meta_info]["reference_time"])
        ax.plot(self._arome._data)
        fig.show()
