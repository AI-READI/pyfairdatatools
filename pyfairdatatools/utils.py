"""A sample module."""


def feet_to_meters(feet):
    """Convert feet to meters."""
    try:
        value = float(feet)
    except ValueError as error:
        print(f"Could not convert {feet} to float")
        raise ValueError(f"Invalid input: {feet}") from error

    return (0.3048 * value * 10000.0 + 0.5) / 10000.0
