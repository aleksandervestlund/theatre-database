import sqlite3
from abc import ABC, abstractmethod
from collections.abc import Iterable
from sqlite3 import OperationalError
from typing import Any

from creation.config import DB_FILE, TABLES
from creation.validators import validate_attribute_names, validate_table_name


class DBConnector(ABC):
    def __init__(self) -> None:
        self.connect()

    @abstractmethod
    def ask_user(self) -> None:
        """Spør brukeren hva de vil gjøre og kjører de tilhørende
        funksjonene.
        """

    def connect(self) -> None:
        self.con = sqlite3.connect(DB_FILE)
        self.con.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.con.cursor()

    def validate_connection(self) -> bool:
        try:
            self.con.execute("SELECT Mobilnummer FROM Kundeprofil")
        except OperationalError:
            print("Tabellene er ikke opprettet.")
            input("Trykk enter for å fortsette.")
            return False
        return True

    def print_table(self, table: str) -> None:
        validate_table_name(table)
        length = len(table)
        dashes = "-" * ((78 - length) // 2)
        print(f"{dashes} {table} {dashes}{'-' * (length % 2)}")
        for row in self.cursor.execute(f"SELECT * FROM {table}"):
            print(row)

    def print_all_tables(
        self, mute_tables: Iterable[str] | None = None
    ) -> None:
        """Printer alle tabellene i databasen.

        :param Iterable[str] | None mute_tables: Tabeller som ikke skal
        printes, defaulter til None
        """
        for table in TABLES:
            if mute_tables is None or table not in mute_tables:
                self.print_table(table)

    def insert_rows(
        self,
        table: str,
        rows: list[tuple[Any, ...]],
        attributes: Iterable[str] | None = None,
    ) -> None:
        """Fyller en tabell med rader. Avhengig av at `create_tables`
        har blitt kjørt først. Alle tupler i `rows` må ha samme lengde
        og bruke samme `attributes`.

        :param str table: Navn på tabellen
        :param list[tuple[Any, ...]] rows: Rader som skal legges til
        :param Iterable[str] attributes: Attributtene som skal settes
        inn, defaulter til None
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

    def close(self) -> None:
        """Lukker tilkoblingen til databasen. Må kjøres til slutt."""
        self.con.execute("PRAGMA analysis_limit=1000")
        self.con.execute("PRAGMA optimize")
        self.con.commit()
        self.con.close()
