import json
from pathlib import Path

from recommendation_mcp.models.recipe import Recipe

INPUT_FILE = Path("data/raw/recipes.jsonl")
OUTPUT_FILE = Path("data/processed/recipes.jsonl")
IMAGE_DIR = Path("data/raw/images")

def extract_ingredients(markdown: str) -> list[str]:
    section = markdown.split("## Ingredients", 1)[1]
    section = section.split("## Instructions", 1)[0]

    ingredients_text = section.strip()

    return [
        ingredient.strip()
        for ingredient in ingredients_text.split(",")
        if ingredient.strip()
    ]


def process_recipe(row: dict) -> Recipe:
    recipe = Recipe(
        recipe_id=int(row["recipe_id"]),
        name=row["name"],
        description=row["description"],
        minutes=int(row["minutes"]),
        ingredients=extract_ingredients(row["markdown"]),
        steps=row["steps"],
        tags=row["tags"],
        nutrition={
            "calories_kcal": float(row["nutrition"]["calories"]),
            "total_fat_pdv": float(row["nutrition"]["total_fat_pdv"]),
            "sugar_pdv": float(row["nutrition"]["sugar_pdv"]),
            "sodium_pdv": float(row["nutrition"]["sodium_pdv"]),
            "protein_pdv": float(row["nutrition"]["protein_pdv"]),
            "saturated_fat_pdv": float(row["nutrition"]["saturated_fat_pdv"]),
            "carbs_pdv": float(row["nutrition"]["carbs_pdv"]),
        },
        rating=float(row["rating"]),
        num_ratings=int(row["num_ratings"]),
        image_path=(IMAGE_DIR / f"{row['recipe_id']}.jpg").as_posix(),
    )

    return recipe
def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    processed = 0

    with (
        INPUT_FILE.open("r", encoding="utf-8") as input_file,
        OUTPUT_FILE.open("w", encoding="utf-8") as output_file,
    ):
        for line in input_file:
            row = json.loads(line)
            recipe = process_recipe(row)

            output_file.write(
                json.dumps(recipe.model_dump(), ensure_ascii=False) + "\n"
            )

            processed += 1

            if processed % 1000 == 0:
                print(f"Processed {processed} recipes")

    print(f"Finished: {processed} recipes")


if __name__ == "__main__":
    main()