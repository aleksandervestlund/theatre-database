import os
from sqlite3 import IntegrityError

from creation.config import (
    AKTER,
    ANSATTE,
    DATOER,
    DB_FILE,
    DELTAR_I,
    FORESTILLINGER,
    GAMLE_SCENE_FILE,
    GAMLE_SCENE_STOLER,
    GRUPPER,
    HOVEDSCENE_FILE,
    HOVEDSCENE_STOLER,
    KUNDEPROFILER,
    OPPGAVER,
    ROLLER,
    SALER,
    SKUESPILLERE,
    SPILLER_ROLLER,
    SQL_FILE,
    STOLER,
    TEATERSTYKKER,
)
from creation.db_connector import DBConnector
from creation.helpers import clear_terminal, print_header, validate_input


class DBCreator(DBConnector):
    def ask_user(self) -> None:
        while True:
            clear_terminal()
            print_header("Endre databasen")

            print("1: Tøm databasen.")
            print("2: Fyll databasen med tabeller.")
            print("3: Fyll databasen med forhåndsbestemte rader.")
            print("4: Reserver forhåndsbestilte seter.")
            print("5: Gå tilbake.")
            print("Hvilken mulighet ønsker du?")

            match validate_input([str(i) for i in range(1, 6)]):
                case "1":
                    self.clear_database()
                case "2":
                    self.create_tables()
                case "3":
                    if not self.validate_tables():
                        continue

                    try:
                        self.fill_tables()
                    except IntegrityError:
                        print("Tabellene er allerede fylt.")
                        self.reconnect()
                        input("Trykk enter for å fortsette.")
                        continue
                case "4":
                    if not self.validate_tables():
                        continue
                    if not self.validate_rows():
                        continue

                    try:
                        self.book_reserved_seats()
                    except IntegrityError:
                        print("Setene er allerede reservert.")
                        self.reconnect()
                        input("Trykk enter for å fortsette.")
                        continue
                case "5":
                    return

            self.con.commit()
            print("Suksess!")
            input("Trykk enter for å fortsette.")

    def create_tables(self) -> None:
        """Kjører `SQL_FILE`."""
        with open(SQL_FILE, encoding="utf-8") as file:
            self.cur.executescript(file.read())

    def fill_tables(self) -> None:
        """Fyller tabellene med data fra `config.py`. Avhengig av at
        `create_tables` har blitt kjørt først.
        """
        self.insert_rows("Teaterstykke", TEATERSTYKKER)
        self.insert_rows("Oppgave", OPPGAVER)
        # fmt: off
        self.insert_rows(
            "Ansatt",
            ANSATTE,
            ["Ansattstatus", "EPostadresse", "Navn", "TeaterstykkeNavn", "OppgaveNavn"],
        )
        # fmt: on
        self.insert_rows("Akt", AKTER, ["TeaterstykkeNavn", "Nummer"])
        self.insert_rows("Rolle", ROLLER)
        self.insert_rows("DeltarI", DELTAR_I)
        self.insert_rows("Skuespiller", SKUESPILLERE, ["Navn"])
        self.insert_rows("SpillerRolle", SPILLER_ROLLER)
        self.insert_rows("Dato", DATOER)
        self.insert_rows("Sal", SALER)
        self.insert_rows("Stol", STOLER)
        self.insert_rows("Forestilling", FORESTILLINGER)
        self.insert_rows("Kundeprofil", KUNDEPROFILER)
        self.insert_rows("Gruppe", GRUPPER)

    def read_from_file(
        self, idx: int, info: tuple[str, str, list[tuple[str, int, int, str]]]
    ) -> None:
        play, filename, chairs = info
        scene = " ".join(filename.split(os.sep)[-1].split("-")).title()

        with open(f"{filename}.txt", encoding="utf-8") as file:
            month, day = [
                int(number) for number in file.readline().split("-")[1:]
            ]
            seats_string = "".join(
                line.strip()
                for line in reversed(file.readlines())
                if line[0] in {"0", "1", "x"}
            )

        self.insert_rows(
            "Billettkjøp",
            [(idx, 1, 1, KUNDEPROFILER[0][0], play, scene, month, day)],
        )
        for j, seat in enumerate(seats_string):
            if seat != "1":
                continue
            self.insert_rows("Billett", [(idx, *chairs[j], play, "Ordinær")])

    def book_reserved_seats(self) -> None:
        """Leser filene i `reservations`. Lager et billettkjøp og
        knytter alle reserverte seter i den respektive filen til dette.
        """
        # fmt: off
        info_list = [
            ("Kongsemnene", HOVEDSCENE_FILE, HOVEDSCENE_STOLER),
            ("Størst av alt er kjærligheten", GAMLE_SCENE_FILE, GAMLE_SCENE_STOLER),
        ]
        # fmt: on
        for i, info in enumerate(info_list, 1):
            self.read_from_file(i, info)

    def clear_database(self) -> None:
        """Sletter databasen og kobler til på nytt."""
        self.con.close()
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        self.connect()
