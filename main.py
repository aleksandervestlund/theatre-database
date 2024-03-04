from creation.database_creator import DatabaseCreator
from creation.database_queryer import DatabaseQueryer


def main() -> None:
    dbc = DatabaseCreator()
    dbc.creation_query(False)
    dbc.print_all_tables({"Dato", "Billett", "Stol"})
    dbc.close(True)  # Lagrer ikke rader

    dbq = DatabaseQueryer()
    dbq.order_tickets()
    dbq.close(False)


if __name__ == "__main__":
    main()
