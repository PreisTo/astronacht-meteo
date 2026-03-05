from astropy.coordinates import SkyCoord


class Targets:
    def __init__(self, targets_list: list):
        self._targets = targets_list

    @classmethod
    def from_config(cls, config_dict):
        targets = []
        if "list" in config_dict.keys():
            for el in config_dict["list"]:
                targets.append(SkyCoord.from_name(el))

        return cls(targets)
