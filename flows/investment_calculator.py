from typing import List

from prefect import flow

from library.models import Portfolio, Asset, Stock, Crypto


def asset_factory(asset_name: str, asset_quantity: float, asset_type: str) -> Asset:
    if asset_type == "Stock":
        return Stock(asset_name, asset_quantity)
    elif asset_type == "Crypto":
        return Crypto(asset_name, asset_quantity)
    else:
        raise ValueError(f"Unknown asset type: {asset_type}")


@flow
def investment_calculator(portfolio_name: str, portfolio_assets: List[dict]) -> None:
    api_key = "my_api_key"

    # Step 1: Create a Portfolio object
    portfolio = Portfolio(portfolio_name)

    # Step 2: Add assets to the Portfolio object
    for asset_dict in portfolio_assets:
        new_asset = asset_factory(asset_dict["name"], asset_dict["quantity"], asset_dict["type"])
        portfolio.add_asset(new_asset)

    # Step 3: Calculate the total value of the Portfolio
    total_value = portfolio.calculate_total_value("https://api.example.com", api_key)

    print(f"Total value of the portfolio '{portfolio_name}': ${total_value}")