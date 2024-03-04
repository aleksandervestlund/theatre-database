from __future__ import annotations

import os

from creation.database_connection import DatabaseConnection
from creation.rows import (
    AKTER,
    ANSATTE,
    DATOER,
    DB_FILE,
    DELTAR_I,
    FORESTILLINGER,
    GAMLE_SCENE_STOLER,
    GRUPPER,
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


class DatabaseCreator(DatabaseConnection):
    def __init__(self) -> None:
        """Lager en tilkobling til en tom database."""
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        super().__init__()

    def create_tables(self) -> None:
        """Kjører `SQL_FILE`."""
        with open(SQL_FILE, encoding="utf-8") as file:
            self.con.executescript(file.read())

    def book_reserved_seats(self) -> None:
        """Leser filene i `reservations`. Lager et billettkjøp og
        knytter alle reserverte seter i den respektive filen til dette.
        """
        # fmt: off
        info_list = [
            ("Kongsemnene", "hovedscenen", HOVEDSCENE_STOLER),
            ("Størst av alt er kjærligheten", "gamle-scene", GAMLE_SCENE_STOLER),
        ]
        # fmt: on
        for i, info in enumerate(info_list, 1):
            play, filename, chairs = info
            scene = " ".join(filename.split("-")).title()
            with open(
                f"reservations/{filename}.txt", encoding="utf-8"
            ) as file:
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
                [(i, 1, 1, KUNDEPROFILER[0][0], play, scene, month, day)],
            )
            for j, seat in enumerate(seats_string):
                if seat != "1":
                    continue
                self.insert_rows("Billett", [(i, *chairs[j], play, "Ordinær")])

    def fill_tables(self) -> None:
        """Fyller tabellene med data fra `rows.py`. Avhengig av at
        `create_tables` har blitt kjørt først.
        """
        self.insert_rows("Teaterstykke", TEATERSTYKKER)
        self.insert_rows("Oppgave", OPPGAVER)
        self.insert_rows(
            "Ansatt",
            ANSATTE,
            ["Ansattstatus", "Navn", "TeaterstykkeNavn", "OppgaveNavn"],
        )
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

    def creation_query(self, query: bool = True) -> None:
        """Spør brukeren hvor utfylt database de ønsker.

        :param bool query: Om brukeren skal bli spurt, defaulter til True
        """
        if query:
            print("1: Lag en database med tomme tabeller.")
            print("2: Lag en database fylt med rader (u/reserverte seter).")
            print("3: Lag en database fylt med rader (m/reserverte seter).")
            print("Hvilken mulighet ønsker du? [1/2/3]")

            while (option := input("")) not in {"1", "2", "3"}:
                print("Ugyldig input. Prøv igjen.")
        else:
            option = "3"

        self.create_tables()
        if option == "1":
            return
        self.fill_tables()
        if option == "2":
            return
        self.book_reserved_seats()
