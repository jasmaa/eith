class NotCommentException(Exception):
    pass


class Interpreter:
    """Eith interpreter.
    """

    def __init__(self, file):
        self.file = file
        self.stack = []
        self.pc = 0
        self.has_more = True
        self.raw_lines = [l.strip() for l in self.file.readlines()]

    def step(self):
        # EOF
        if self.pc >= len(self.raw_lines):
            self.has_more = False
            return

        raw_line = self.raw_lines[self.pc]
        line = raw_line.upper()

        if line == 'IS-COMMENT':
            # Is comment
            idx = self.stack.pop() - 1
            self.stack.append(-1 if self.raw_lines[idx][:2] == '\ ' else 0)
        elif line == 'READ-COMMENT':
            # Read comment
            idx = self.stack.pop() - 1
            if self.raw_lines[idx][:2] == '\ ':
                a = int(self.raw_lines[idx][2:])
                self.stack.append(a)
            else:
                raise NotCommentException
        elif line == 'COMMENT':
            # Comment
            idx = self.stack.pop() - 1
            self.raw_lines[idx] = f'\ {self.raw_lines[idx]}'
        elif line == 'UNCOMMENT':
            # Uncomment
            idx = self.stack.pop() - 1
            if self.raw_lines[idx][:2] == '\ ':
                self.raw_lines[idx] = self.raw_lines[idx][2:]
            else:
                raise NotCommentException
        elif line == 'TOGGLE-COMMENT':
            # Toggle comment
            idx = self.stack.pop() - 1
            if self.raw_lines[idx][:2] == '\ ':
                self.raw_lines[idx] = self.raw_lines[idx][2:]
            else:
                self.raw_lines[idx] = f'\ {self.raw_lines[idx]}'
        elif line == 'COMMENT-RANGE':
            # Comment range
            b = self.stack.pop() - 1
            a = self.stack.pop() - 1
            for i in range(a, b):
                self.raw_lines[i] = f'\ {self.raw_lines[i]}'
        elif line == 'UNCOMMENT-RANGE':
            # Uncomment range
            b = self.stack.pop() - 1
            a = self.stack.pop() - 1
            for i in range(a, b):
                if self.raw_lines[i][:2] == '\ ':
                    self.raw_lines[i] = self.raw_lines[i][2:]
                else:
                    raise NotCommentException
        elif line == 'TOGGLE-COMMENT-RANGE':
            # Toggle comment range
            b = self.stack.pop() - 1
            a = self.stack.pop() - 1
            for i in range(a, b):
                if self.raw_lines[i][:2] == '\ ':
                    self.raw_lines[i] = self.raw_lines[i][2:]
                else:
                    self.raw_lines[i] = f'\ {self.raw_lines[i]}'
        elif line == '+':
            # Add
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)
        elif line == 'KEY':
            a = int(input())
            self.stack.append(a)
        elif line == '.':
            # Print
            print(self.stack.pop())
        elif line.isdigit():
            # Number
            self.stack.append(int(line))

        self.pc += 1
