from typing import List


class CoreInterpreterMixin:
    """Eith Core interpreter mixin.
    """

    def interp_number(self, token: str):
        self.stack.append(int(token))

    def interp_if(self, tokens: List[str]):
        if tokens[-1] != 'THEN':
            raise SyntaxError('missing "THEN".')

        # Find else idx
        counter = 0
        idx = 0
        else_idx = len(tokens) - 1
        while idx < len(tokens):
            if tokens[idx] == 'IF':
                counter += 1
            elif tokens[idx] == 'THEN':
                counter -= 1
            if counter == 1 and tokens[idx] == 'ELSE':
                else_idx = idx
                break
            idx += 1

        v = self.stack.pop()
        interp_tokens = (
            tokens[else_idx+1:len(tokens)-1] if v == 0 else tokens[1:else_idx]
        )
        self.interp_tokens(interp_tokens)

    def interp_do_loop(self, tokens: List[str]):
        if tokens[-1] != 'LOOP':
            raise SyntaxError('missing "LOOP".')

        interp_tokens = tokens[1:len(tokens)-1]

        a = self.stack.pop()
        b = self.stack.pop()
        for i in range(a, b):
            self.loop_idx = i
            self.interp_tokens(interp_tokens)
        self.loop_idx = None

    def interp_i(self):
        if self.loop_idx == None:
            raise RuntimeError('use of "i" outside of loop is not allowed.')
        self.stack.append(self.loop_idx)

    def interp_begin_until(self, tokens: List[str]):
        if tokens[-1] != 'UNTIL':
            raise SyntaxError('missing "UNTIL".')

        interp_tokens = tokens[1:len(tokens)-1]

        while self.stack.pop() != 0:
            self.interp_tokens(interp_tokens)

    def interp_add(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def interp_sub(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)

    def interp_mult(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)

    def interp_mult_div(self):
        c = self.stack.pop()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append((a * b) // c)

    def interp_mult_div_mod(self):
        c = self.stack.pop()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append((a * b) // c)
        self.stack.append((a * b) % c)

    def interp_div(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a // b)

    def interp_div_mod(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a // b)
        self.stack.append(a % b)

    def interp_zero_lt(self):
        a = self.stack.pop()
        self.stack.append(
            -1 if a < 0 else 0
        )

    def interp_zero_eq(self):
        a = self.stack.pop()
        self.stack.append(
            -1 if a == 0 else 0
        )

    def interp_one_plus(self):
        a = self.stack.pop()
        self.stack.append(a + 1)

    def interp_one_minus(self):
        a = self.stack.pop()
        self.stack.append(a - 1)

    def interp_two_mult(self):
        a = self.stack.pop()
        self.stack.append(a << 1)

    def interp_two_div(self):
        a = self.stack.pop()
        self.stack.append(a >> 1)

    def interp_two_drop(self):
        self.stack.pop()
        self.stack.pop()

    def interp_two_dup(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a)
        self.stack.append(b)
        self.stack.append(a)
        self.stack.append(b)
    
    def interp_two_over(self):
        d = self.stack.pop()
        c = self.stack.pop()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a)
        self.stack.append(b)
        self.stack.append(c)
        self.stack.append(d)
        self.stack.append(a)
        self.stack.append(b)
    
    def interp_two_swap(self):
        d = self.stack.pop()
        c = self.stack.pop()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(c)
        self.stack.append(d)
        self.stack.append(a)
        self.stack.append(b)

    def interp_key(self):
        a = int(input())
        self.stack.append(a)

    def interp_dot(self):
        print(self.stack.pop())

    def interp_dot_string(self, tokens: List[str]):
        s = ' '.join(tokens[1:])
        print(s[:-1])

    def interp_dup(self):
        v = self.stack.pop()
        self.stack.append(v)
        self.stack.append(v)

    def interp_invert(self):
        v = self.stack.pop()
        self.stack.append(-1 if v == 0 else 0)
