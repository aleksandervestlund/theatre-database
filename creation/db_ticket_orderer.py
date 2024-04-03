from creation.config import TODAY_DAY, TODAY_MONTH
from creation.db_connector import DBConnector
from creation.helpers import (
    clear_terminal,
    print_header,
    validate_input,
    validate_phone_number,
)


class DBTicketOrderer(DBConnector):
    def ask_user(self) -> None:
        if not self.validate_tables():
            return
        if not self.validate_rows():
            return
        if not self.validate_tickets():
            return

        clear_terminal()
        print_header("Bestill billetter")

        print("Hva er ditt telefonnummer?")
        while not validate_phone_number(phone := input("[SVAR]: ")):
            print("Ugyldig telefonnummer. Prøv igjen.")
        if len(phone) == 8:
            phone = f"0047{phone}"

        name = self.cur.execute(
            "SELECT Navn FROM Kundeprofil WHERE Mobilnummer = ?", (phone,)
        ).fetchone()
        if name is None:
            print("Du har ingen kundeprofil. Vil du opprette en?")
            if validate_input(["j", "n"]) == "n":
                print("Takk for besøket!")
                input("Trykk enter for å fortsette.")
                return
            name = self.create_user(phone)
            self.con.commit()
        else:
            name = name[0]

        print(f"Velkommen, {name}!")
        play = self.get_play()
        stage = self.get_stage(play)
        day, month = self.get_date(play)

        groups = self.get_group(play)
        amount = len(groups)

        fitting_seats = self.get_fitting_seats(play, stage, day, month, amount)
        if not fitting_seats:
            print(
                "Ingen rader med så mange tilgjengelige seter. Prøv igjen "
                "senere."
            )
            input("Trykk enter for å fortsette.")
            return

        print("Følgende rader er tilgjengelige. Hvilken ønsker du?")
        area, row = validate_input(
            [f"{area}:{row}" for area, row in fitting_seats]
        ).split(":")
        row = int(row)

        seat_numbers = self.get_seat_numbers(
            play, stage, day, month, amount, area, row
        )
        ticket_id = self.book_tickets(
            phone, play, stage, day, month, area, row, seat_numbers, groups
        )
        self.con.commit()

        price = self.calculate_price(ticket_id)
        print(f"Takk for handelen! Prisen for alle billettene er {price} kr.")
        input("Trykk enter for å fortsette.")

    def validate_tickets(self) -> bool:
        """Sjekker at det finnes forhåndsbestillinger."""
        if not self.cur.execute("SELECT ID FROM Billettkjøp").fetchall():
            print("Forhåndsbestillinger må leses.")
            input("Trykk enter for å fortsette.")
            return False
        return True

    def create_user(self, phone: str) -> str:
        """Lager en ny kundeprofil."""
        print("Hva er ditt navn?")
        name = input("[SVAR]: ")

        print("Hva er din adresse?")
        address = input("[SVAR]: ")
        self.insert_rows("Kundeprofil", [(phone, address, name)])

        return name

    def get_play(self) -> str:
        """Finner lovlige teaterstykker og lar brukeren velge."""
        print("Hvilken forestilling ønsker du å se?")
        plays = [
            play[0]
            for play in self.cur.execute(
                "SELECT Navn FROM Teaterstykke"
            ).fetchall()
        ]
        return validate_input(plays)

    def get_stage(self, play: str) -> str:
        """Finner salen forestillingen spilles i."""
        return self.cur.execute(
            """
            SELECT SalNavn
            FROM Teaterstykke
                INNER JOIN Forestilling
                    ON Navn = TeaterstykkeNavn
            WHERE Navn = ?
            """,
            (play,),
        ).fetchone()[0]

    def get_date(self, play: str) -> tuple[int, int]:
        """Finner alle datoer forestillingen spilles og lar brukeren
        velge.
        """
        dates = [
            f"{day}/{month}"
            for day, month in self.cur.execute(
                """
                SELECT DagVises, MånedVises
                FROM Forestilling
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

        return day, month

    def get_group(self, play: str) -> list[str]:
        """Finner alle grupper og lar brukeren velge."""
        all_groups = [
            group[0]
            for group in self.cur.execute(
                "SELECT Navn FROM Gruppe WHERE TeaterstykkeNavn = ?",
                (play,),
            ).fetchall()
        ]

        groups = []
        while True:
            print("Hva slags billetter ønsker du?")
            group = validate_input(all_groups)

            print("Hvor mange billetter ønsker du?")
            while not (amount := input("[SVAR]: ")).isdigit():
                print("Ugyldig antall. Prøv igjen.")
            amount = int(amount)
            groups.extend([group] * amount)

            print("Ønsker du fler?")
            if validate_input(["j", "n"]) == "n":
                break

        return groups

    def get_fitting_seats(
        self, play: str, stage: str, day: int, month: int, amount: int
    ) -> list[tuple[str, int]]:
        """Finner rader med nok ledige seter."""
        return self.cur.execute(
            """
            SELECT Område, RadNummer
            FROM Stol AS S1
            WHERE SalNavn = ? AND (RadNummer, Område, Nummer) NOT IN (
                SELECT S2.RadNummer, S2.Område, S2.Nummer
                FROM Stol AS S2
                    INNER JOIN Billett
                        ON S2.Nummer = StolNummer
                            AND S2.RadNummer = Billett.RadNummer
                            AND S2.Område = Billett.Område
                    INNER JOIN Billettkjøp
                        ON BillettkjøpID = ID
                WHERE S2.Salnavn = S1.SalNavn
                    AND Billettkjøp.TeaterstykkeNavn = ?
                    AND DagVises = ?
                    AND MånedVises = ?
            )
            GROUP BY RadNummer, Område
            HAVING COUNT(Nummer) >= ?
            ORDER BY Område ASC, RadNummer ASC
            """,
            (stage, play, day, month, amount),
        ).fetchall()

    def get_seat_numbers(
        self,
        play: str,
        stage: str,
        day: int,
        month: int,
        amount: int,
        area: str,
        row: int,
    ) -> list[int]:
        """Finner ledige seter."""
        return [
            seat[0]
            for seat in self.cur.execute(
                """
                SELECT Nummer
                FROM Stol AS S1
                WHERE SalNavn = ?
                    AND Område = ?
                    AND RadNummer = ?
                    AND (RadNummer, Område, Nummer) NOT IN (
                        SELECT S2.RadNummer, S2.Område, S2.Nummer
                        FROM Stol AS S2
                            INNER JOIN Billett
                                ON S2.Nummer = StolNummer
                                    AND S2.RadNummer = Billett.RadNummer
                                    AND S2.Område = Billett.Område
                            INNER JOIN Billettkjøp
                                ON BillettkjøpID = ID
                        WHERE S2.Salnavn = S1.SalNavn
                            AND S2.Område = S1.Område
                            AND S2.RadNummer = S1.RadNummer
                            AND Billettkjøp.TeaterstykkeNavn = ?
                            AND DagVises = ?
                            AND MånedVises = ?
                    )
                LIMIT ?
                """,
                (stage, area, row, play, day, month, amount),
            ).fetchall()
        ]

    def book_tickets(
        self,
        phone: str,
        play: str,
        stage: str,
        day: int,
        month: int,
        area: str,
        row: int,
        seat_numbers: list[int],
        groups: list[str],
    ) -> int:
        """Fyller tabellene med billettkjøp og billetter."""
        # INTEGER har AUTOINCREMENT, men må vite hvilken ID som ble tildelt
        ticket_id = self.cur.execute(
            "SELECT MAX(ID) + 1 FROM Billettkjøp"
        ).fetchone()[0]

        # fmt: off
        self.insert_rows(
            "Billettkjøp",
            [(ticket_id, TODAY_MONTH, TODAY_DAY, phone, play, stage, month, day)],
        )
        
        self.insert_rows(
            "Billett",
            [(ticket_id, stage, seat, row, area, play, group) for seat, group in zip(seat_numbers, groups)],
        )
        # fmt: on
        return ticket_id

    def calculate_price(self, ticket_id: int) -> int:
        """Regner ut prisen for billettene."""
        prices = self.cur.execute(
            """
            SELECT COUNT(StolNummer), Pris, Pris10
            FROM Billett 
                INNER JOIN Gruppe
                    ON Billett.TeaterstykkeNavn = Gruppe.TeaterstykkeNavn
                        AND GruppeNavn = Navn
            WHERE BillettkjøpID = ?
            GROUP BY Pris, Pris10
            """,
            (ticket_id,),
        ).fetchall()

        return sum(
            count * (price1 if count < 10 else price10)
            for count, price1, price10 in prices
        )
