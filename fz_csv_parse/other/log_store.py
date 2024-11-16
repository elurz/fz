from tkinter import *
from datetime import datetime
from tkinter import filedialog


class LogsFile(object):

    def __init__(self, name_logs='Logs', name_file='', type_file='txt', path_dir=''):
        self.path_dir = path_dir

        self.type_filelog = type_file
        if not self.type_filelog:
            self.type_filelog = 'txt'

        self.name_logs = name_logs
        if not self.name_logs:
            self.name_logs = 'Logs'

        self.name_file = name_file
        if not self.name_file:
            self.name_file = self.name_logs + '_' + datetime.now().strftime("%Y-%m-%d") \
                             + '.' + self.type_filelog.replace('.', '')

    def fullname_file(self):
        if self.path_dir:
            return self.path_dir + '/' + self.name_file
        else:
            return self.name_file

    def select_path_dir(self):
        root = Tk()
        root.withdraw()
        self.path_dir = filedialog.askdirectory()
        root.destroy()

    def write_line(self, text, with_dt: bool = True):
        with open(self.fullname_file(), 'a', encoding='utf-8-sig') as f:
            if with_dt:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S "))
            f.write(text)
            f.write('\n')

    def write(self, text):
        with open(self.fullname_file(), 'a', encoding='utf-8-sig') as f:
            f.write(text)

    def __str__(self):
        return f'{self.name_logs} {self.fullname_file()}'
