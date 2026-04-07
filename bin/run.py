#!/usr/bin/env python3

import matplotlib.pyplot as plt

import pathlib
from astronacht_meteo.astronacht import Astronacht

if __name__ == "__main__":
    script_directory = pathlib.Path(__file__).parent.resolve()
    astronacht = Astronacht.from_config(script_directory / "default_config.yml")

    fig, ax = plt.subplots(
        nrows=2, ncols=2, layout="constrained", figsize=(16, 9), sharex=True
    )
    ax = ax.flatten()
    astronacht.weather.plot_parameter(
        ax=ax[0], parameter="clouds", color="black", label="AROME"
    )
    astronacht.weather.plot_ensemble_parameter(
        ax=ax[0], parameter="clouds_ensemble", label="Ensemble"
    )
    ax[0].legend()

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
    if len(astronacht.targets.targets) > 0:
        fig2, ax = plt.subplots(1, layout="constrained", figsize=(16, 9))
        ax = astronacht.targets.get_airmass_plot(ax=ax)
        ax.legend()
    plt.show()
