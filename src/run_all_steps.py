import subprocess
import sys

steps = [
    "01_parse_listings_data.py",
    "02_add_listings_features.py",
    "03_get_market_performance_from_bybit.py",
    "04_get_prelisting_data_from_coingecko.py"
]

for step in steps:
    print(f"running {step}")
    result = subprocess.run([sys.executable, step], check=True)
    if result.returncode != 0:
        print(f"failed at {step}")
        sys.exit(1)
    print(f"{step} is done")
