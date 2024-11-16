from numpy.testing.print_coercion_tables import print_cancast_table

import other.converters as converter
from other.reader import ReaderFile
from db.connector_zakupki import *



file1 = ReaderFile.get_file_name()

print('file name: ', file1)

db = ConnectorZakupki()

limit = 500

list_values = []

with open(file1, 'r', encoding='utf-8-sig') as file:
    for line in ReaderFile.read_big_file(file):
        try:
            arr_row = line.split(';')
            if len(arr_row) == 9:
                list_values.append({'id': arr_row[0],
                                            'number': arr_row[1],
                                            'dt': converter.str_to_dt(arr_row[2]),
                                            'deadline': converter.str_to_dt(arr_row[3]),
                                            'subject': arr_row[4],
                                            'okpd_code': arr_row[5],
                                            'okpd_name': arr_row[6],
                                            'cost': float(arr_row[7]),
                                            'execution_period': int(arr_row[8])})
                # print(len(list_values))
                if len(list_values) == limit:
                    db.insert_list_contract(list_values)
                    # print(result)
                    list_values = []
                    # print(datetime.now())
            else:
                print('line error', line)
        except Exception as ex:
            print('[Exception]:', ex.__repr__())

# print(db.insert_list_contract(list_values))
