from operator import (
    add,
    and_,
    floordiv,
    iadd,
    iand,
    ifloordiv,
    ilshift,
    imatmul,
    imod,
    imul,
    ior,
    ipow,
    irshift,
    isub,
    itruediv,
    ixor,
    lshift,
    matmul,
    mod,
    mul,
    or_,
    pow,
    rshift,
    sub,
    truediv,
    xor,
)
from dis import _nb_ops

class VirtualMachineStateOperatorInstructions:
    def unary_negative(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                -self.stack[-1],
            ]
        )

    def unary_not(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                not self.stack[-1],
            ]
        )

    def unary_invert(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                ~self.stack[-1],
            ]
        )

    def get_iter(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                iter(self.stack[-1]),
            ]
        )

    def to_bool(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
                bool(self.stack[-1]),
            ]
        )

    def binary_subscr(self):
        return self.transition(
            stack=[
                *self.stack[:-1],
            ],
        )

    def binary_subscr(self):
        return self.transition(
            stack=[
                *self.stack[:-2],
                self.stack[-2][self.stack[-1]],
            ]
        )

    def binary_op(self):
        return self.transition(
            stack=[
                *self.stack[:-2],
                {
                    "+": add,
                    "-": sub,
                    "*": mul,
                    "/": truediv,
                    "//": floordiv,
                    "%": mod,
                    "**": pow,
                    "<<": lshift,
                    ">>": rshift,
                    "&": and_,
                    "|": or_,
                    "^": xor,
                    "@": matmul,
                    "+=": iadd,
                    "-=": isub,
                    "*=": imul,
                    "/=": itruediv,
                    "//=": ifloordiv,
                    "%=": imod,
                    "**=": ipow,
                    "<<=": ilshift,
                    ">>=": irshift,
                    "&=": iand,
                    "|=": ior,
                    "^=": ixor,
                    "@=": imatmul,
                }[_nb_ops[self.current_instruction_argument_value][1]](self.stack[-2], self.stack[-1])
            ]
        )

    def compare_op(self):
        return self.transition(
            stack=[
                *self.stack[:-2],
                {
                    "<": lambda left, right: left < right,
                    "<=": lambda left, right: left <= right,
                    ">": lambda left, right: left > right,
                    ">=": lambda left, right: left >= right,
                    "==": lambda left, right: left == right,
                    "!=": lambda left, right: left != right,
                    "in": lambda left, right: left in right,
                    "not in": lambda left, right: left not in right,
                    "is": lambda left, right: left is right,
                    "is not": lambda left, right: left is not right,
                }[self.current_instruction_argument_value](self.stack[-2], self.stack[-1])
            ]
        )
