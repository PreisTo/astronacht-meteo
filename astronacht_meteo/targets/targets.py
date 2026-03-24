import warnings
from astropy.coordinates import SkyCoord, get_body
from astroplan import FixedTarget
from astropy.time import Time
import matplotlib.pyplot as plt
from astroplan.plots import plot_airmass


class Targets:
    def __init__(self, targets_list: list, observer=None, date=None):
        self._targets = targets_list
        if observer is not None:
            self._observer = observer
        if date is not None:
            self._date = date

    def get_airmass_plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(1)
        for target in self._targets:
            plot_airmass(
                target,
                self._observer,
                Time(self._date.start_time + self._date.duration / 2),
                altitude_yaxis=True,
                ax=ax,
            )
        ax.fill_between(
            [
                Time(self._date.start_time).datetime64,
                Time(self._date.stop_time).datetime64,
            ],
            3.0,
            1.0,
            color="magenta",
            alpha=0.2,
        )

        return ax

    @classmethod
    def from_dict(cls, config_dict, **kwargs):
        observer = kwargs.get("observer", None)
        date = kwargs.get("date", None)
        targets = []
        if "list" in config_dict.keys():
            for el in config_dict["list"]:
                if el not in ["saturn", "jupiter"]:
                    targets.append(FixedTarget(SkyCoord.from_name(el), name=el))
                else:
                    if observer is not None and date is not None:
                        targets.append(
                            FixedTarget(
                                get_body(
                                    el,
                                    time=Time(date.start_time),
                                    location=observer.location,
                                ),
                                name=el,
                            )
                        )
                    else:
                        warnings.warn(f"No date and observer passed - will skip {el}")

        return cls(targets, **kwargs)
