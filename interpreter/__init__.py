from .comment import CommentInterpreterMixin
from .core import CoreInterpreterMixin


class Interpreter(CommentInterpreterMixin, CoreInterpreterMixin):
    """Top-level Eith interpreter.
    """

    def __init__(self, file):
        self.file = file
        self.stack = []
        self.pc = 0
        self.has_more = True
        self.raw_lines = [l.strip() for l in self.file.readlines()]

    def interp(self):
        """Interpret file.
        """

        while self.has_more:
            self.step()
        self.file.seek(0)
        self.file.write('\n'.join(self.raw_lines)+'\n')

    def step(self):
        """Steps one instruction.
        """

        # Ignore on EOF
        if self.pc >= len(self.raw_lines):
            self.has_more = False
            return

        raw_line = self.raw_lines[self.pc]
        line = raw_line.upper()

        # === Eith Comment words ===
        if line == 'IS-COMMENT':
            self.interp_is_comment(self)
        elif line == 'READ-COMMENT':
            self.interp_read_comment()
        elif line == 'COMMENT':
            self.interp_comment()
        elif line == 'UNCOMMENT':
            self.interp_uncomment()
        elif line == 'TOGGLE-COMMENT':
            self.interp_toggle_comment()
        elif line == 'COMMENT-RANGE':
            self.interp_comment_range()
        elif line == 'UNCOMMENT-RANGE':
            self.interp_uncomment_range()
        elif line == 'TOGGLE-COMMENT-RANGE':
            self.interp_toggle_comment_range()

        # === Forth Core words ===
        elif line == '+':
            self.interp_add()
        elif line == 'KEY':
            self.interp_key()
        elif line == '.':
            self.interp_dot()
        elif line.isdigit():
            self.interp_number(line)

        self.pc += 1
