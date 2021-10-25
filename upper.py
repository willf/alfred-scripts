#!/usr/bin/env python3
# -*- coding: utf-8 -*-p
import clipboard
import sys

#
# Converts text in clipboard to upper case
#


def convert(text):
    return text.upper()


def clipboard_main():
    to_convert = clipboard.paste()
    clipboard.copy(convert(to_convert.lower()))


def main():
    sys.stdout.write(convert(sys.stdin.read()))


import unittest


class TestConvert(unittest.TestCase):
    def test_convert(self):
        text = "Hello World!"
        match = "HELLO WORLD!"
        self.assertEqual(convert(text), match)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv.pop(1)
        if action == "--test":
            unittest.main()
        elif action == "--clipboard":
            clipboard_main()
        else:
            print("Unknown action: {}".format(action))
        sys.exit(1)
    else:
        main()
