import re

from creation.config import TODAY_DAY, TODAY_MONTH
from creation.database_connection import DatabaseConnection
from creation.validators import validate_input


class DatabaseQueryer(DatabaseConnection):
    def ask_user(self) -> None:
        while True:
            print()
            print("1: Kjøp billetter.")
            print("2: Finn forestillinger.")
            print("3: Finn skuespillere.")
            print("4: Finn best solgte forestilling.")
            print("5: Finn teaterstykker.")
            print("6: Gå tilbake.")
            print("Hva vil du gjøre?")

            match validate_input([str(i) for i in range(1, 7)]):
                case "1":
                    self.order_tickets()
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass
                case "5":
                    pass
                case "6":
                    return

            input("Trykk en tast for å fortsette.")

    def order_tickets(self) -> None:
        print("Ønsker du å kjøpe billetter?")
        if validate_input(["j", "n"]) == "n":
            return

        print("Hva er ditt telefonnummer?")
        phone = input("[SVAR]: ")
        # while (
        #     not re.fullmatch(
        #         r"((((00)|\+)47)|)[49]\d{7}",
        #         (phone := input("[SVAR]: ")),
        #     )
        #     is not None
        # ):
        #     print("Ugyldig telefonnummer. Prøv igjen.")

        name = self.cursor.execute(
            "SELECT Navn FROM Kundeprofil WHERE Mobilnummer = ?", (phone,)
        ).fetchone()
        if name is None:
            print("Du har ingen kundeprofil. Vil du opprette en?")
            if validate_input(["j", "n"]) == "n":
                return

            print("Hva er ditt navn?")
            name = input("[SVAR]: ")
            print("Hva er din adresse?")
            address = input("[SVAR]: ")
            self.insert_rows("Kundeprofil", [(phone, address, name)])
        else:
            name = name[0]

        print(f"Velkommen, {name}!")
        print("Hvilken forestilling ønsker du å se?")
        plays = [
            play[0]
            for play in self.con.execute(
                "SELECT Navn FROM Teaterstykke"
            ).fetchall()
        ]
        play = validate_input(plays)
        stage = self.cursor.execute(
            """
            SELECT SalNavn
            FROM Teaterstykke INNER JOIN Forestilling ON Navn = TeaterstykkeNavn
            WHERE Navn = ?
            """,
            (play,),
        ).fetchone()[0]

        dates = [
            f"{day}/{month}"
            for day, month in self.cursor.execute(
                """
                SELECT DagVises, MånedVises FROM Forestilling
                WHERE TeaterstykkeNavn = ?
                ORDER BY MånedVises ASC, DagVises ASC
                """,
                (play,),
            )
        ]
        print("Hvilken dato vil du se forestillingen?")
        day, month = [
            int(number) for number in validate_input(dates).split("/")
        ]

        print("Hvor mange billetter ønsker du?")
        amount = int(input("[SVAR]: "))
        fitting_seats = self.cursor.execute(
            """
            SELECT Område, RadNummer
            FROM Stol AS S1
            WHERE SalNavn = ? AND (RadNummer, Område, Nummer) NOT IN (
                SELECT S2.RadNummer, S2.Område, S2.Nummer
                FROM Stol AS S2 INNER JOIN Billett ON (S2.Nummer = StolNummer
                AND S2.RadNummer = Billett.RadNummer AND S2.Område = Billett.Område)
                INNER JOIN Billettkjøp ON (BillettkjøpID = ID)
                WHERE S2.Salnavn = S1.SalNavn AND Billettkjøp.TeaterstykkeNavn = ? AND DagVises = ? AND MånedVises = ?
            )
            GROUP BY RadNummer, Område
            HAVING COUNT(Nummer) >= ?
            ORDER BY Område ASC, RadNummer ASC
            """,
            (stage, play, day, month, amount),
        ).fetchall()
        if not fitting_seats:
            print(
                "Ingen rader med så mange tilgjengelige seter. Prøv igjen "
                "senere."
            )
            return

        print("Følgende rader er tilgjengelige. Hvilken ønsker du?")
        area, row = validate_input(
            [f"{area}:{row}" for area, row in fitting_seats]
        ).split(":")
        seat_numbers = self.cursor.execute(
            """
            SELECT Nummer
            FROM Stol AS S1
            WHERE SalNavn = ? AND Område = ? AND RadNummer = ?
                AND (RadNummer, Område, Nummer) NOT IN (
                    SELECT S2.RadNummer, S2.Område, S2.Nummer
                    FROM Stol AS S2 INNER JOIN Billett ON (S2.Nummer = StolNummer
                        AND S2.RadNummer = Billett.RadNummer
                        AND S2.Område = Billett.Område)
                    INNER JOIN Billettkjøp ON (BillettkjøpID = ID)
                    WHERE S2.Salnavn = S1.SalNavn AND S2.Område = S1.Område
                        AND S2.RadNummer = S1.RadNummer
                        AND Billettkjøp.TeaterstykkeNavn = ?
                        AND DagVises = ? AND MånedVises = ?
            )
            LIMIT ?
            """,
            (stage, area, row, play, day, month, amount),
        ).fetchall()

        print("Hva slags billetter ønsker du?")
        groups = [
            group[0]
            for group in self.cursor.execute(
                "SELECT Navn FROM Gruppe WHERE TeaterstykkeNavn = ?",
                (play,),
            ).fetchall()
        ]
        group = validate_input(groups)

        # fmt: off
        self.insert_rows(
            "Billettkjøp",
            [(TODAY_MONTH, TODAY_DAY, phone, play, stage, month, day)],
            ["MånedKjøpt", "DagKjøpt", "KundeprofilMobilnummer", "TeaterstykkeNavn", "SalNavn", "MånedVises", "DagVises"],
        )
        ticket_id = self.cursor.execute(
            """
            SELECT ID FROM Billettkjøp
            WHERE MånedKjøpt = ? AND DagKjøpt = ?
                AND KundeprofilMobilnummer = ? AND TeaterstykkeNavn = ?
                AND SalNavn = ? AND MånedVises = ? AND DagVises = ?
            """,
            (TODAY_MONTH, TODAY_DAY, phone, play, stage, month, day)
        ).fetchall()[-1][0]
        self.insert_rows(
            "Billett",
            [(ticket_id, stage, seat[0], row, area, play, group) for seat in seat_numbers],
        )
        # fmt: on

        price = self.cursor.execute(
            """
            SELECT SUM(Pris) FROM Billett INNER JOIN Gruppe ON
                (Billett.TeaterstykkeNavn = Gruppe.TeaterstykkeNavn
                AND GruppeNavn = Navn)
            WHERE BillettkjøpID = ?
            """,
            (ticket_id,),
        ).fetchone()[0]

        print(f"Prisen for alle billettene er {price} kr.")
        print("Takk for handelen!")
