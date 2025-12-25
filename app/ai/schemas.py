from pydantic import BaseModel
from typing import List, Optional
from datetime import time

# =========================
# INPUT SCHEMA
# =========================

class IngredientCalculationInput(BaseModel):
    # Customer / Event Details
    name: str
    phone_number: str
    event_location: str

    # Event Info
    event_name: str
    serving_start_time: time

    # People Count
    adults: int
    kids: int

    # Food Selection
    food_choices: List[str]
    food_allergies: Optional[str] = None

    # AI Parameters
    package: str
    event_type: Optional[str] = "birthday"
    buffer_percent: Optional[float] = 0.05


# =========================
# OUTPUT SCHEMAS
# =========================

class IngredientOutput(BaseModel):
    name: str
    quantity: float
    unit: str


class DishOutput(BaseModel):
    dish: str
    ingredients: List[IngredientOutput]
    confidence_score: int


class ReasoningOutput(BaseModel):
    event_type: str
    event_multiplier: float
    buffer_percent: float
    explanation: str


class IngredientCalculationResponse(BaseModel):
    package: str
    total_people: int
    dishes: List[DishOutput]
    reasoning: Optional[ReasoningOutput] = None
