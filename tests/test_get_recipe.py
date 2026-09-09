from recommendation_mcp.storage.database import get_connection, get_recipe


def test_get_recipe():
    connection = get_connection()

    recipe = get_recipe(connection, 63986)

    connection.close()

    assert recipe is not None
    assert recipe["recipe_id"] == 63986
    assert recipe["name"] == "chicken lickin  good  pork chops"
    assert recipe["image_path"] == "data/raw/images/63986.jpg"