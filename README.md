# Astonacht Meteo

Some tools for helping to decide if its worth to do an "Astronacht".

The API of Geosphere Austria is used for weater data.

This is being developed for the Astronacht outreach event organized by the Department of Astro- and Particle Physics of the University of Innsbruck.

All scripts default to our location and timezone but can be easily changed for your needs :)

## ToDos:
- [ ] add docs
- [ ] add github page/actions to run automatically
- [ ] add some basic tests
- [ ] add meteoblue API - caution only 5000
- [ ] add GUI
- [ ] add script for current situation
- [x] create a config instead of hardcoding defaults
- [ ] find an api that supplies elevation map of tyrol --> get angular blockage --> [Open Elevation](https://open-elevation.com/) or [Google Elevation](https://developers.google.com/maps/documentation/elevation/overview) or [tiris](https://www.tirol.gv.at/statistik-budget/tiris/)
- [ ] weather: check date conditions


## Installation
There is a `environment.yml` for creating a `conda` environment either with `conda` or `mamba`.
It is using `Python=3.14` because who wants outdated Python anyway (usually me...).

```bash
git clone https://github.com/PreisTo/astronacht-meteo.git
cd astronacht-meteo
mamba env create -f environment.yml -n astronacht
mamba activate astronacht
pip install . # install the package
```

## Usage
Modify the config file in `bin` and run the `run.py` within the `bin/` dir:
```bash
./run.py
```
This will give you a quick weather overview.

## Contributing

Contributions are *_very_* welcome!
Please create an issue if you find a bug or have a feature request.
If you want to implement it - even better! Add your changes and create a PR to the `dev` branch :)

## Acknowledgment
Thanks a lot to Geosphere Austria for the free API access!
Also this project makes use of [`astroplan`](https://ui.adsabs.harvard.edu/abs/2018AJ....155..128M/abstract) - which made this way more easier - thanks for all the useful and easy functionalities!
