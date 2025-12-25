import pandas as pd
from pathlib import Path

EXCEL_PATH = Path("data/ingredient_ratios.xlsx")


def load_ingredient_ratios():
    """
    Loads ingredient ratios from Excel
    Returns structured dict usable by AI calculator
    """

    df = pd.read_excel(EXCEL_PATH)

    ratios = {}

    for _, row in df.iterrows():
        package = row["package"]
        dish = row["dish"]

        ratios.setdefault(package, {})
        ratios[package].setdefault(dish, [])

        ratios[package][dish].append({
            "name": row["ingredient"],
            "adult": row["adult_qty_g"],
            "kid": row["kid_qty_g"],
            "unit": "g"
        })

    return ratios
