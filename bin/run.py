#!/usr/bin/env python3

from astronacht_meteo.astronacht import Astronacht

if __name__ == "__main__":
    astronacht = Astronacht.from_config("./default_config.yml")
