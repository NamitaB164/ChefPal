import json
import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/processed/recipes.db")


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def insert_recipe(
    connection: sqlite3.Connection,
    recipe: dict,
) -> None:
    nutrition = recipe["nutrition"]

    connection.execute(
        """
        INSERT INTO recipes (
            recipe_id,
            name,
            description,
            minutes,
            ingredients,
            steps,
            tags,
            calories_kcal,
            total_fat_pdv,
            sugar_pdv,
            sodium_pdv,
            protein_pdv,
            saturated_fat_pdv,
            carbs_pdv,
            rating,
            num_ratings,
            image_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            recipe["recipe_id"],
            recipe["name"],
            recipe["description"],
            recipe["minutes"],
            json.dumps(recipe["ingredients"], ensure_ascii=False),
            json.dumps(recipe["steps"], ensure_ascii=False),
            json.dumps(recipe["tags"], ensure_ascii=False),
            nutrition["calories_kcal"],
            nutrition["total_fat_pdv"],
            nutrition["sugar_pdv"],
            nutrition["sodium_pdv"],
            nutrition["protein_pdv"],
            nutrition["saturated_fat_pdv"],
            nutrition["carbs_pdv"],
            recipe["rating"],
            recipe["num_ratings"],
            recipe["image_path"],
        ),
    )


def create_tables(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            recipe_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            minutes INTEGER NOT NULL,
            ingredients TEXT NOT NULL,
            steps TEXT NOT NULL,
            tags TEXT NOT NULL,
            calories_kcal REAL NOT NULL,
            total_fat_pdv REAL NOT NULL,
            sugar_pdv REAL NOT NULL,
            sodium_pdv REAL NOT NULL,
            protein_pdv REAL NOT NULL,
            saturated_fat_pdv REAL NOT NULL,
            carbs_pdv REAL NOT NULL,
            rating REAL NOT NULL,
            num_ratings INTEGER NOT NULL,
            image_path TEXT
        )
        """
    )

    connection.commit()