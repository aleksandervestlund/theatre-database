from creation.db_connector import DBConnector
from creation.db_creator import DBCreator
from creation.db_queryer import DBQueryer
from creation.db_ticket_orderer import DBTicketOrderer
from creation.validators import validate_input


def main() -> None:
    print("Hei! Velkommen til teateret.")
    while True:
        print("---------------------")
        print("1: Endre database.")
        print("2: Bestill billetter.")
        print("3: SQL-spørringer.")
        print("4: Avslutt.")
        print("Hva vil du gjøre?")

        match validate_input(["1", "2", "3", "4"]):
            case "1":
                dbc = DBCreator()
                dbc.ask_user()
                dbc.close(True)
            case "2":
                dbq = DBTicketOrderer()
                dbq.ask_user()
                dbq.close(True)
            case "3":
                dbq = DBQueryer()
                dbq.ask_user()
                dbq.close(True)
            case "4":
                break

    DBConnector().print_all_tables()


if __name__ == "__main__":
    main()
