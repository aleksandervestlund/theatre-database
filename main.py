import sqlite3

from creation.fill_database import DatabaseCreator, query_user


def main() -> None:
    db = DatabaseCreator()
    query_user(db, False)
    try:
        db.print_all_tables(["Dato", "Stol", "Billett"])
    except sqlite3.OperationalError:
        print("Ingen tabeller.")
    db.close()


if __name__ == "__main__":
    main()
