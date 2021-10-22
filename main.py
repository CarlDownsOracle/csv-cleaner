# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from decimal import Decimal
from re import sub
import csv


def convert(input_string):
    try:
        value = input_string.replace(',','')
        value = value.replace('$','')
        return Decimal(value)
    except Exception as e:
        print('exception is {} input is {}'.format(e, input_string))


def is_a_discard(item):
    return item['marker'] == 'discard'


def is_a_keeper(item):
    return item['marker'] == 'keep'


def filter_csv(input_file):
    with open(input_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        identifiers = {}

        for row in csv_reader:

            print(row)

            key = row.get("Material") + "." + row.get("Customer")
            print(key)

            comparable_row = identifiers.get(key)

            if comparable_row is None:
                comparable_row = []
                identifiers[key] = comparable_row

            comparable_row.append(row)

        print (identifiers)

        for key, comparable_row in identifiers.items():

            for idx1, row in enumerate(comparable_row):

                if row.get('marker') is not None:
                    continue

                credit = convert(row.get('Credit amount'))
                debit = convert(row.get('Debit amount'))

                cancelling_entries = False
                for idx2, target in enumerate(comparable_row):

                    if target.get('marker') is not None:
                        continue

                    target_credit = convert(target.get('Credit amount'))
                    target_debit = convert(target.get('Debit amount'))

                    if credit == - target_debit and debit == - target_credit:
                        cancelling_entries = True
                        target['marker'] = 'discard'

                if cancelling_entries:
                    row['marker'] = 'discard'
                else:
                    row['marker'] = 'keep'

        discarded_rows = []
        kept_rows = []

        for key, comparable_row in identifiers.items():
            for idx1, row in enumerate(comparable_row):
                if is_a_keeper(row):
                    kept_rows.append(row)
                if is_a_discard(row):
                    discarded_rows.append(row)

        try:

            print(discarded_rows)
            if len(discarded_rows) > 0:
                columns = discarded_rows[0].keys()

                with open("discarded.csv", 'w', newline='') as csv_file_out:
                    writer = csv.DictWriter(csv_file_out, fieldnames=columns)
                    writer.writeheader()
                    for key in discarded_rows:
                        writer.writerow(key)

        except IOError:
            print("I/O error")


        try:

            print(kept_rows)
            if len(kept_rows) > 0:
                columns = kept_rows[0].keys()

                with open("kept.csv", 'w', newline='') as csv_file_out:
                    writer = csv.DictWriter(csv_file_out, fieldnames=columns)
                    writer.writeheader()
                    for key in kept_rows:
                        writer.writerow(key)

        except IOError:
            print("I/O error")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filter_csv("test2.csv")
