from .arome import AROME


class NWPV2(AROME):
    resource_id = "nwp-v2-1h-1km"
    mode = "forecast"
