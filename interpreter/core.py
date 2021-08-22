class CoreInterpreterMixin:
    """Forth Core interpreter mixin.
    """

    def interp_add(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def interp_key(self):
        a = int(input())
        self.stack.append(a)

    def interp_dot(self):
        print(self.stack.pop())

    def interp_number(self, line: str):
        self.stack.append(int(line))
