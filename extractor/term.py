

class Term:

    def __init__(self, ) -> None:

        self.id = None
        self.r_term = None
        self.r_pos = []

    def __repr__(self) -> str:
        return repr(self.id + " " + self.r_term + " " + str(self.r_pos))
