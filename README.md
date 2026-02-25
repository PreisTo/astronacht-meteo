# Astonacht Meteo

Some tools for helping to decide if its worth to do an Astronacht.

## ToDos:
- [ ] add docs
- [ ] add github page/actions to run automatically
- [ ] add some basic tests
- [ ] add meteoblue API - caution only 5000

## Installation
There is a `environment.yml` for creating a `conda` environment either with `conda` or `mamba`.
It is using `Python=3.14` because who wants outdated Python anyway (usually me...).

```bash
mamba env create -f environment.yml -n astronacht
mamba activate astronacht
pip install . # install the package
```

## Usage
Basic usage for getting the cloud coverage today at Technik
```bash
./bin/get_cloud_plots.py
```

