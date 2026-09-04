import json
import sqlite3

from recommendation_mcp.storage.database import create_tables, insert_recipe


def test_insert_recipe():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    create_tables(connection)

    with open("data/processed/recipes.jsonl", encoding="utf-8") as file:
        recipe = json.loads(file.readline())

    insert_recipe(connection, recipe)
    connection.commit()

    result = connection.execute(
        "SELECT * FROM recipes WHERE recipe_id = ?",
        (recipe["recipe_id"],),
    ).fetchone()

    connection.close()

    assert result is not None
    assert result["recipe_id"] == recipe["recipe_id"]
    assert result["name"] == recipe["name"]
    assert result["image_path"] == recipe["image_path"]