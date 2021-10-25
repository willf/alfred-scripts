#!/usr/bin/env python3
# -*- coding: utf-8 -*-p
import clipboard
import sys

#
# Converts text in clipboard to small caps
#

CONVERSION_TABLE = {
    "a": "ᴀ",
    "b": "ʙ",
    "c": "ᴄ",
    "d": "ᴅ",
    "e": "ᴇ",
    "f": "ꜰ",
    "g": "ɢ",
    "h": "ʜ",
    "i": "ɪ",
    "j": "ᴊ",
    "k": "ᴋ",
    "l": "ʟ",
    "m": "ᴍ",
    "n": "ɴ",
    "o": "ᴏ",
    "p": "ᴘ",
    "q": "ǫ",
    "r": "ʀ",
    "s": "ꜱ",
    "t": "ᴛ",
    "u": "ᴜ",
    "v": "ᴠ",
    "w": "ᴡ",
    "x": "x",  # Not a real small cap
    "y": "ʏ",
    "z": "ᴢ",
}


def convert_char(char):
    return CONVERSION_TABLE.get(char) or char


def convert(text):
    return "".join(convert_char(char) for char in text.lower())


def clipboard_main():
    to_convert = clipboard.paste()
    clipboard.copy(convert(to_convert.lower()))


def main():
    sys.stdout.write(convert(sys.stdin.read()))


import unittest


class TestSmallCaps(unittest.TestCase):
    def test_lower_small_caps(self):
        text = "abcdefghijklmnopqrstuvwxyz!"
        match = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ!"
        for i in range(len(text)):
            self.assertEqual(convert(text[i]), match[i])

    def test_upper_small_caps(self):
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!"
        match = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ!"
        for i in range(len(text)):
            self.assertEqual(convert(text[i]), match[i])

    def test_simple_text(self):
        text = "Hello World!"
        match = "ʜᴇʟʟᴏ ᴡᴏʀʟᴅ!"
        for i in range(len(text)):
            self.assertEqual(convert(text[i]), match[i])


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
