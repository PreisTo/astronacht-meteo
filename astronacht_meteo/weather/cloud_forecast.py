from astronacht_meteo.geosphere_api.arome import AROME


def get_cloud_forecast_arome(arome: AROME):
    arome.get_timeseries_data()
    pass
