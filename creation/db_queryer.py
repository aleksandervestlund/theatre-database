from typing import Any

from creation.db_connector import DBConnector
from creation.validators import validate_input


def pretty_print(attributes: list[str], rows: list[tuple[Any, ...]]) -> None:
    """Printer ut en tabell med attributter og rader. Hver rad må ha
    like mange elementer som det er attributter.

    :param list[str] attributes: Attributtene som skal stå over
    tabellen
    :param list[tuple] rows: Radene som skal printes ut
    """
    max_lengths = [len(attribute) for attribute in attributes]
    for i in range(len(rows[0])):
        for row in rows:
            max_lengths[i] = max(max_lengths[i], len(str(row[i])))

    separator = "+"
    for length in max_lengths:
        separator += f"{'-' * (length + 2)}+"

    print(separator)
    for i, attribute in enumerate(attributes):
        print(f"| {attribute:<{max_lengths[i]}}", end=" ")
    print("|")
    print(separator)

    for row in rows:
        for i, value in enumerate(row):
            print(f"| {value:<{max_lengths[i]}}", end=" ")
        print("|")
    print(separator)


class DBQueryer(DBConnector):
    def ask_user(self) -> None:
        if not self.validate_connection():
            return
        if not self.validate_has_rows():
            return

        while True:
            print("+--------------------------------------------------------+")
            print("1: Forestillinger på gitt dato.")
            print("2: Navn på skuespillere.")
            print("3: Bestselgende forestillinger.")
            print("4: Skuespillere i samme akt som gitt skuespiller.")
            print("5: Gå tilbake.")
            print("Hva vil du gjøre?")

            match validate_input([str(i) for i in range(1, 6)]):
                case "1":
                    self.get_plays()
                case "2":
                    self.get_actors()
                case "3":
                    self.get_best_sellers()
                case "4":
                    self.get_actors_in_same_act()
                case "5":
                    return

            input("Trykk enter for å fortsette.")

    def get_plays(self) -> None:
        """Spør brukeren om en dato og printer ut forestillinger for den
        datoen.
        """
        all_dates = [
            f"{day}/{month}"
            for day, month in self.cursor.execute(
                """
                SELECT DagVises, MånedVises FROM Forestilling
                GROUP BY DagVises, MånedVises
                ORDER BY MånedVises ASC, DagVises ASC
                """
            )
        ]
        print("Hvilken dato vil du se forestillinger for?")
        day, month = [
            int(number) for number in validate_input(all_dates).split("/")
        ]

        rows = self.cursor.execute(
            """
            SELECT Forestilling.TeaterstykkeNavn, Forestilling.SalNavn,
                COUNT(Billett.BillettkjøpID)
            FROM Forestilling LEFT OUTER JOIN Billettkjøp
                ON Forestilling.TeaterstykkeNavn = Billettkjøp.TeaterstykkeNavn 
                    AND Forestilling.SalNavn = Billettkjøp.SalNavn
                    AND Forestilling.DagVises = Billettkjøp.DagVises 
                    AND Forestilling.MånedVises = Billettkjøp.MånedVises
                LEFT OUTER JOIN Billett
                    ON Billettkjøp.ID = Billett.BillettkjøpID
            WHERE Forestilling.DagVises = ? AND Forestilling.MånedVises = ?
            GROUP BY Forestilling.TeaterstykkeNavn, Forestilling.SalNavn
            ORDER BY Forestilling.TeaterstykkeNavn ASC
            """,
            (day, month),
        ).fetchall()
        pretty_print(["TeaterstykkeNavn", "SalNavn", "Antall"], rows)

    def get_actors(self) -> None:
        """Printer ut skuespillerene og hvilke roller de har."""
        rows = self.cursor.execute(
            """
            SELECT Akt.TeaterstykkeNavn, Skuespiller.Navn,
                SpillerRolle.RolleNavn
            FROM Akt INNER JOIN DeltarI
                ON Akt.Nummer = DeltarI.AktNummer
                    AND Akt.TeaterstykkeNavn = DeltarI.TeaterstykkeNavn
                INNER JOIN SpillerRolle USING (RolleNavn)
                INNER JOIN Skuespiller
                    ON SpillerRolle.SkuespillerID = Skuespiller.ID
            GROUP BY SpillerRolle.RolleNavn
            ORDER BY Akt.TeaterstykkeNavn ASC, Skuespiller.Navn ASC,
                SpillerRolle.RolleNavn ASC
            """
        ).fetchall()
        pretty_print(["TeaterstykkeNavn", "Navn", "RolleNavn"], rows)

    def get_best_sellers(self) -> None:
        """Printer ut forestillinger og hvor mange billetter som er
        solgt.
        """
        rows = self.cursor.execute(
            """
            SELECT Forestilling.TeaterstykkeNavn, Forestilling.DagVises,
                Forestilling.MånedVises, COUNT(Billett.BillettkjøpID) AS Antall
            FROM Forestilling INNER JOIN Billettkjøp
                ON Forestilling.TeaterstykkeNavn = Billettkjøp.TeaterstykkeNavn 
                    AND Forestilling.SalNavn = Billettkjøp.SalNavn
                    AND Forestilling.DagVises = Billettkjøp.DagVises 
                    AND Forestilling.MånedVises = Billettkjøp.MånedVises
                INNER JOIN Billett ON Billettkjøp.ID = Billett.BillettkjøpID
            GROUP BY Forestilling.TeaterstykkeNavn, Forestilling.DagVises,
                Forestilling.MånedVises
            ORDER BY Antall DESC, Forestilling.MånedVises ASC,
                Forestilling.TeaterstykkeNavn ASC, Forestilling.DagVises ASC
            """
        ).fetchall()
        pretty_print(
            ["Teaterstykke", "Dag", "Måned", "Solgte billetter"], rows
        )

    def get_actors_in_same_act(self) -> None:
        all_actors = [
            actor[0]
            for actor in self.cursor.execute(
                "SELECT Navn FROM Skuespiller"
            ).fetchall()
        ]
        print("Oppgi skuespiller:")
        name = validate_input(all_actors)

        rows = self.cursor.execute(
            """
            SELECT S1.Navn, S2.Navn, DI1.TeaterstykkeNavn
            FROM Skuespiller AS S1 CROSS JOIN Skuespiller AS S2
                INNER JOIN SpillerRolle AS SR1 ON S1.ID = SR1.SkuespillerID
                INNER JOIN SpillerRolle AS SR2 ON S2.ID = SR2.SkuespillerID
                INNER JOIN DeltarI AS DI1 ON SR1.RolleNavn = DI1.RolleNavn
                INNER JOIN DeltarI AS DI2 ON SR2.RolleNavn = DI2.RolleNavn
            WHERE S1.Navn = ?
                AND S1.Navn <> S2.Navn
                AND DI1.TeaterstykkeNavn = DI2.TeaterstykkeNavn
                AND DI1.AktNummer = DI2.AktNummer
            GROUP BY S1.Navn, S2.Navn
            ORDER BY S2.Navn ASC, DI1.TeaterstykkeNavn ASC
            """,
            (name,),
        ).fetchall()
        pretty_print(["Skuespiller", "Skuespiller", "Teaterstykke"], rows)
