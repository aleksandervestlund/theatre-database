import sqlite3
from abc import ABC, abstractmethod
from collections.abc import Iterable
from sqlite3 import OperationalError
from typing import Any

from creation.config import DB_FILE
from creation.helpers import validate_attribute_names, validate_table_name


class DBConnector(ABC):
    def __init__(self) -> None:
        self.connect()

    @abstractmethod
    def ask_user(self) -> None:
        """Spør brukeren hva de vil gjøre og kjører de tilhørende
        funksjonene.
        """

    def connect(self) -> None:
        """Kobler til databasen. Blir kjørt i konstruktøren."""
        self.con = sqlite3.connect(DB_FILE)
        self.con.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.con.cursor()

    def reconnect(self) -> None:
        self.close()
        self.connect()

    def validate_tables(self) -> bool:
        try:
            # Sjekker om vilkårlig tabell finnes
            self.con.execute("SELECT Mobilnummer FROM Kundeprofil")
        except OperationalError:
            print("Tabellene er ikke opprettet.")
            input("Trykk enter for å fortsette.")
            self.reconnect()
            return False
        return True

    def validate_rows(self) -> bool:
        # Sjekker om vilkårlig rad finnes
        if not self.con.execute("SELECT Navn FROM Teaterstykke").fetchall():
            print("Tabellene er tomme.")
            input("Trykk enter for å fortsette.")
            return False
        return True

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
        :param list[tuple] rows: Rader som skal legges til
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

    def validate_tables(self) -> bool:
        """Sjekker at tabellene finnes."""
        try:
            # Sjekker om vilkårlig tabell finnes
            self.con.execute("SELECT Mobilnummer FROM Kundeprofil")
        except OperationalError:
            print("Tabellene er ikke opprettet.")
            input("Trykk enter for å fortsette.")
            return False
        return True

    def validate_rows(self) -> bool:
        """Sjekker at tabellene er fylt med forhåndsdefinerte rader."""
        # Sjekker om vilkårlig rad finnes
        if not self.con.execute("SELECT Navn FROM Teaterstykke").fetchall():
            print("Tabellene er tomme.")
            input("Trykk enter for å fortsette.")
            return False
        return True
