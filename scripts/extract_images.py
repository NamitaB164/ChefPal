from pathlib import Path

from datasets import load_dataset

OUTPUT_DIR = Path("data/raw/images")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset("rahul7star/food-recipes")["train"]

    for index, row in enumerate(dataset):
        recipe_id = row["recipe_id"]
        image = row["image"]

        image_path = OUTPUT_DIR / f"{recipe_id}.jpg"

        image.thumbnail((800, 800))
        image.save(
            image_path,
            format="JPEG",
            quality=85,
            optimize=True,
        )

        if (index + 1) % 100 == 0:
            print(f"Saved {index + 1} / {len(dataset)} images")


if __name__ == "__main__":
    main()