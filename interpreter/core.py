from typing import List


class CoreInterpreterMixin:
    """Eith Core interpreter mixin.
    """

    def interp_add(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def interp_sub(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)

    def interp_key(self):
        a = int(input())
        self.stack.append(a)

    def interp_dot(self):
        print(self.stack.pop())

    def interp_number(self, token: str):
        self.stack.append(int(token))

    def interp_if(self, tokens: List[str]):
        if tokens[-1] != ';':
            raise SyntaxError('missing ";".')
        if tokens[-2] != 'THEN':
            raise SyntaxError('missing "THEN".')

        else_idx = tokens.index('ELSE') if 'ELSE' in tokens else len(tokens)-2

        v = self.stack.pop()
        interp_tokens = (
            tokens[else_idx+1:len(tokens)-2] if v == 0 else tokens[1:else_idx]
        )
        for token in interp_tokens:
            self.interp_token(token)

    def interp_do_loop(self, tokens: List[str]):
        if tokens[-1] != ';':
            raise SyntaxError('missing ";".')
        if tokens[-2] != 'LOOP':
            raise SyntaxError('missing "LOOP".')

        interp_tokens = tokens[1:len(tokens)-2]

        a = self.stack.pop()
        b = self.stack.pop()
        for i in range(a, b):
            self.loop_idx = i
            for token in interp_tokens:
                self.interp_token(token)
        self.loop_idx = None

    def interp_i(self):
        if self.loop_idx == None:
            raise RuntimeError('use of "i" outside of loop is not allowed.')
        self.stack.append(self.loop_idx)

    def interp_begin_until(self, tokens: List[str]):
        if tokens[-1] != ';':
            raise SyntaxError('missing ";".')
        if tokens[-2] != 'UNTIL':
            raise SyntaxError('missing "UNTIL".')

        interp_tokens = tokens[1:len(tokens)-2]

        while self.stack[-1] != 0:
            for token in interp_tokens:
                self.interp_token(token)

    def interp_dup(self):
        v = self.stack.pop()
        self.stack.append(v)
        self.stack.append(v)

    def interp_invert(self):
        v = self.stack.pop()
        self.stack.append(-1 if v == 0 else 0)
