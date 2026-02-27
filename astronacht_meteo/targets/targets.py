from astroplan import FixedTarget, Observer
from astropy.time import Time


class GoodTargets:
    """
    Gives you some good targets for a time range and and a observer
    """

    def __init__(self, observer: Observer, date, conditions):
        self._observer = observer
        self._observation_start = date.start
        self._conditions = conditions

    def _test_planets(self):
        planets = [
            FixedTarget.from_name(p) for p in ["Jupiter", "Saturn", "Venus", "Mars"]
        ]
        rise_times = self._observer.target_rise_time(
            planets, self._observation_start, horizon=self._conditions.minimum_zenith
        )
        set_times = self._observer.target_set_time(
            planets, self._observation_start, horizon=self._conditions.minimum_zenith
        )

    @classmethod
    def from_dict(config_dict):
        raise NotImplementedError()


class Target:
    """
    A good target
    """

    def __init__(self):
        pass
