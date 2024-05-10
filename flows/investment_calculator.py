import asyncio
import datetime
from typing import List

from prefect import flow
from prefect.blocks.system import JSON

from library.models import Portfolio, Asset, Stock, Crypto


def asset_factory(asset_name: str, asset_quantity: float, asset_type: str) -> Asset:
    if asset_type == "Stock":
        return Stock(asset_name, asset_quantity)
    elif asset_type == "Crypto":
        return Crypto(asset_name, asset_quantity)
    else:
        raise ValueError(f"Unknown asset type: {asset_type}")


@flow
async def investment_calculator(portfolio_names: List[str]) -> None:
    api_block = await JSON.load("polygon-api-key")
    url = api_block.value["url"]
    api_key = api_block.value["api_key"]

    # Step 1: Create a Portfolio object
    for portfolio_name in portfolio_names:
        portfolio = Portfolio(portfolio_name)

        portfolio_block = await JSON.load(portfolio_name)
        portfolio_assets: List[dict] = portfolio_block.value

        # Step 2: Add assets to the Portfolio object
        for asset_dict in portfolio_assets:
            new_asset = asset_factory(asset_dict["name"], asset_dict["quantity"], asset_dict["type"])
            portfolio.add_asset(new_asset)

        # Step 3: Calculate the total value of the Portfolio
        total_value = portfolio.calculate_total_value(url, api_key)

        current_time = datetime.date.today()

        print(f"Total value of the portfolio '{portfolio_name}' for date {current_time}: ${total_value}")


if __name__ == "__main__":
    asyncio.run(investment_calculator(['alex-roth-ira', 'crypto-portfolio']))
