from recommendation_mcp.storage.database import (
    filter_recipes,
    get_connection,
    get_recipe,
)


def test_filter_recipes_combined():
    connection = get_connection()

    recipe_ids = [66, 142, 62]

    results = filter_recipes(
        connection,
        recipe_ids,
        max_minutes=30,
        required_tags=["vegetarian"],
    )

    for recipe_id in results:
        recipe = get_recipe(connection, recipe_id)

        assert recipe["minutes"] <= 30
        assert "vegetarian" in recipe["tags"].lower()

    connection.close()
def test_filter_recipes_without_filters():
    connection = get_connection()

    recipe_ids = [66, 142, 62]

    results = filter_recipes(
        connection,
        recipe_ids,
    )

    connection.close()

    assert results == recipe_ids