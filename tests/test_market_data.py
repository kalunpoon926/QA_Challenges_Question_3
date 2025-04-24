import sys
import os

# Add the parent directory to sys.path so that custom modules like 'core.logger_config' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import pytest
from core.logger_config import setup_logger

# Initialize a logger instance for logging test steps and responses
logger = setup_logger(__name__)

'''
    Parameterize the test to allow for multiple stock codes if needed
    To test multiple stock codes, modify the @pytest.mark.parametrize section in test_market_data.py.
    @pytest.mark.parametrize("stock_code", ["000001", "000002", "000004"])
'''
@pytest.mark.parametrize("stock_code", ["000001","000002","000004"])
def test_szse_market_data(stock_code):

    """
    This test verifies that the market data for a given stock code from SZSE API:
    - Returns a successful HTTP status
    - Contains valid 'high' and 'low' values
    - Ensures 'high' is greater than 'low'
    """

    # API endpoint for Shenzhen Stock Exchange market data with specific stock code
    url = f"https://www.szse.cn/api/market/ssjjhq/getTimeData?random=0.367046636775733&marketId=1&code={stock_code}"

    try:
        # Send a GET request to the SZSE API
        response = requests.get(url, timeout=10)

        # Assert that the response is successful (HTTP 200)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Parse the JSON response
        data = response.json()
        # Log the full response for debugging
        logger.info(data)

        # Extract and convert the 'high' and 'low' prices
        high = float(data["data"]["high"])
        low = float(data["data"]["low"])

        # Log the high and low values
        logger.info(f"High: {high}, Low: {low}")

        # Validate that high is greater than low
        assert high > low, "High value is not greater than Low value"
        logger.info("High value is greater than Low value")

    # Catch and log HTTP or connection errors
    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")

    # Catch and log cases where expected keys are missing from the response
    except KeyError as e:
        logger.info(f"Missing expected key in response: {e}")