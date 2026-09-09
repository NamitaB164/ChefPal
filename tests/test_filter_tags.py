import json

from recommendation_mcp.storage.database import (
    filter_recipes,
    get_connection,
    get_recipe,
)


def test_filter_by_tags():
    connection = get_connection()

    recipe_ids = [66, 142, 62]

    results = filter_recipes(
        connection,
        recipe_ids,
        required_tags=["vegetarian"],
    )

    for recipe_id in results:
        recipe = get_recipe(connection, recipe_id)
        tags = {
            tag.lower()
            for tag in json.loads(recipe["tags"])
        }

        assert "vegetarian" in tags

    connection.close()
def test_filter_by_tags_preserves_order():
    connection = get_connection()

    recipe_ids = [142, 66, 62]

    results = filter_recipes(
        connection,
        recipe_ids,
        required_tags=["vegetarian"],
    )

    expected = [
        recipe_id
        for recipe_id in recipe_ids
        if "vegetarian" in {
            tag.lower()
            for tag in json.loads(
                get_recipe(connection, recipe_id)["tags"]
            )
        }
    ]

    connection.close()

    assert results == expected