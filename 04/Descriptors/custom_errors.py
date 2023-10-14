class InvalidValues(Exception):
    def __init__(self, index: int):
        self.index = index

    def __str__(self):
        return f"Value at index {self.index} must be nonzero"


class InvalidColumnIndicies(Exception):
    def __init__(self, index: int):
        self.index = index

    def __str__(self):
        return f"Value at index {self.index} must be non-negative integer"


class InvalidRowOffsets(Exception):
    def __init__(self, index: int):
        self.index = index

    def __str__(self):
        return (
            f"Value at index {self.index} must be non-negative integer,"
            " greater then previous value"
        )
