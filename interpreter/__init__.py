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
        self.loop_idx = None
        self.raw_lines = [l.strip() for l in self.file.readlines()]

    def run(self):
        """Run program.
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
        tokens = line.split()

        if len(tokens) >= 1 and tokens[0] == '\\':
            # Comment, no-op
            pass
        elif len(tokens) >= 1 and tokens[0] == 'IF':
            # IF ... (ELSE) THEN ;
            self.interp_if(tokens)
        elif len(tokens) >= 1 and tokens[0] == 'DO':
            # DO ... LOOP ;
            self.interp_loop(tokens)
        else:
            # Single tokens
            for token in tokens:
                self.interp_token(token)

        self.pc += 1

    def interp_token(self, token: str):
        """Interprets single token.
        """

        # === Comment words ===
        if token == 'IS-COMMENT':
            self.interp_is_comment()
        elif token == 'READ-COMMENT':
            self.interp_read_comment()
        elif token == 'COMMENT':
            self.interp_comment()
        elif token == 'UNCOMMENT':
            self.interp_uncomment()
        elif token == 'TOGGLE-COMMENT':
            self.interp_toggle_comment()
        elif token == 'COMMENT-RANGE':
            self.interp_comment_range()
        elif token == 'UNCOMMENT-RANGE':
            self.interp_uncomment_range()
        elif token == 'TOGGLE-COMMENT-RANGE':
            self.interp_toggle_comment_range()

        # === Core words ===
        elif token == '+':
            self.interp_add()
        elif token == 'KEY':
            self.interp_key()
        elif token == '.':
            self.interp_dot()
        elif token == 'I':
            self.interp_i()
        elif token == 'DUP':
            self.interp_dup()
        elif token == 'INVERT':
            self.interp_invert()
        elif token.isdigit():
            self.interp_number(token)
        else:
            raise RuntimeError(f'unexpected symbol "{token}"')
