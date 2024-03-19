from creation.db_creator import DBCreator
from creation.db_queryer import DBQueryer
from creation.db_ticket_orderer import DBTicketOrderer
from creation.helpers import clear_terminal, print_header, validate_input


def main() -> None:
    while True:
        clear_terminal()
        print_header("Velkommen til Trøndelag Teater")

        print("1: Endre database.")
        print("2: Bestill billetter.")
        print("3: SQL-spørringer.")
        print("4: Avslutt.")
        print("Hva vil du gjøre?")

        match validate_input([str(i) for i in range(1, 5)]):
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

        print("Takk for besøket!")


if __name__ == "__main__":
    main()
