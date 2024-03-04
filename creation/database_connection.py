import sqlite3
from collections.abc import Iterable
from typing import Any

from creation.rows import DB_FILE, TABLES
from creation.validators import validate_attribute_names, validate_table_name


class DatabaseConnection:
    def __init__(self) -> None:
        self.con = sqlite3.connect(DB_FILE)
        self.con.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.con.cursor()

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
        attributes: list[str] | None = None,
    ) -> None:
        """Fyller en tabell med rader. Avhengig av at `create_tables`
        har blitt kjørt først. Alle tupler i `rows` må ha samme lengde
        og bruke samme `attributes`.

        :param str table: Navn på tabellen
        :param list[tuple[Any, ...]] rows: Rader som skal legges til
        :param list[str] attributes: Attributtene som skal settes inn,
        defaulter til None
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

    def close(self, commit: bool = True) -> None:
        """Lukker tilkoblingen til databasen. Må kjøres til slutt.

        :param bool commit: Om endringene på radene skal lagres,
        defaulter til True
        """
        self.con.execute("PRAGMA analysis_limit=1000")
        self.con.execute("PRAGMA optimize")
        if commit:
            self.con.commit()
        self.con.close()
