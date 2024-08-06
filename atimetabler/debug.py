import os
import inspect

from colorama import Fore

DEFAULT_NEWLINE = False

def colourizer(colour: str):
    def colour_print(*args: object, newline: bool = DEFAULT_NEWLINE):
        print(colour, end='')
        print(*args, end='')
        print(Fore.RESET, end='\n' if newline else '')
    return colour_print

red = colourizer(Fore.RED)
green = colourizer(Fore.GREEN)
yellow = colourizer(Fore.YELLOW)
blue = colourizer(Fore.BLUE)
magenta = colourizer(Fore.MAGENTA)
cyan = colourizer(Fore.CYAN)
white = colourizer(Fore.WHITE)
black = colourizer(Fore.BLACK)

def debug_print(*args: object, code: int = 1):
    colours_by_code = {
        0: green,
        1: red,
    }
    stack_frame_caller = inspect.stack()[1]
    colour = colours_by_code.get(code, blue)
    parent_folder = os.path.dirname(os.path.dirname(__file__))

    caller = os.path.relpath(stack_frame_caller.filename, parent_folder)
    lineno = stack_frame_caller.lineno
    function = stack_frame_caller.function

    yellow("[ ")
    cyan(f"{caller:>30}")
    yellow(":")
    blue(str(lineno))
    yellow(" | ")
    magenta(f"{function:<20}")
    yellow(" ]: ")
    colour(*args, newline=True)