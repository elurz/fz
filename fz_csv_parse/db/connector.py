import psycopg2 as db_pg


class ConStr:
    def __init__(self, server: str = '', db_name: str = '', username: str = '', password: str = ''):
        self.server = server
        self.db_name = db_name
        self.username = username
        self.password = password


class Connector:

    @staticmethod
    def execute(con_str: ConStr, query: str, val: tuple = None):
        results = []
        rowcount: int = 0
        err_text: str = ''
        is_successfully = False
        cnx = None
        cursor = None
        try:
            cnx = db_pg.connect(user=con_str.username, password=con_str.password,
                                host=con_str.server, database=con_str.db_name)
            cursor = cnx.cursor()
            cursor.execute(query, val)
            if query.lower().startswith('select'):
                rows = cursor.fetchall()
                if rows:
                    columns = [column[0] for column in cursor.description]
                    for row in rows:
                        results.append(dict(zip(columns, row)))
                is_successfully = True
            elif query.lower().startswith('insert') or query.lower().startswith('update') \
                    or query.lower().startswith('delete'):
                cnx.commit()
                if cursor.rowcount > 0:
                    is_successfully = True
                else:
                    err_text = 'Затронуто 0 строк'
            rowcount = cursor.rowcount
        except Exception as ex:
            err_text = ex.__repr__()
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
            return is_successfully, results, rowcount, err_text
