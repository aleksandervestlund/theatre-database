from __future__ import annotations

import os
import sqlite3
from typing import Any

from creation.rows import (
    AKTER,
    ANSATTE,
    DATOER,
    DELTAR_I,
    FORESTILLINGER,
    GAMLE_SCENE_STOLER,
    GRUPPER,
    HOVEDSCENE_STOLER,
    KUNDEPROFILER,
    OPPGAVER,
    ROLLER,
    SALER,
    STOLER,
    SKUESPILLERE,
    SPILLER_ROLLER,
    TABLES,
    TEATERSTYKKER,
)
from creation.validators import validate_attribute_names, validate_table_name


class DatabaseCreator:
    DB_FILE = "teater.db"
    SQL_FILE = "creation/create.sql"

    def __init__(self) -> None:
        """Lager en tilkobling til en tom database."""
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)
        self.con = sqlite3.connect(self.DB_FILE)
        self.con.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.con.cursor()

    def print_table(self, table: str) -> None:
        validate_table_name(table)
        dashes = "-" * (46 - len(table) // 2)
        print(f"{dashes}{table}{dashes}")
        for row in self.cursor.execute(f"SELECT * FROM {table}"):
            print(row)

    def print_all_tables(self, mute_tables: list[str] | None = None) -> None:
        """Printer alle tabellene i databasen.

        :param list[str] mute_tables: Tabeller som ikke skal printes
        """
        if mute_tables is None:
            for table in TABLES:
                self.print_table(table)
            return
        for table in TABLES:
            if table not in mute_tables:
                self.print_table(table)

    def create_tables(self) -> None:
        """Kjører `SQL_FILE`."""
        with open(self.SQL_FILE, encoding="utf-8") as file:
            self.con.executescript(file.read())

    def insert_rows(
        self,
        table: str,
        rows: list[tuple[Any, ...]],
        attributes: list[str] | None = None,
    ) -> None:
        """Legger til `rows` i `table`. Alle rader må være like lange og
        bruke samme `attributtes`.
        """
        if not rows:
            return
        validate_table_name(table)
        command = f"INSERT INTO {table} "
        if attributes is not None:
            validate_attribute_names(attributes)
            command += f"({', '.join(attributes)}) "
        command += f"VALUES ({', '.join(('?') * len(rows[0]))})"
        for row in rows:
            self.cursor.execute(command, row)

    def book_reserved_seats(self) -> None:
        """Leser fra filene i `reservations` og legger til et
        billettkjøp per fil og lager en billett til alle reserverte
        seter i den respektive filen.
        """
        for i, info in enumerate(
            # fmt: off
            (
                ("hovedscenen", "Kongsemnene", HOVEDSCENE_STOLER),
                ("gamle-scene", "Størst av alt er kjærligheten", GAMLE_SCENE_STOLER),
            ),
            # fmt: on
            start=1,
        ):
            filename, play, chairs = info
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
        # fmt: off
        self.insert_rows("Teaterstykke", TEATERSTYKKER)
        self.insert_rows("Gruppe", GRUPPER)
        self.insert_rows("Oppgave", OPPGAVER)
        self.insert_rows("Ansatt", ANSATTE, ["Ansattstatus", "Navn", "TeaterstykkeNavn", "OppgaveNavn"])
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
        # fmt: off
        self.book_reserved_seats()

    def close(self, commit: bool = False) -> None:
        """Lukker tilkoblingen til databasen. Må kjøres til slutt.
        Commiter ikke by default.
        """
        self.con.execute("PRAGMA analysis_limit=1000")
        self.con.execute("PRAGMA optimize")
        if commit:
            self.con.commit()
        self.con.close()
