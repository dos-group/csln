from unittest import TestCase, main
from . import VirtualMachine, VirtualMachineInlineHandler, VirtualMachineStateRenderer
from asyncio import run

class VirtualMachineTest(TestCase):
    def __init__(self, *positional_arguments, **keyword_arguments):
        super().__init__(
            *positional_arguments,
            **keyword_arguments,
        )

        self.__virtual_machine = VirtualMachine()

    def test_hihi(self):
        def hello(state):
            print("#" * 80)
            print(VirtualMachineStateRenderer().render(state))

            return state

        machine = VirtualMachine(
            VirtualMachineInlineHandler(
                before_line_execute=hello,
            )
        )

        run(
            machine.execute_string(
"""
y = 200

values = (
    10,
    20,
    y,
)
"""
            )
        )

    def test_pass(self):
        self.assertIsNone(self.__execute("pass").return_value_instance)

    def test_loop0(self):
        values = []

        self.__execute(
            """
for value in range(10):
    append(value)
            """,
            globals={
                "append": values.append,
                "range": range,
            }
        )

        self.assertEqual(list(range(10)), values)

    def test_function0(self):
        self.assertIsNone(
            self.__execute(
                """
def outer():
    pass

outer()
                """,
            ).return_value_instance,
        )

    def test_function1(self):
        self.assertIsNone(
            self.__execute(
                """
def outer():
    nop()

outer()
                """,
                globals={
                    "nop": lambda: None,
                }
            ).return_value_instance,
        )

    def test_function2(self):
        values = []

        self.__execute(
            """
def outer():
     nop()

     for value in range(10):
         append(value)

     nop()
     nop()

outer()
            """,
            globals={
                "nop": lambda: None,
                "append": values.append,
                "range": range,
            }
        )

        self.assertEqual(list(range(10)), values)

    def test_function2(self):
        values = []

        self.__execute(
            """
def outer():
     nop()

     for value in range(10):
         append(value)

     nop()
     nop()

outer()
            """,
            globals={
                "nop": lambda: None,
                "append": values.append,
                "range": range,
            }
        )

        self.assertEqual(list(range(10)), values)

    def test_format0(self):
        value = []

        def append(f):
            value.append(f)

        self.__execute(
            """
append("".format())
            """,
            globals={
                "append": value.append,
            }
        )

        self.assertEqual(
            [""],
            value,
        )

    def test_format1(self):
        value = []

        def append(f):
            value.append(f)

        self.__execute(
            """
append("{} World {}".format("Hello", 119))
            """,
            globals={
                "append": value.append,
            }
        )

        self.assertEqual(
            ["Hello World 119"],
            value,
        )

    def test_store_subscription0(self):
        state = self.__execute(
            """
value["hello"] = "world"
            """,
            globals={
                "value": {},
            }
        )

        self.assertEqual(
            {
                "hello": "world",
            },
            state.globals["value"],
        )

    def test_unpack(self):
        state = self.__execute(
            """
object_centers = [
    (-2.8806677429384724, 2.932613065721629, 0.0),
    (2.921284185918296, 2.91954201739466, 0.0),
    (-2.9843183445513564, -2.922871293824027, 0.0),
]
robot_height = 0.32999936056071455
offset = 1.0

for idx, (cx, cy, cz) in enumerate(object_centers):
    target = (cx + offset, cy, robot_height)
            """,
            globals={
                "enumerate": enumerate,
            },
        )

    def test_binary_slice(self):
        import dis

        values = []

        self.__execute(
            """
call([0, 1, 2, 3, 4][1:4])
            """,
            globals={
                "call": values.extend,
            }
        )

        self.assertEqual([0, 1, 2, 3, 4][1:4], values)

    def __execute(self, string, **keyword_arguments):
        return run(
            self.__virtual_machine.execute_string(string, **keyword_arguments),
        )

if __name__ == '__main__':
    main()
