from tkinter import *
from tkinter import filedialog as fd


class ReaderFile:

    @staticmethod
    def get_file_name():
        root = Tk()
        root.withdraw()
        name_f = fd.askopenfilename(filetypes=(("csv files", "*.csv"), ("txt files", "*.txt"), ("all files", "*.*")))
        root.destroy()
        return name_f

    @staticmethod
    def read_big_file(file_object):
        while True:
            line_current = file_object.readline()
            if not line_current:
                break
            yield line_current.strip()

    @staticmethod
    def read_file(fname, separator=';'):
        i = 1
        h_arr = []
        result = []
        with open(fname, encoding='utf-8-sig') as f_read:
            for line in f_read:
                if line:
                    if i == 1:
                        h_arr = line.rstrip().split(separator)
                    else:
                        arr = line.rstrip().split(separator)
                        x = {}
                        for el in range(0, len(h_arr)):
                            x[h_arr[el]] = arr[el]
                        result.append(x)
                    i += 1
        print('read ', len(result), ' line from file ', fname)
        return result
