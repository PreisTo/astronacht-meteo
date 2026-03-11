#!/usr/bin/env python

from astronacht_meteo.astronacht import Astronacht

if __name__ == "__main__":
    astronacht = Astronacht()
    astronacht.weather.plot_clouds()
