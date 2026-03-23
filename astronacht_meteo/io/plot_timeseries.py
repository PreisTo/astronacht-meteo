from typing import TYPE_CHECKING, Optional

import astropy.units as u
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pytz

if TYPE_CHECKING:
    from astronacht_meteo.date import Date
    from astronacht_meteo.weather import Weather


def get_weather_plot(
    weather: "Weather",
    parameter="clouds",
    ax=None,
    title=False,
    date: Optional["Date"] = None,
) -> mpl.axes.Axes:
    if ax is None:
        fig, ax = plt.subplots(1, layout="constrained")
    data = getattr(weather, parameter)
    ax.plot(weather.times, data)
    if isinstance(data, u.Quantity):
        data = data.value

    if np.min(data) < 0:
        y_min = -np.abs(np.min(data)) * 1.1
    else:
        y_min = 0.9 * np.min(data)

    if np.max(data) < 0:
        y_max = -np.abs(np.max(data)) * 0.9
    else:
        y_max = 1.1 * np.max(data)

    ax.set_ylim(y_min, y_max)
    if date is not None:
        ax.fill_between(
            [date.start_time, date.stop_time],
            y_min,
            y_max,
            color="magenta",
            alpha=0.2,
        )

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%m-%d %H:%M", tz=pytz.timezone("Europe/Vienna"))
    )

    ax.tick_params(axis="x", labelrotation=60)
    ax.set_xlabel("Time")
    temp = getattr(weather, parameter)
    if isinstance(temp, u.Quantity):
        ylabel = parameter + f" [{temp.unit}]"
    else:
        ylabel = parameter + " [a.u.]"

    ax.set_ylabel(ylabel)
    ref_time = weather.ref_time

    if title:
        ax.set_title("Last update from " + f"{ref_time}" + "UTC")

    return ax
