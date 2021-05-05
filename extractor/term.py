

class Term:

    def __init__(self) -> None:

        self.exist = None
        self.id = None
        self.definition = []
        self.r_term = None
        self.r_pos = []

    def __repr__(self) -> str:
        return repr(f"{self.exist} {self.id} {self.r_term} {self.r_pos}")
