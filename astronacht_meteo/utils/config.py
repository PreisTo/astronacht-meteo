import yaml
from pathlib import Path

minimum_keys = {"location": ["name", "lon", "lat"], "date": ["day", "time"]}


def load_config(filename) -> dict:
    if not isinstance(filename, Path):
        filename = Path(filename)

    with filename.open("r") as f:
        config = yaml.safe_load(f)
    for k, v in minimum_keys.items():
        assert k in config.keys(), (
            f"You are missing {k} in your config file. "
            + f"You need to provide at least {minimum_keys}"
        )
        for sk in v:
            assert sk in config[k].keys(), (
                f"You are missing {k}/{sk} in your config file. "
                + f"You need to provide at least {minimum_keys}"
            )
    return config
