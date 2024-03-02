import os
import sqlite3
from rows import (
    AKTER,
    ANSATTE,
    BILLETTER,
    BILLETTKJOEP,
    DATOER,
    DELTAR_I,
    FORESTILLINGER,
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
with open(SQL_FILE, encoding="utf-8") as file:
    con.executescript(file.read())


def _validate_table(table_name: str) -> None:
    """Validerer tabellnavnet. Case-sensitiv."""
    if table_name not in TABLES:
        raise ValueError(f"Ugyldig tabell: {table_name}")


def print_all_rows(table_name: str) -> None:
    _validate_table(table_name)
    print(f"--------------------------{table_name}--------------------------")
    for row in cursor.execute(f"SELECT * FROM {table_name}"):
        print(row)


def insert_rows(
    table_name: str, rows: list, attributes: list[str] | None = None
) -> None:
    if not rows:
        return
    _validate_table(table_name)
    command = f"INSERT INTO {table_name} "
    if attributes is not None:
        command += f"({', '.join(attributes)}) "
    command += f"VALUES ({', '.join(['?'] * len(rows[0]))})"
    for row in rows:
        cursor.execute(command, row)


def populate_database() -> None:
    insert_rows("Teaterstykke", TEATERSTYKKER)
    insert_rows("Gruppe", GRUPPER)
    insert_rows("Oppgave", OPPGAVER)
    # fmt: off
    insert_rows(
        "Ansatt",
        ANSATTE,
        ["Ansattstatus", "Navn", "TeaterstykkeNavn", "OppgaveNavn"],
    )
    # fmt: on
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
    # fmt: off
    insert_rows(
        "Billettkjøp",
        BILLETTKJOEP,
        ["MånedKjøpt", "DagKjøpt", "KundeprofilMobilnummer", "TeaterstykkeNavn", "SalNavn", "MånedVises", "DagVises"],
    )
    # fmt: on
    insert_rows("Billett", BILLETTER)


def create_seat_reservations() -> None:
    # filename, play
    for i, info in enumerate(
        (
            ("hovedscenen", "Kongsemnene"),
            ("gamle-scene", "Størst av alt er kjærligheten"),
        ),
        start=1,
    ):
        filename, play = info
        scene = " ".join(filename.split("-")).title()
        with open(f"reservations/{filename}.txt", encoding="utf-8") as file:
            _, month, day = file.readline().split("-")
            seats_string = "".join(
                line.strip()
                for line in reversed(file.readlines())
                if line[0] in {"0", "1"}
            )

        # fmt: off
        insert_rows(
            "Billettkjøp",
            [(i, 1, 1, "004700000000", play, scene, int(month), int(day))],
        )
        # fmt: on

        for j, seat in enumerate(seats_string):
            if seat == "0":
                continue
            insert_rows(
                "Billett",
                [(i, *HOVEDSCENE_STOLER[j], play, "Ordinær")],
            )


populate_database()
create_seat_reservations()

for table in TABLES:
    if table not in {"Dato", "Stol"}:
        print_all_rows(table)

con.execute("PRAGMA analysis_limit=1000")
con.execute("PRAGMA optimize")
# con.commit()
con.close()
