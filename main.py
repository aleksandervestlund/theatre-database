from sqlite3 import IntegrityError

from creation.db_creator import DBCreator
from creation.db_queryer import DBQueryer
from creation.db_ticket_orderer import DBTicketOrderer
from creation.helpers import clear_terminal, validate_input


def test_db_creator() -> None:
    dbc = DBCreator()
    dbc.clear_database()
    dbc.create_tables()
    dbc.fill_tables()
    try:
        dbc.fill_tables()
    except IntegrityError:
        print("Hola")
    dbc.clear_database()
    dbc.close()


def main() -> None:
    test_db_creator()

    while True:
        clear_terminal()
        print("+--------------------------------------------------------+")
        print("|             Velkommen til Trøndelag Teater             |")
        print("+--------------------------------------------------------+")

        print("1: Endre database.")
        print("2: Bestill billetter.")
        print("3: SQL-spørringer.")
        print("4: Avslutt.")
        print("Hva vil du gjøre?")

        match validate_input(["1", "2", "3", "4"]):
            case "1":
                dbc = DBCreator()
                dbc.ask_user()
                dbc.close()
            case "2":
                dbtc = DBTicketOrderer()
                dbtc.ask_user()
                dbtc.close()
            case "3":
                dbq = DBQueryer()
                dbq.ask_user()
                dbq.close()
            case "4":
                break


if __name__ == "__main__":
    main()
