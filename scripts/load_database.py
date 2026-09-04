import json

from recommendation_mcp.storage.database import (
    create_tables,
    get_connection,
    insert_recipe,
)


INPUT_FILE = "data/processed/recipes.jsonl"


def main() -> None:
    connection = get_connection()
    create_tables(connection)

    loaded = 0

    with open(INPUT_FILE, encoding="utf-8") as file:
        for line in file:
            recipe = json.loads(line)
            insert_recipe(connection, recipe)
            loaded += 1

            if loaded % 1000 == 0:
                print(f"Loaded {loaded} recipes")

    connection.commit()
    connection.close()

    print(f"Finished: {loaded} recipes")


if __name__ == "__main__":
    main()