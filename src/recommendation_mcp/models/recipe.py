from pydantic import BaseModel, Field


class Nutrition(BaseModel):
    calories_kcal: float = Field(ge=0)
    total_fat_pdv: float = Field(ge=0)
    sugar_pdv: float = Field(ge=0)
    sodium_pdv: float = Field(ge=0)
    protein_pdv: float = Field(ge=0)
    saturated_fat_pdv: float = Field(ge=0)
    carbs_pdv: float = Field(ge=0)


class Recipe(BaseModel):
    recipe_id: int
    name: str
    description: str
    minutes: int = Field(ge=0)
    ingredients: list[str]
    steps: list[str]
    tags: list[str]
    nutrition: Nutrition
    rating: float = Field(ge=0)
    num_ratings: int = Field(ge=0)
    image_path: str | None = None