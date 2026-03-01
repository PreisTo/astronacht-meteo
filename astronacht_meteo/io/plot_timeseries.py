from datetime import datetime

import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pytz


def get_cloud_plot(arome) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    meta_info = arome.get_timeseries_data()  # just the defaults here

    fig, ax = plt.subplots(1, layout="constrained")

    ax.plot(arome._times, arome._data)

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%m-%d %H:%M", tz=pytz.timezone("Europe/Vienna"))
    )
    ax.tick_params(axis="x", labelrotation=60)
    ax.set_xlabel("Time")
    ax.set_ylabel("Cloudcover [Percentage]")
    ref_time = pytz.UTC.localize(
        datetime.strptime(
            arome._last_query[meta_info]["reference_time"],
            "%Y-%m-%dT%H:%M+00:00",
        )
    ).astimezone(pytz.timezone("Europe/Vienna"))

    ax.set_title("Last update from " + f"{ref_time}" + "UTC")
    ax.legend()

    return fig, ax
