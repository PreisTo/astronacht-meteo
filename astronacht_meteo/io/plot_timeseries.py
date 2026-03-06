import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pytz

from astronacht_meteo.weather import Weather


def get_cloud_plot(weather: Weather) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    fig, ax = plt.subplots(1, layout="constrained")

    ax.plot(weather._times, weather._data)

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%m-%d %H:%M", tz=pytz.timezone("Europe/Vienna"))
    )
    ax.tick_params(axis="x", labelrotation=60)
    ax.set_xlabel("Time")
    ax.set_ylabel("Cloudcover [Percentage]")
    ref_time = weather.ref_time

    ax.set_title("Last update from " + f"{ref_time}" + "UTC")
    ax.legend()

    return fig, ax
