"""Helper shared by the three exercises."""


def mean(values):
    """Return the arithmetic mean of a non-empty list of finite real numbers."""
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)
