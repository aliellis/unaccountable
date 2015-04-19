from prettytable import PrettyTable


def validate_columns(t_data):
    # PrettyTable will error if columns have varying lengths, this adds
    # whitespace to equal column lengths
    col_length = max(len(v) for k, v in t_data.iteritems())
    for col_data in t_data:
        while len(t_data[col_data]) < col_length:
            t_data[col_data].append("")
    return t_data


def generate_table(dict):
    table = PrettyTable()
    for key in dict:
        col = dict[key]
        table.add_column(key, dict[key])
    table.align = "l"
    return table
