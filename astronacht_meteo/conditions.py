class Condition:
    def _clouds(self):
        pass

    def _percipitation(self):
        pass

    def _rel_humidity(self):
        pass

    def _sun(self):
        pass

    def _thunderstorm_risk(self):
        pass

    def _risk(self):
        pass

    def _zenith(self):
        pass


class MinimalCondition(Condition):
    pass


class Conditions:
    def __init__(self, minimal: MinimalCondition, current: Condition = None):
        pass
