#!/usr/bin/env python3
import re
import sys
import clipboard

HEADER_RE = r"\s*(:?)(-+)(:?)\s*"
SEPARATOR_RE = r"\s*\|\s*"


def convert(
    text,
    seperator=r" | ",
    prefix=None,
    postfix=None,
):
    lines = text.split("\n")
    rows = list(
        map(
            lambda line: split_text(line, prefix, postfix),
            lines,
        )
    )
    column_widths = find_column_widths(rows)
    new_rows = list(map(lambda row: reformat_row(row, column_widths), rows))
    return (
        "\n".join(
            list(map(lambda cells: seperator.join(cells).strip(), new_rows))
        ).strip()
        + "\n"
    )


def split_text(line, prefix, postfix):
    left_re = r"^" + (prefix or "")
    right_re = (postfix or "") + r"$"
    stripped = re.sub(left_re, "", re.sub(right_re, "", line))
    return list(map(lambda x: x.strip(), re.split(SEPARATOR_RE, stripped)))


def reformat_row(row, column_widths):
    return list(map(lambda tup: reformat_cell(tup, column_widths), enumerate(row)))


def is_header_cell(cell):
    m = re.match(HEADER_RE, cell)
    if m:
        return m.groups()
    return False


def reformat_cell(tup, column_widths):
    i = tup[0]
    cell = tup[1]
    m = is_header_cell(cell)
    if i < len(column_widths):
        width = column_widths[i]
        if m:
            lft, mid, rgt = m
            mid = mid[0]
            return lft + mid * (width - len(lft) - len(rgt)) + rgt
        return cell.ljust(width)
    return cell


def column_width(cell):
    if is_header_cell(cell):
        return 0
    return len(cell.strip())


def find_column_widths(rows):
    row = rows[0]
    initial = [column_width(col) for col in row]
    for row in rows[1:]:
        for i, cell in enumerate(row):
            width = column_width(cell)
            if i < len(initial) and width > initial[i]:
                initial[i] = width
    return initial


def clipboard_main():
    clipboard.copy(convert(clipboard.paste()))


def main():
    sys.stdout.write(convert(sys.stdin.read()))


# Unit tests

import unittest
import textwrap


class TestReformat(unittest.TestCase):
    def test_column_width(self):
        self.assertEqual(column_width(""), 0)
        self.assertEqual(column_width("----"), 0)
        self.assertEqual(column_width(" ----: "), 0)
        self.assertEqual(column_width(" BOB "), 3)
        self.assertEqual(column_width(" BOB"), 3)
        self.assertEqual(column_width("BOB "), 3)

    def test_reformat_cell(self):
        tup = (0, " -----------: ")
        self.assertEqual(reformat_cell(tup, [6]), "-----:")

    def test_reformat_markdown_table(self):
        test = textwrap.dedent(
            """\
            | Header | Header 2 | Header 3          |
            | ------ | ---------------------------: | ---- |
            | one    | two      | three three three |
            """
        )
        expected = textwrap.dedent(
            """\
            | Header | Header 2 | Header 3          |
            | ------ | -------: | ----------------- |
            | one    | two      | three three three |
            """
        )
        self.assertEqual(convert(test), expected)

    def test_reformat_interlinear_text(self):
        test = textwrap.dedent(
            """\
            \sr ὁ | δέ | κουφὀnους | ἐστὶν | •
            \lm he | and | empty-headed | he is | ;
            \gt d-msn | P | a-mss | v-3sp | ;
            """
        )
        expected = textwrap.dedent(
            """\
            \sr ὁ     | δέ  | κουφὀnους    | ἐστὶν | •
            \lm he    | and | empty-headed | he is | ;
            \gt d-msn | P   | a-mss        | v-3sp | ;
            """
        )
        self.assertEqual(convert(test), expected)


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
