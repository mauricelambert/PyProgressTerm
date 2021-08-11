#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implement customizable progress bar and rotating animations
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""This package implement customizable progress bar and rotating animations."""

__version__ = "0.0.2"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = (
    "This package implement customizable progress bar and rotating animations."
)
__license__ = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/PyProgressTerm"

copyright = """
PyProgressTerm  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
license = __license__
__copyright__ = copyright

print(copyright)

__all__ = ["Progress"]

from argparse import ArgumentParser, Namespace
from textwrap import shorten
from time import sleep, time
import asyncio
import sys
import os

if os.name == "nt":
    os.system(
        "reg add HKEY_CURRENT_USER\\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x00000001 /f > nul"
    )


class Progress:

    """This class implement customizable progress bar and rotating animations."""

    rotating_characters = ["\\", "-", "/", "|"]
    rotating_characters_length = 4

    def __init__(self):

        self.length = 0
        self.running = True
        self.start = time()

    def progress_bar(
        self,
        step: int,
        progress_length: int = 50,
        line_length: int = 10,
        text: str = "",
        empty_char: str = " ",
        progress_char: str = "\u2588",
        first_delimiter: str = "|",
        last_delimiter: str = "|",
        total: int = 100,
        placeholder: str = "...",
    ) -> None:

        """This function implement a customizable progress bar.

        progress_char and empty_char must be a character.

        text is a short description of the step.

        line_length is the max text length."""

        pourcent = round(abs(step) / total * 100)
        position = round(pourcent / 100 * progress_length)

        if pourcent > 100:
            raise ValueError(f"step ({step}) is greater than total ({total})")

        text = shorten(text, width=line_length, placeholder=placeholder)

        back = "\b" * self.length
        cleanner = " " * self.length
        bar = f"{{0:{empty_char}<{progress_length}}}".format(progress_char * position)
        current_string = (
            f"{first_delimiter}{bar}{last_delimiter} {step}/{total} {pourcent}% {text}"
        )

        self.length = len(current_string)

        print(f"{back}{cleanner}{back}{current_string}", end="")
        sys.stdout.flush()

    def thread_infinity_run(
        self,
        function_name: str = "progress_bar",
        total: int = 100,
        wait: int = 0.05,
        **kwargs,
    ) -> None:

        """This function implement an infinity progress bar (for thread)."""

        counter = 0
        while self.start:
            counter += 1

            if counter > total:
                counter = 0

            sleep(wait)
            getattr(self, function_name)(counter, total=total, **kwargs)

    async def async_infinity_run(
        self,
        function_name: str = "progress_bar",
        total: int = 100,
        wait: int = 0.05,
        **kwargs,
    ) -> None:

        """This function implement an infinity progress bar (for asynchronous)."""

        counter = 0
        while self.start:
            counter += 1

            if counter > total:
                counter = 0

            await asyncio.sleep(wait)
            getattr(self, function_name)(counter, total=total, **kwargs)

    def timed_progress_bar(
        self,
        *args,
        function_name: str = "progress_bar",
        first_delimiter: str = "|",
        **kwargs,
    ) -> None:

        """This function implement a timed probress bar."""

        current = time() - self.start
        minutes = round(current // 60)
        seconds = round(current % 60)

        if minutes < 10:
            minutes = f"0{minutes}"

        if seconds < 10:
            seconds = f"0{seconds}"

        first_delimiter = f"{minutes}:{seconds} {first_delimiter}"
        getattr(self, function_name)(*args, first_delimiter=first_delimiter, **kwargs)

    def colored_progress_bar(
        self,
        *args,
        foreground: str = "default",
        background: str = "default",
        function_name: str = "progress_bar",
        first_delimiter: str = "|",
        last_delimiter: str = "|",
        **kwargs,
    ) -> None:

        """This function implement a colored progress bar.

        Colors must be black, red, green, yellow, blue,
        magenta, cyan gray or default."""

        colors = {
            "black": "0",
            "red": "1",
            "green": "2",
            "yellow": "3",
            "blue": "4",
            "magenta": "5",
            "cyan": "6",
            "gray": "7",
            "default": "9",
        }

        if foreground not in colors.keys():
            raise ValueError(
                f"foreground ({foreground}) must be a value in {list(colors.keys())}"
            )

        if background not in colors.keys():
            raise ValueError(
                f"background ({background}) must be a value in {list(colors.keys())}"
            )

        first_delimiter = (
            f"\x1b[3{colors[foreground]}m\x1b[4{colors[background]}m{first_delimiter}"
        )
        last_delimiter = f"{last_delimiter}\x1b[39m\x1b[49m"

        getattr(self, function_name)(
            *args,
            first_delimiter=first_delimiter,
            last_delimiter=last_delimiter,
            **kwargs,
        )

    @staticmethod
    def get_rotation(step: int) -> str:

        """This function return the character for rotating animations."""

        return Progress.rotating_characters[step % Progress.rotating_characters_length]

    def rotating_progress_bar(
        self, step: int, *args, function_name: str = "progress_bar", **kwargs
    ) -> None:

        """This function implement a rotating animation in the progress bar."""

        kwargs.update({"progress_char": self.get_rotation(step)})
        getattr(self, function_name)(step, *args, **kwargs)

    def rotating_animation(
        self,
        step: int,
        line_length: int = 10,
        title: str = "Progress...",
        text: str = "",
        total: int = 100,
        placeholder: str = "...",
    ) -> None:

        """This function implement a rotating animation."""

        pourcent = round(abs(step) / total * 100)

        if pourcent > 100:
            raise ValueError(f"step ({step}) is greater than total ({total})")

        text = shorten(text, width=line_length, placeholder=placeholder)
        back = "\b" * self.length
        cleanner = " " * self.length
        current_string = (
            f"{title} {Progress.get_rotation(step)} {step}/{total} {pourcent}% {text}"
        )

        self.length = len(current_string)

        print(f"{back}{cleanner}{back}{current_string}", end="")
        sys.stdout.flush()


def test():

    """This function test the Progess class (comment
    and uncomment lines to test all functions)."""

    from random import sample
    from string import digits
    from itertools import permutations

    random_ = sample(digits, 10)
    progress = Progress()

    bar, empty = "\u2588", " "
    progress.thread_infinity_run(
        function_name="rotating_animation",
        total=150,
        wait=0.2,
        title="Running...",
        line_length=20,
        text="bruteforce attack is running.",
    )

    for i, string in enumerate(permutations(random_, 4)):
        i %= 151

        sleep(0.2)
        progress.rotating_progress_bar(
            i,
            text=f'[{" ".join(string)} ' * 2,
            line_length=12,
            placeholder="]...",
            progress_length=50,
            empty_char=empty,
            progress_char=bar,
            first_delimiter="Progress... |",
            total=150,
            function_name="colored_progress_bar",
            background="default",
            foreground="green",
        )
        progress.timed_progress_bar(
            i,
            text=f'[{" ".join(string)} ' * 2,
            line_length=12,
            placeholder="]...",
            progress_length=50,
            empty_char=empty,
            progress_char=bar,
            first_delimiter="Progress... |",
            total=150,
        )
        progress.rotating_animation(
            i,
            line_length=12,
            title="Rotating...",
            text=f'[{" ".join(string)} ' * 2,
            placeholder="]...",
            total=150,
        )


def parse_args() -> Namespace:

    """This function parse command line arguments."""

    parser = ArgumentParser()
    parser.add_argument(
        "--foreground-color",
        "-c",
        help="Progress bar color.",
        choices={"blue", "red", "black", "green", "yellow", "magenta", "cyan", "gray"},
    )
    parser.add_argument(
        "--background-color",
        "-C",
        help="Background color of the progress bar.",
        choices={"blue", "red", "black", "green", "yellow", "magenta", "cyan", "gray"},
    )
    parser.add_argument(
        "--mode",
        "-m",
        help="Progress bar mode.",
        choices={"timed", "rotating", "colored"},
    )
    parser.add_argument(
        "--rotating",
        "-r",
        help="Rotating animation only, no progress bar.",
        action="store_true",
    )
    parser.add_argument(
        "--size", "-s", help="Size of the progress bar.", type=int, default=50
    )
    parser.add_argument(
        "--total-step", "-t", help="Number of steps.", type=int, default=150
    )
    parser.add_argument(
        "--first-delimiter",
        "-f",
        help="First delimitier of the progress bar.",
        default="|",
    )
    parser.add_argument(
        "--last-delimiter",
        "-l",
        help="Last delimitier of the progress bar.",
        default="|",
    )
    parser.add_argument(
        "--progress-character", "-p", help="Progress bar character.", default="\u2588"
    )
    parser.add_argument(
        "--empty-character",
        "-e",
        help="Empty character (in the progress bar).",
        default=" ",
    )
    parser.add_argument(
        "--text", "-T", help="Short description of a step.", default="Progress..."
    )
    parser.add_argument(
        "--text-length",
        "-L",
        help="Max length for the description (using textwrap).",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--placeholder", "-P", help="Placeholder for wrapped text.", default="..."
    )
    parser.add_argument(
        "--step-time", "-i", help="Time of steps.", type=float, default=0.2
    )
    return parser.parse_args()


def main() -> None:

    """This function execute this file from the command line."""

    from contextlib import suppress

    arguments = parse_args()

    kwargs = {
        "wait": arguments.step_time,
        "total": arguments.total_step,
        "text": arguments.text,
        "line_length": arguments.text_length,
        "placeholder": arguments.placeholder,
    }

    if arguments.rotating:
        kwargs["function_name"] = "rotating_animation"

    else:
        kwargs["progress_length"] = arguments.size
        kwargs["first_delimiter"] = arguments.first_delimiter
        kwargs["last_delimiter"] = arguments.last_delimiter
        kwargs["progress_char"] = arguments.progress_character
        kwargs["empty_char"] = arguments.empty_character

        if arguments.mode == "timed":
            kwargs["function_name"] = "timed_progress_bar"
        elif arguments.mode == "rotating":
            kwargs["function_name"] = "rotating_progress_bar"
        elif arguments.mode == "colored":
            kwargs["function_name"] = "colored_progress_bar"

            if arguments.foreground_color:
                kwargs["foreground"] = arguments.foreground_color
            if arguments.background_color:
                kwargs["background"] = arguments.background_color

    progress = Progress()
    with suppress(KeyboardInterrupt):
        progress.thread_infinity_run(**kwargs)


if __name__ == "__main__":
    main()
    sys.exit(0)
