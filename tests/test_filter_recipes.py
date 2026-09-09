from recommendation_mcp.storage.database import (
    filter_by_calories,
    get_connection,
    get_recipe,
)


def test_filter_by_calories():
    connection = get_connection()

    recipe_ids = [63986, 66019, 216970]

    results = filter_by_calories(
        connection,
        recipe_ids,
        max_calories=500,
    )

    for recipe_id in results:
        recipe = get_recipe(connection, recipe_id)
        assert recipe["calories_kcal"] <= 500

    connection.close()
def test_filter_by_calories_preserves_order():
    connection = get_connection()

    recipe_ids = [216970, 63986, 66019]

    results = filter_by_calories(
        connection,
        recipe_ids,
        max_calories=500,
    )

    expected = [
        recipe_id
        for recipe_id in recipe_ids
        if get_recipe(connection, recipe_id)["calories_kcal"] <= 500
    ]

    connection.close()

    assert results == expected