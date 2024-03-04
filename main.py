from sqlite3 import OperationalError

from creation.database_creator import DatabaseCreator


def query_user(db: DatabaseCreator, query: bool = True) -> None:
    """Spør brukeren hvor utfylt database de ønsker.

    :param DatabaseCreator db: Databasen som skal endres
    :param bool query: Om brukeren skal bli spurt, defaulter til True
    """
    if query:
        print("Mulighet 1: Lag en tom database.")
        print("Mulighet 2: Lag en database med tomme tabeller.")
        print("Mulighet 3: Lag en database fylt med rader.")
        print("Hvilken mulighet ønsker du? [1/2/3]")

        while (option := input("")) not in {"1", "2", "3"}:
            print("Ugyldig input. Prøv igjen.")
    else:
        option = "3"

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
        db.print_all_tables(["Dato", "Billett"])
    except OperationalError:
        print("Ingen tabeller.")
    db.close(False)  # Lagrer ikke rader til db1


if __name__ == "__main__":
    main()
