"""Example module with no pylint findings."""


def add_numbers(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def main() -> None:
    """Entry point for the script."""
    result = add_numbers(2, 3)
    print(result)


if __name__ == "__main__":
    main()
