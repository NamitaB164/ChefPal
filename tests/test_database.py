from recommendation_mcp.storage.database import create_tables, get_connection


def test_create_recipes_table():
    connection = get_connection()
    create_tables(connection)

    table = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'recipes'
        """
    ).fetchone()

    connection.close()

    assert table is not None
    assert table["name"] == "recipes"