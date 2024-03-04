from creation.database_connection import DatabaseConnection
from creation.validators import validate_input


class DatabaseQueryer(DatabaseConnection):
    def order_tickets(self) -> None:
        print("Ønsker du å kjøpe billetter? [j/n]")
        # if validate_input(["j", "n"]) == "n":
        #     return

        print("Hva er ditt telefonnummer?")
        # phone = input("")
        phone = "004700000000"
        name = self.cursor.execute(
            "SELECT Navn FROM Kundeprofil WHERE Mobilnummer = ?", (phone,)
        ).fetchone()
        if name is None:
            print("Du har ingen kundeprofil. Vil du opprette en? [j/n]")
            if validate_input(["j", "n"]) == "n":
                return

            print("Hva er ditt navn?")
            name = input("")
            print("Hva er din adresse?")
            address = input("")
            self.insert_rows("Kundeprofil", [(phone, address, name)])
        else:
            name = name[0]

        print(f"Velkommen, {name}!")
        print("Hvilken forestilling ønsker du å se?")
        # play = validate_input(["Kongsemnene", "Størst av alt er kjærligheten"])
        play = "Størst av alt er kjærligheten"

        dates = [
            f"{day}/{month}"
            for day, month in self.cursor.execute(
                "SELECT DagVises, MånedVises FROM Forestilling "
                "WHERE TeaterstykkeNavn = ? "
                "ORDER BY MånedVises ASC, DagVises ASC",
                (play,),
            )
        ]

        print("Hvilken dato vil du se forestillingen?")
        # day, month = [
        #     int(number) for number in validate_input(dates).split("/")
        # ]
        day, month = 3, 2

        print("Hvor mange billetter ønsker du?")
        # amount = int(input(""))
        amount = 9

        # Funker ikke
        fitting_seats = self.cursor.execute(
            "SELECT Stol.RadNummer, Stol.Område, COUNT(Nummer) AS Antall FROM Stol "
            "LEFT OUTER JOIN Billett ON (Nummer = StolNummer AND Stol.RadNummer = Billett.RadNummer AND Stol.Område = Billett.Område) "
            "INNER JOIN Billettkjøp ON (BillettkjøpID = ID) "
            "WHERE Billettkjøp.TeaterstykkeNavn = ? AND DagVises = ? AND MånedVises = ? "
            "GROUP BY Stol.RadNummer, Stol.Område "
            "HAVING Antall < 18 - ?",
            (play, day, month, amount),
        ).fetchall()
        print(fitting_seats)
