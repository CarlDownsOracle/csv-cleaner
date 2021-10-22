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
        decimal = Decimal(value)
        return abs(decimal)
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

        unique_id = 1
        for row in csv_reader:

            print(row)

            key = row.get("Material") + "." + row.get("Customer") + "." + row.get("ABS")
            credit = convert(row.get('Credit'))
            debit = convert(row.get('Debit'))
            row['c_credit'] = credit
            row['c_debit'] = debit

            print(key)

            comparable_row = identifiers.get(key)

            if comparable_row is None:
                comparable_row = []
                identifiers[key] = comparable_row
                comparable_row.append(row)

            # Look at what is in the comparable row now
            # if I have a opposing entry, then go ahead and
            # remove it, add to the discarded list now
            # comparable_row.append(row)

            else:
                row_credit = row.get('c_credit')
                row_debit = row.get('c_debit')

                for idx2, target in enumerate(comparable_row):

                    if target.get('marker') is not None:
                        continue

                    target_credit = target.get('c_credit')
                    target_debit = target.get('c_debit')

                    if row_credit == target_debit and row_debit == target_credit:
                        target['marker'] = str(unique_id)
                        row['marker'] = str(unique_id)
                        unique_id += 1
                        break

                comparable_row.append(row)



        print (identifiers)

        discarded_rows = []
        kept_rows = []

        for key, comparable_row in identifiers.items():
            for idx1, comparable_entry in enumerate(comparable_row):
                if comparable_entry.get('marker') is not None:
                    discarded_rows.append(comparable_entry)
                else:
                    kept_rows.append(comparable_entry)

        output_to_file(discarded_rows,"discarded.csv")
        output_to_file(kept_rows,"kept.csv")


def output_to_file(output_rows, filename):
    try:

        if len(output_rows) > 0:
            columns = output_rows[0].keys()

            with open(filename, 'w', newline='') as csv_file_out:
                writer = csv.DictWriter(csv_file_out, fieldnames=columns)
                writer.writeheader()
                for key in output_rows:
                    writer.writerow(key)

    except IOError:
        print("I/O error")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filter_csv("test.csv")
    # filter_csv("test2.csv")
