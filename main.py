from creation.database_creator import DatabaseCreator
from creation.database_queryer import DatabaseQueryer
from creation.validators import validate_input


def main() -> None:
    dbc = DatabaseCreator()
    dbq = DatabaseQueryer()

    print("Hei! Velkommen til teateret.")
    while True:
        print("1: Opprett database.")
        print("2: SQL-spørringer.")
        print("3: Avslutt.")
        print("Hva vil du gjøre?")

        match validate_input(["1", "2", "3"]):
            case "1":
                dbc.ask_user()
            case "2":
                dbq.ask_user()
            case "3":
                break

    dbc.close(True)
    dbq.close(True)


if __name__ == "__main__":
    main()
