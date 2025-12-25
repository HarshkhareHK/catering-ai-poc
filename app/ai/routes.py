from fastapi import APIRouter, HTTPException
from app.ai.schemas import (
    IngredientCalculationInput,
    IngredientCalculationResponse
)
from app.ai.calculator import calculate_ingredients

router = APIRouter()


@router.post(
    "/calculate-ingredients",
    response_model=IngredientCalculationResponse
)
def calculate_ingredients_api(payload: IngredientCalculationInput):

    try:
        dishes, reasoning = calculate_ingredients(
            package=payload.package,
            adults=payload.adults,
            kids=payload.kids,
            event_type=payload.event_type,
            buffer_percent=payload.buffer_percent
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "package": payload.package,
        "total_people": payload.adults + payload.kids,
        "dishes": dishes,
        "reasoning": reasoning
    }
