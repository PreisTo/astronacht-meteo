#!/usr/bin/env python3

from astronacht_meteo.astronacht import Astronacht
import matplotlib.pyplot as plt

if __name__ == "__main__":
    astronacht = Astronacht.from_config("./default_config.yml")

    fig, ax = plt.subplots(
        nrows=2, ncols=2, layout="constrained", figsize=(16, 9), sharex=True
    )
    ax = ax.flatten()
    astronacht.weather.plot_parameter(ax=ax[0], parameter="clouds")
    astronacht.weather.plot_parameter(ax=ax[1], parameter="temperature")
    astronacht.weather.plot_parameter(
        ax=ax[2],
        parameter="relative_humidity",
    )
    astronacht.weather.plot_parameter(
        ax=ax[3],
        parameter="pressure",
    )
    fig.suptitle(f"Last update at {astronacht.weather.ref_time}")
    plt.show()
