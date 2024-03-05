from creation.database_creator import DatabaseCreator
from creation.database_queryer import DatabaseQueryer
from creation.validators import validate_input


def main() -> None:
    print("Hei! Velkommen til teateret.")
    while True:
        
        print("1: Endre database.")
        print("2: SQL-spørringer.")
        print("3: Avslutt.")
        print("Hva vil du gjøre?")

        match validate_input(["1", "2", "3"]):
            case "1":
                dbc = DatabaseCreator()
                dbc.ask_user()
                dbc.close(True)
            case "2":
                dbq = DatabaseQueryer()
                dbq.ask_user()
                dbq.close(True)
            case "3":
                return


if __name__ == "__main__":
    main()
