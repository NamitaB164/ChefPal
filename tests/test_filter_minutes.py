from recommendation_mcp.storage.database import (
    filter_recipes,
    get_connection,
    get_recipe,
)


def test_filter_by_minutes():
    connection = get_connection()

    recipe_ids = [63986, 66019, 216970]

    results = filter_recipes(
        connection,
        recipe_ids,
        max_minutes=30,
    )

    for recipe_id in results:
        recipe = get_recipe(connection, recipe_id)
        assert recipe["minutes"] <= 30

    connection.close()

def test_filter_by_minutes_preserves_order():
    connection = get_connection()

    recipe_ids = [216970, 63986, 66019]

    results = filter_recipes(
        connection,
        recipe_ids,
        max_minutes=30,
    )

    expected = [
        recipe_id
        for recipe_id in recipe_ids
        if get_recipe(connection, recipe_id)["minutes"] <= 30
    ]

    connection.close()

    assert results == expected