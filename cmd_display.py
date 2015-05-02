from prettytable import PrettyTable


def validate_columns(t_data):
    # PrettyTable will error if columns have varying lengths, this adds
    # whitespace to equal column lengths
    col_length = max(len(v) for k, v in t_data.iteritems())
    for col_data in t_data:
        while len(t_data[col_data]) < col_length:
            t_data[col_data].append("")
    return t_data


def generate_table(t_dict):
    table = PrettyTable()
    for key in t_dict:
        col = t_dict[key]
        table.add_column(key, t_dict[key])
    table.align = "l"
    return table


def table_contents_to_s(t_dict):
    for key in t_dict:
        t_dict[key] = [str(t_dict[key])]
    return t_dict
