from app.ai.excel_loader import load_ingredient_ratios

INGREDIENT_RATIOS = load_ingredient_ratios()

EVENT_TYPE_MULTIPLIERS = {
    "birthday": 1.05,
    "party": 1.10,
    "wedding": 1.00,
    "corporate": 1.05,
    "kids_party": 1.15
}

EVENT_RISK_SCORE = {
    "wedding": 5,
    "birthday": 10,
    "corporate": 10,
    "party": 20,
    "kids_party": 25
}


def calculate_confidence(event_type, kids_ratio, buffer_percent):
    base = 100
    base -= EVENT_RISK_SCORE.get(event_type, 15)
    base -= int(kids_ratio * 20)
    base += int(buffer_percent * 100)
    return max(60, min(base, 95))


def calculate_ingredients(
    package: str,
    adults: int,
    kids: int,
    event_type: str = "birthday",
    buffer_percent: float = 0.05
):
    if package not in INGREDIENT_RATIOS:
        raise ValueError("Invalid catering package")

    multiplier = EVENT_TYPE_MULTIPLIERS.get(event_type, 1.0)
    total_people = adults + kids
    kids_ratio = kids / total_people if total_people else 0

    dishes_output = []

    for dish, ingredients in INGREDIENT_RATIOS[package].items():
        dish_ingredients = []

        for ing in ingredients:
            base_qty_g = (adults * ing["adult"]) + (kids * ing["kid"])
            adjusted_qty_g = base_qty_g * multiplier * (1 + buffer_percent)

            dish_ingredients.append({
                "name": ing["name"],
                "quantity": round(adjusted_qty_g / 1000, 2),
                "unit": "kg"
            })

        confidence = calculate_confidence(
            event_type=event_type,
            kids_ratio=kids_ratio,
            buffer_percent=buffer_percent
        )

        dishes_output.append({
            "dish": dish,
            "ingredients": dish_ingredients,
            "confidence_score": confidence
        })

    reasoning = {
        "event_type": event_type,
        "event_multiplier": multiplier,
        "buffer_percent": buffer_percent,
        "explanation": (
            f"For a {event_type.replace('_', ' ')} event, "
            f"a {int((multiplier - 1) * 100)}% adjustment was applied. "
            f"A {int(buffer_percent * 100)}% chef buffer was added "
            f"to ensure sufficient food."
        )
    }

    return dishes_output, reasoning
