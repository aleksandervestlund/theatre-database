import os
import sqlite3
from typing import Any
from rows import (
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


DB_FILE = "teater.db"
SQL_FILE = "create.sql"

# Lag ny .db fil
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
con = sqlite3.connect(DB_FILE)
con.execute("PRAGMA foreign_keys = ON")
cursor = con.cursor()
with open(SQL_FILE, encoding="utf-8") as sql:
    con.executescript(sql.read())


def _validate_table_name(table_name: str) -> None:
    """Validerer tabellnavnet. Case-sensitiv."""
    if table_name not in TABLES:
        raise ValueError(f"Ugyldig tabellnavn: {table_name}.")


def print_all_rows(table_name: str) -> None:
    _validate_table_name(table_name)
    dashes = "-" * ((92 - len(table_name)) // 2)
    print(f"{dashes}{table_name}{dashes}")
    for row in cursor.execute(f"SELECT * FROM {table_name}"):
        print(row)


def insert_rows(
    table_name: str, rows: list[Any], attributes: list[str] | None = None
) -> None:
    if not rows:
        return
    _validate_table_name(table_name)
    command = f"INSERT INTO {table_name} "
    if attributes is not None:
        command += f"({', '.join(attributes)}) "
    command += f"VALUES ({', '.join(('?') * len(rows[0]))})"
    for row in rows:
        cursor.execute(command, row)


def create_seat_reservations() -> None:
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
        with open(f"reservations/{filename}.txt", encoding="utf-8") as file:
            month, day = [
                int(number) for number in file.readline().split("-")[1:]
            ]
            seats_string = "".join(
                line.strip()
                for line in reversed(file.readlines())
                if line[0] in {"0", "1", "x"}
            )

        insert_rows(
            "Billettkjøp",
            [(i, 1, 1, KUNDEPROFILER[0][0], play, scene, month, day)],
        )
        for j, seat in enumerate(seats_string):
            if seat != "1":
                continue
            insert_rows("Billett", [(i, *chairs[j], play, "Ordinær")])


def populate_database() -> None:
    # fmt: off
    insert_rows("Teaterstykke", TEATERSTYKKER)
    insert_rows("Gruppe", GRUPPER)
    insert_rows("Oppgave", OPPGAVER)
    insert_rows("Ansatt", ANSATTE, ["Ansattstatus", "Navn", "TeaterstykkeNavn", "OppgaveNavn"])
    insert_rows("Akt", AKTER, ["TeaterstykkeNavn", "Nummer"])
    insert_rows("Rolle", ROLLER)
    insert_rows("DeltarI", DELTAR_I)
    insert_rows("Skuespiller", SKUESPILLERE, ["Navn"])
    insert_rows("SpillerRolle", SPILLER_ROLLER)
    insert_rows("Dato", DATOER)
    insert_rows("Sal", SALER)
    insert_rows("Stol", STOLER)
    insert_rows("Forestilling", FORESTILLINGER)
    insert_rows("Kundeprofil", KUNDEPROFILER)
    # fmt: on
    create_seat_reservations()


populate_database()

for table in TABLES:
    if table not in {"Dato", "Stol", "Billett"}:
        print_all_rows(table)

con.execute("PRAGMA analysis_limit=1000")
con.execute("PRAGMA optimize")
# con.commit()
con.close()
