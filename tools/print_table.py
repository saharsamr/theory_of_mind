from prettytable import PrettyTable


def print_table(field_names, rows):

    tbl = PrettyTable()
    tbl.field_names = field_names

    for row in rows:
        tbl.add_row(row)

    print(tbl)
