#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Table class that has a draw method. It draws (sorted and) nice table of
data. Handles unicode characters correctly.
"""

import operator
import unicodedata

__author__ = "Kimmo Brunfeldt"


class Table(object):
    """This class offers ability to nicely print a table which is in format:

    [ ["header1", "header2"],
      [1, "info1"],
      [2, "info2"]
    ]

    Element can be basically anything that can be sorted and converted
    to string.
    """
    # Characters used in drawing.
    CORNER = '+'
    HORIZONTAL = '-'
    VERTICAL = '|'

    def __init__(self, table):
        super(Table, self).__init__()

        self._headers = table.pop(0)
        # Now table contains only data, not headers.
        self._table = table
        self._column_widths = self._get_column_widths()

    def draw(self):
        """Draws a nice table of 2 dimensional list.
        First row of table is headers, following rows are data."""
        # +--+--+
        limiter = self.CORNER + \
                  self.CORNER.join([x * self.HORIZONTAL
                                   for x in self._column_widths]) + self.CORNER

        # Print headers
        print(limiter)
        self._print_row(self._headers)
        print(limiter)

        # Print the actual data
        for row in self._table:
            self._print_row(row)

        print(limiter)

    def sort_by_column(self, sort_column, reverse=False):
        self._table.sort(key=operator.itemgetter(sort_column),
                         reverse=reverse)

    # Non-public:

    def _print_row(self, row):
        """Prints row's items separated with self.VERTICAL,
        and space-padded to match max widths.
        """
        line = self.VERTICAL

        for max_width, element in zip(self._column_widths, row):

            element = self._all_to_unicode(element)
            element = self._strip_nonprintable(element)
            element = u' ' + element + u' '

            element_width = self._width_when_printed(element)
            line += element + ' ' * (max_width - element_width)
            line += self.VERTICAL

        print(line.encode('utf-8'))

    def _get_column_widths(self):
        column_widths = []

        # For each column, find the element that is the widest when printed.
        for i in range(len(self._headers)):
            column_width = max(self._width_when_printed(row[i])
                               for row in self._table)

            # Check if header is the widest.
            header_width = self._width_when_printed(self._headers[i])
            if column_width < header_width:
                column_width = header_width

            # When printed elements are padded with spaces on sides.
            extra_width = 2

            column_width += extra_width
            column_widths.append(column_width)

        return column_widths

    def _width_when_printed(self, mixed):
        """Counts text's actual width in terminal when
        fixed-width font is used. http://unicode.org/reports/tr11/ is more
        information about W and F chars."""
        text = self._all_to_unicode(mixed)
        text = self._strip_nonprintable(text)
        return sum(1 + (unicodedata.east_asian_width(c) in "WF") \
                   for c in text)

    def _strip_nonprintable(self, text):
        """Strips non-printable characters. text must be unicode."""

        # Strip ascii codes 0-31 and 127
        non = list(xrange(32)) + [127]
        return u''.join([u'' if ord(char) in non else char for char in text])

    def _all_to_unicode(self, mixed):
        """Tries to converts anything to unicode."""

        if isinstance(mixed, unicode):
            return mixed

        if not isinstance(mixed, str):
            mixed = str(mixed)

        try:
            unicodestring = mixed.decode('utf-8')

        except UnicodeDecodeError:
            try:
                unicodestring = mixed.decode('iso-8859-1')

            # Force decoding with utf-8
            except UnicodeDecodeError:
                unicodestring = mixed.decode('utf-8', 'replace')

        return unicodestring


if __name__ == '__main__':
    data = [
        ['ID', 'Person'],
        [8, 'Pál Erdős'],
        [23, 'Kurt Gödel'],
        [2, 'Évariste Galois'],
        [3, 'Guillaume de l\'Hôpital'],
        [12, '汉语漢汉语漢汉语漢汉语漢汉语漢汉语漢'],
        [0, 'ἔννεπε, μοῦσα, πολύτροπον'],
        [35, 'ὃς μάλα πολλὰ πλάγχθη'],
    ]

    table = Table(data)
    table.sort_by_column(0)
    table.draw()
