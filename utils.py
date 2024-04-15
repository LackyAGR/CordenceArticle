"""Utils file for common operations."""

# Imports
from datetime import datetime
from nanoid import generate


# Valid characters
valid_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_uid(size=11, prefix="NL", year=True):
    """Generate a unique identifier.

    Args:
        size (int, optional): Size of the random string to be generated. Defaults to 11.
        prefix (str, optional): Prefix for the unique ID. Defaults to "".

    Raises:
        TypeError: If size is not int.
        TypeError: If prefix is not str.

    Returns:
        str: Unique ID.
    """
    # Error handling for incorrect data types
    if not isinstance(size, int):
        raise TypeError("size must of type int")
    if not isinstance(prefix, str):
        raise TypeError("prefix must of type str")

    # Set current year
    this_year = str(datetime.now().year)
    # Generate random text using nanoid
    random_txt = generate(alphabet=valid_chars, size=size)
    # Create the final string without prefix
    if year:
        uid = f"{prefix}-{random_txt}-{this_year}"
    else:
        uid = f"{prefix}-{random_txt}"

    return uid