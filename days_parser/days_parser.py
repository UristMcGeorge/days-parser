
"""
days_parser.py - test data parser project for Sainsbury's
"""

import csv
from itertools import dropwhile
import os
from pprint import pprint


days = {
    'mon': 'square',
    'tue': 'square',
    'wed': 'square',
    'thu': 'double',
    'fri': 'double',
    }  # CPython 3.6+ and Python 3.7+ dicts are ordered


class DaysParser:
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename  # location of the file to parse

    def specific(self, day, value):
        spec = days[day]
        if spec == 'double':
            return value*2
        elif spec == 'square':
            return value**2
        else:
            raise ValueError(f'Unexpected specific {spec}')

    def parse_input_row(self, row):
        parsed_row = []
        row_days = {}  # CPython 3.6+ and Python 3.7+ dicts are ordered

        for datum in row:
            d_range = datum.split('-')
            if len(d_range) == 1:
                if datum in days:
                    row_days[datum] = int(row[datum])
            elif len(d_range) == 2 and (elem in days for elem in d_range):
                days_from_start = dropwhile(lambda x: x != d_range[0], days)
                for day in days_from_start:
                    row_days[day] = int(row[datum])
                    if day == d_range[1]:
                        break
                else:  # range like fri-mon?
                    raise ValueError(f'Unexpected range {d_range}')

        for row_day in row_days:
            description = row['description']
            spec = self.specific(row_day, row_days[row_day])
            parsed_row.append({
                'day': row_day,
                'description': f'{description} {spec}',
                days[row_day]: spec,
                'value': row_days[row_day],
                })

        return parsed_row

    def parse_csv(self):
        parsed_csv = []
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                parsed_csv.append(self.parse_input_row(row))
                if len(parsed_csv) > 1:
                    raise ValueError('Expecting only one non-header line')
        return parsed_csv[0]

    def get_parsed(self):
        return self.parse_csv()

    def print_parsed(self):
        pprint(self.parse_csv())


if __name__ == '__main__':
    for filename in ('../../../csv_files/1.csv', '../../../csv_files/2.csv', '../../../csv_files/3.csv'):
        days_parser = DaysParser(filename)
        days_parser.print_parsed()
