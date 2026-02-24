#!/usr/bin/python3
from astronacht_meteo.astronacht import Astronacht

if __name__ == "__main__":
    astronacht = Astronacht()
    fig, _ = astronacht.get_cloud_plot()
    fig.show()
