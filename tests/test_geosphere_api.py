import unittest
from unittest.mock import patch

from astronacht_meteo.geosphere_api.ensemble import Ensemble
from astronacht_meteo.geosphere_api.nwpv2 import NWPV2


class TestEnsemble(unittest.TestCase):
    def test_timeseries_uses_ensemble_v2_dataset(self):
        api = Ensemble()
        response = {
            "features": [
                {
                    "properties": {
                        "parameters": {
                            "tcc_p50": {"data": [25.0, 50.0]},
                        }
                    }
                }
            ],
            "timestamps": [
                "2024-01-01T00:00:00+00:00",
                "2024-01-01T01:00:00+00:00",
            ],
            "reference_time": "2024-01-01T00:00:00+00:00",
        }

        with patch.object(api, "_query_dict", return_value=response) as query:
            query_key, data = api.get_timeseries_data(
                parameters=["tcc_p50"], position="47.0,11.0"
            )

        self.assertEqual(
            api._url,
            "https://dataset.api.hub.geosphere.at/v1/timeseries/forecast/"
            "ensemble-v2-1h-1km",
        )
        query.assert_called_once_with(
            {
                "parameters": ["tcc_p50"],
                "lat_lon": "47.0,11.0",
                "forecast_offset": 0,
            }
        )
        self.assertEqual(data["tcc_p50"].tolist(), [25.0, 50.0])
        self.assertEqual(len(data["times"]), 2)
        self.assertIn("parameters", query_key)


class TestNWPV2(unittest.TestCase):
    def test_timeseries_uses_nwp_v2_dataset_and_default_parameter(self):
        api = NWPV2()
        response = {
            "features": [
                {
                    "properties": {
                        "parameters": {
                            "tcc": {"data": [25.0, 50.0]},
                        }
                    }
                }
            ],
            "timestamps": [
                "2024-01-01T00:00:00+00:00",
                "2024-01-01T01:00:00+00:00",
            ],
            "reference_time": "2024-01-01T00:00:00+00:00",
        }

        with patch.object(api, "_query_dict", return_value=response) as query:
            _, data = api.get_timeseries_data(position="47.0,11.0")

        self.assertEqual(
            api._url,
            "https://dataset.api.hub.geosphere.at/v1/timeseries/forecast/"
            "nwp-v2-1h-1km",
        )
        query.assert_called_once_with(
            {
                "parameters": ["tcc"],
                "lat_lon": "47.0,11.0",
                "forecast_offset": 0,
            }
        )
        self.assertEqual(data["tcc"].tolist(), [25.0, 50.0])


if __name__ == "__main__":
    unittest.main()
