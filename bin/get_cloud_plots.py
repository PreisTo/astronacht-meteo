#!/usr/bin/env python
from astronacht_meteo.astronacht import Astronacht
import matplotlib.pyplot as plt

if __name__ == "__main__":
    astronacht = Astronacht()
    fig, ax = astronacht.get_cloud_plot()
    plt.show()
