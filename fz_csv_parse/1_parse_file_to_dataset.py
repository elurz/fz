from other.reader import *
import other.converters as converter


file1 = ReaderFile.get_file_name()

print('file name: ', file1)

num_row_error = 0
num_row_ok = 0

with open(f'row_error.csv', 'a', encoding='utf-8-sig') as f_error:
    with open(f'dataset.csv', 'a', encoding='utf-8-sig') as f_result:
        with open(file1, 'r', encoding='utf-8') as file:
            f_result.write('id;number;dt;deadline;subject;okpd_code;okpd_name;cost;execution_period\n')
            for line in ReaderFile.read_big_file(file):

                line_current = line_current.strip().replace(r'\"', '').replace(';', ',').replace(r',\N,',
                                                                                                 r',"<НЕ ОПРЕДЕЛЕНО>",')
                line_current = line_current.replace(r',\N,', r',"<НЕ ОПРЕДЕЛЕНО>",')
                line_current = line_current.replace(r'","', ';').replace('"', '').replace('\xa0', '')

                arr_row = line.split(';')

                row_dict = {}

                err = False
                if len(arr_row) != 27:
                    err = True
                else:
                    row_dict = {"id" : arr_row[0],
                                "number": arr_row[1],
                                "dt": arr_row[13],
                                'deadline': arr_row[15],
                                "subject": arr_row[11],
                                "okpd_code": arr_row[26],
                                "okpd_name": arr_row[25],
                                "cost": arr_row[21],
                                "execution_period": 0}
                    if row_dict['cost'] == '<НЕ ОПРЕДЕЛЕНО>':
                        row_dict['cost'] = arr_row[20]

                    # продолжительность контракта (в днях)
                    dt_start = converter.str_to_dt(arr_row[13])
                    dt_end = converter.str_to_dt(arr_row[15])
                    if not dt_end or not dt_end:
                        err = True
                    else:
                        row_dict['execution_period'] = (dt_end - dt_start).days

                    if row_dict['subject'] == '<НЕ ОПРЕДЕЛЕНО>' or \
                        not row_dict['cost'].replace('.', '').isnumeric() or \
                        not row_dict['number'].isnumeric() or \
                        not row_dict['okpd_code'].replace('.', '').isnumeric():
                        err = True
                if err:
                    num_row_error += 1
                    f_error.write(line+'\n')
                else:
                    num_row_ok += 1
                    f_result.write(";".join(map(str, row_dict.values())) + '\n')

                if (num_row_ok + num_row_error) % 500000 == 0:
                    print('row ok ', num_row_ok)

print('count row ok ', num_row_ok, ', error ', num_row_error)
