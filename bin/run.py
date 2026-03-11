#!/usr/bin/env python3

from astronacht_meteo.astronacht import Astronacht
from datetime import datetime
import matplotlib.pyplot as plt
import pytz

if __name__ == "__main__":
    astronacht = Astronacht.from_config("./default_config.yml")
    fig, ax = plt.subplots(nrows=2, ncols=2, layout="constrained", figsize=(16, 9))
    ax = ax.flatten()

    astronacht.weather.plot_parameter(ax=ax[0])
    astronacht.weather.plot_parameter(ax=ax[1], parameter="temperature", title=False)
    astronacht.weather.plot_parameter(
        ax=ax[2], parameter="relative_humidity", title=False
    )
    astronacht.weather.plot_parameter(ax=ax[3], parameter="pressure", title=False)

    fig.savefig("test.png")
