import xlrd
import sys
import os


class ExcelInterpreter:
    def __init__(self, xls_file_path):
        try :
            self._xls_file_path = xls_file_path
            self._workbook = xlrd.open_workbook(self._xls_file_path)
            self._sheets = self._workbook.sheet_names()
            print(self._sheets)
        except BaseException as e:
            print("open xls file(%s) failed!" % self._xls_file_path)
            raise Exception(e)


    def interpreter(self):
        print("interpreter")


#参数1 输入excel文件路径 参数2 导出目录
if __name__ == '__main__':
    print("main entrance")
    src_path = sys.argv[1]
    out_path = sys.argv[2]
    excel_interpreter = ExcelInterpreter(src_path)
    excel_interpreter.interpreter()

    #inPath = sys.argv[0]

