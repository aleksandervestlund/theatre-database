from creation.rows import ATTRIBUTES, TABLES


def validate_table_name(table_name: str) -> None:
    """Validerer tabellnavnet. Case-sensitiv."""
    if table_name not in TABLES:
        raise ValueError(f"Ugyldig tabellnavn: {table_name}.")


def validate_attribute_names(attribute_names: list[str]) -> None:
    """Validerer attributtnavn. Case-sensitiv."""
    for attribute in attribute_names:
        if attribute not in ATTRIBUTES:
            raise ValueError(f"Ugyldig attributtnavn: {attribute}.")
