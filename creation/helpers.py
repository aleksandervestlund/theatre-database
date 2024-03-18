import os
import re
from collections.abc import Iterable
from sqlite3 import OperationalError
from typing import Any

from creation.config import ATTRIBUTES, TABLES


def validate_table_name(table_name: str) -> None:
    """Validerer tabellnavnet for å forhindre SQL-injection.
    Case-sensitiv.

    :param str table_name: Tabellnavn
    """
    if table_name not in TABLES:
        raise OperationalError(f"Ugyldig tabellnavn: {table_name}.")


def validate_attribute_names(attribute_names: Iterable[str]) -> None:
    """Validerer attributtnavn for å forhindre SQL-injection.
    Case-sensitiv.

    :param Iterable[str] attribute_names: Attributtnavn
    """
    for attribute in attribute_names:
        if attribute not in ATTRIBUTES:
            raise OperationalError(f"Ugyldig attributtnavn: {attribute}.")


def validate_input(legal_answers: list[str]) -> str:
    """Tar inn input fra brukeren og sjekker at det er gyldig.
    Case-sensitivt.

    :param list[str] legal_answers: Lovlige input-verdier
    """
    print(f"Mulige svar: {', '.join(legal_answers)}")
    while (answer := input("[SVAR]: ")) not in legal_answers:
        print("Ugyldig input. Prøv igjen.")
    return answer


def validate_phone_number(phone_number: str) -> bool:
    """Validerer om telefonnummeret er et gyldig norsk telefonnummer."""
    return re.fullmatch(r"(0047)?\d{8}", phone_number) is not None


def print_header(header: str) -> None:
    """Printer ut overskrift."""
    length = 56
    print(f"+{'-' * length}+")
    print(f"|{header:^{length}}|")
    print(f"+{'-' * length}+")


def pretty_print(attributes: list[str], rows: list[tuple[Any, ...]]) -> None:
    """Printer ut en tabell med attributter og rader. Hver rad må ha
    like mange elementer som det er attributter.

    :param list[str] attributes: Attributtene som skal stå over tabellen
    :param list[tuple] rows: Radene som skal printes ut
    """
    if not rows:
        print("Ingen resultater.")
        return

    max_lengths = [len(attribute) for attribute in attributes]
    for i in range(len(rows[0])):
        for row in rows:
            max_lengths[i] = max(max_lengths[i], len(str(row[i])))

    separator = f"+{'+'.join('-' * (length + 2) for length in max_lengths)}+"

    print(separator)
    for i, attribute in enumerate(attributes):
        print(f"| {attribute:^{max_lengths[i]}}", end=" ")
    print("|")
    print(separator)

    for row in rows:
        for i, value in enumerate(row):
            print(f"| {value:<{max_lengths[i]}}", end=" ")
        print("|")
    print(separator)


def clear_terminal() -> None:
    """Tømmer terminalen."""
    os.system("cls" if os.name == "nt" else "clear")
