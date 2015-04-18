from prettytable import PrettyTable

def generate_table(data):
    result_table = PrettyTable()
    column = data.values()[0]
    result_table.add_column(data.keys()[0], column)
    result_table.align = 'l'
    return result_table
