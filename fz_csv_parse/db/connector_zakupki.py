from datetime import datetime
from typing import Dict
import psycopg2 as db
from db.connector import Connector, ConStr
from other.log_store import LogsFile


class ConnectorZakupki:

    def __init__(self):
        self.con_str = ConStr(server='127.0.0.1', db_name='db_zakupki', username='postgres',
                              password='qqqq1111')
        self.logs = LogsFile(name_logs='ConDb')

    def get_list_contract(self):
        q_text = 'select * from contract'
        # val = (id_u, )

        is_successfully, results, rowcount, err_text = Connector.execute(self.con_str, q_text)
        if is_successfully:
            return results
        else:
            print(err_text + ' [get_list_contract]')
            return []

    def insert_contract(self, id, number, dt, deadline, subject, okpd_code, okpd_name, cost, execution_period):
        q_text = 'insert into contract (id, number, dt, deadline, subject, okpd_code, okpd_name, cost, execution_period) ' \
                 'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        val = (id, number, dt, deadline, subject, okpd_code, okpd_name, cost, execution_period)
        is_successfully, results, rowcount, err_text = Connector.execute(self.con_str, q_text, val)
        if not is_successfully:
            self.logs.write_line(err_text + ' [insert_contract, id_u:' + str(id) + ']')
        return is_successfully

    def insert_list_contract(self, list_values):
        q_text = 'insert into contract (id, number, dt, deadline, subject, okpd_code, okpd_name, cost, execution_period) ' \
                 'values '
        val = ()
        for v in list_values:
            q_text += ' (%s, %s, %s, %s, %s, %s, %s, %s, %s), '
            val += (v['id'], v['number'], v['dt'], v['deadline'], v['subject'], v['okpd_code'],
                    v['okpd_name'], v['cost'], v['execution_period'])
        is_successfully, results, rowcount, err_text = Connector.execute(self.con_str, q_text.strip(', '), val)
        if not is_successfully:
            self.logs.write_line(err_text + ' [insert_contract, id_u:' + str(id) + ']')
        return is_successfully
