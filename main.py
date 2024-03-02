import sqlite3

from creation.database_creator import DatabaseCreator


def query_user(db: DatabaseCreator, query: bool = True) -> None:
    """Spør brukeren hvor utfylt database de ønsker. Alle svar annet enn
    1 og 2 vil gi en komplett database.

    :param DatabaseCreator db: Databasen som skal endres
    :param bool query: Om brukeren skal bli spurt, defaulter til True
    """
    print("Mulighet 1: Lag en tom database.")
    print("Mulighet 2: Lag en database med tomme tabeller.")
    print("Mulighet 3: Lag en database fylt med rader.")
    option = input("Hvilken mulighet ønsker du? [1/2/3]\n") if query else "3"

    if option == "1":
        return
    db.create_tables()
    if option == "2":
        return
    db.fill_tables()


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
