import requests
import json

def test_predict():
    url = "http://localhost:8000/predict"

    payload = {
        "data": [
            ["HOBBIES_1_001", "2016-05-22", "d_1960", 5, 10.5, 7, 1, 0, 5.0, 4.8, 4.6, 4.7, 4.9, 5.1, 0.02],
            ["HOBBIES_1_002", "2016-05-23", "d_1961", 5, 12.0, 1, 0, 0, 6.0, 5.8, 5.6, 5.7, 5.9, 6.1, 0.03]
        ],
        "columns": [
            "item_id", "date", "d", "month", "sell_price", "day_of_week", "is_weekend", "is_holiday",
            "lag_7", "lag_14", "lag_28", "rolling_mean_7", "rolling_mean_14", "rolling_mean_28", "price_change"
        ]
    }

    response = requests.post(url, json=payload)
    print(json.dumps(response.json(), indent=4))
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


if __name__ == "__main__":
    test_predict()