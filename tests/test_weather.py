import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

import numpy as np

from astronacht_meteo.weather import Weather


class TestWeather(unittest.TestCase):
    def test_uses_ensemble_median_parameters_and_units(self):
        data = {
            "tcc_p50": np.array([45.0]),
            "tcc_p10": np.array([25.0]),
            "tcc_p90": np.array([65.0]),
            "msl_p50": np.array([100000.0]),
            "2t_p50": np.array([12.0]),
            "2r_p50": np.array([70.0]),
            "10u_p50": np.array([3.0]),
            "10v_p50": np.array([4.0]),
            "times": [datetime(2026, 11, 12)],
            "reference_time": datetime(2026, 11, 12),
        }
        ensemble = SimpleNamespace(get_timeseries_data=Mock(return_value=("key", data)))
        location = SimpleNamespace(lat=47.0, lon=11.0)

        with patch("astronacht_meteo.weather.Ensemble", return_value=ensemble):
            weather = Weather(location)

        ensemble.get_timeseries_data.assert_called_once_with(
            parameters=[
                "tcc_p50",
                "tcc_p10",
                "tcc_p90",
                "msl_p50",
                "2t_p50",
                "2r_p50",
                "10u_p50",
                "10v_p50",
            ],
            position="47.0,11.0",
        )
        self.assertEqual(weather.clouds.value.tolist(), [45.0])
        self.assertEqual(weather.pressure.value.tolist(), [1000.0])
        self.assertEqual(weather.temperature.value.tolist(), [12.0])
        self.assertEqual(weather.relative_humidity.value.tolist(), [70.0])
        self.assertEqual(weather.wind.value.tolist(), [5.0])
        self.assertEqual(
            weather.clouds_ensemble.value.tolist(), [[25.0], [45.0], [65.0]]
        )


if __name__ == "__main__":
    unittest.main()
