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
def get_recipe(
    connection: sqlite3.Connection,
    recipe_id: int,
) -> sqlite3.Row | None:
    return connection.execute(
        "SELECT * FROM recipes WHERE recipe_id = ?",
        (recipe_id,),
    ).fetchone()
def _filter_by_calories(
    connection: sqlite3.Connection,
    recipe_ids: list[int],
    max_calories: float,
) -> list[int]:
    if not recipe_ids:
        return []

    placeholders = ",".join("?" for _ in recipe_ids)

    query = f"""
        SELECT recipe_id
        FROM recipes
        WHERE recipe_id IN ({placeholders})
        AND calories_kcal <= ?
    """

    parameters = [*recipe_ids, max_calories]

    rows = connection.execute(query, parameters).fetchall()

    valid_ids = {row["recipe_id"] for row in rows}

    # Preserve the original hybrid/RRF ranking order.
    return [
        recipe_id
        for recipe_id in recipe_ids
        if recipe_id in valid_ids
    ]

def _filter_by_minutes(
    connection: sqlite3.Connection,
    recipe_ids: list[int],
    max_minutes: int,
) -> list[int]:
    if not recipe_ids:
        return []

    placeholders = ",".join("?" for _ in recipe_ids)

    query = f"""
        SELECT recipe_id
        FROM recipes
        WHERE recipe_id IN ({placeholders})
        AND minutes <= ?
    """

    parameters = [*recipe_ids, max_minutes]

    rows = connection.execute(query, parameters).fetchall()

    valid_ids = {row["recipe_id"] for row in rows}

    # Preserve the original hybrid/RRF ranking order.
    return [
        recipe_id
        for recipe_id in recipe_ids
        if recipe_id in valid_ids
    ]

def _filter_by_tags(
    connection: sqlite3.Connection,
    recipe_ids: list[int],
    required_tags: list[str],
) -> list[int]:
    if not recipe_ids:
        return []

    if not required_tags:
        return recipe_ids

    placeholders = ",".join("?" for _ in recipe_ids)

    query = f"""
        SELECT recipe_id, tags
        FROM recipes
        WHERE recipe_id IN ({placeholders})
    """

    rows = connection.execute(
        query,
        recipe_ids,
    ).fetchall()

    valid_ids = set()

    required = {
        tag.lower()
        for tag in required_tags
    }

    for row in rows:
        tags = {
            tag.lower()
            for tag in json.loads(row["tags"])
        }

        if required.issubset(tags):
            valid_ids.add(row["recipe_id"])

    return [
        recipe_id
        for recipe_id in recipe_ids
        if recipe_id in valid_ids
    ]
def _filter_by_rating(
    connection: sqlite3.Connection,
    recipe_ids: list[int],
    min_rating: float,
) -> list[int]:
    if not recipe_ids:
        return []

    placeholders = ",".join("?" for _ in recipe_ids)

    query = f"""
        SELECT recipe_id
        FROM recipes
        WHERE recipe_id IN ({placeholders})
        AND rating >= ?
    """

    parameters = [*recipe_ids, min_rating]

    rows = connection.execute(query, parameters).fetchall()

    valid_ids = {row["recipe_id"] for row in rows}

    return [recipe_id for recipe_id in recipe_ids if recipe_id in valid_ids]
def filter_recipes(
    connection: sqlite3.Connection,
    recipe_ids: list[int],
    max_calories: float | None = None,
    max_minutes: int | None = None,
    required_tags: list[str] | None = None,
    min_rating: float | None = None,
) -> list[int]:
    if not recipe_ids:
        return []

    results = recipe_ids

    if max_calories is not None:
        results = _filter_by_calories(
            connection,
            results,
            max_calories,
        )

    if max_minutes is not None:
        results = _filter_by_minutes(
            connection,
            results,
            max_minutes,
        )
    if min_rating is not None:
        results = _filter_by_rating(connection, results, min_rating)
    if required_tags is not None:
        results = _filter_by_tags(
            connection,
            results,
            required_tags,
        )

    return results