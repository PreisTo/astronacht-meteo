#!/usr/bin/env python
import matplotlib.pyplot as plt

from astronacht_meteo.astronacht import Astronacht

if __name__ == "__main__":
    astronacht = Astronacht()
    fig, ax = astronacht.get_cloud_plot()
    plt.show()
