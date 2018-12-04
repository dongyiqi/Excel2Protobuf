# after .proto and autogenerated_pb2.py created.
# reflect all attributes from autogenerated_pb2.py and fill the data.
# Create data.bin file

import xlrd
import os
import sys


class WorkbookParser:
    def __init__(self, excel_file_path, protos_python_path):
        (excel_file_dir, excel_file_name_withext) = os.path.split(excel_file_path)
        (self._excel_file_name, excel_file_name_ext) = os.path.splitext(excel_file_name_withext)
        self._module_name = self._excel_file_name + "_pb2"
        self._sheer_parser = []
        # load excel file
        try:
            self._workbook = xlrd.open_workbook(excel_file_path)
        except Exception as e:
            print("open xls file(%s) failed! error:%s" % (excel_file_path, e))
            raise
        # load python file
        try:
            # sys.path.append(os.getcwd())
            sys.path.append(protos_python_path)
            exec('from ' + self._module_name + ' import *')
            self._module = sys.modules[self._module_name]
        except Exception as e:
            print("load module(%s) failed! error:%s " % (self._module_name, e))
            raise

        try:
            for sheet in self._workbook.sheets():
                self._sheer_parser.append(SheetParser(self._module, sheet).parse())
        except Exception as e:
            print("open sheet file(%s) failed! errror:%s" % (excel_file_path, e))
            raise


DATA_ROW_START = 3
# assert first column must be the id col
# ID_COLUMN_INDEX = 0
FIELD_NAME_ROW = 0
FIELD_TYPE_ROW = 1
FIELD_COMMENT_ROW = 2


class SheetParser:
    def __init__(self, module, sheet):
        self._module = module
        self._sheet = sheet
        self._row_count = len(self._sheet.col_values(0))
        self._col_count = len(self._sheet.row_values(0))

    def parse(self):
        print("parse sheet ", self._sheet.name)
        item_map = getattr(self._module, self._sheet.name + '_Data')()
        for cur_row in range(DATA_ROW_START, self._row_count):
            item = item_map.items.add()
            self._parse_row(item, cur_row)

        print(str(item_map))
        return self

    def _parse_row(self, item, cur_row):
        for column_index in range(0, self._col_count):
            field_name = self._sheet.cell_value(FIELD_NAME_ROW, column_index)
            if field_name.startswith('#'):
                continue
            field_type = self._sheet.cell_value(FIELD_TYPE_ROW, column_index)
            field_value = self._sheet.cell_value(cur_row, column_index)
            self._set_item_field(item, field_name, field_type, field_value)
            # print(field_name, field_strong_value)

    def _set_item_field(self, item, field_name, field_type, field_value):
        is_repeated = False
        if field_type.startswith("repeated"):
            field_type = field_type.split(' ')[1]
            is_repeated = True
        if is_repeated:
            value_array = []
            splited_values = field_value.split('|')
            for splited_value in splited_values:
                field_strong_value = self._get_field_strong_value_single(field_type, splited_value)
                if field_strong_value is not None:
                    item.__getattribute__(field_name).append(field_strong_value)
        else:
            field_strong_value = self._get_field_strong_value_single(field_type, field_value)
            if field_strong_value is not None:
                item.__setattr__(field_name, field_strong_value)


    @staticmethod
    def _get_field_strong_value_single(field_type, field_value):
        try:
            if field_type == "int32" or field_type == "int64"\
                    or field_type == "uint32" or field_type == "uint64"\
                    or field_type == "sint32" or field_type == "sint64"\
                    or field_type == "fixed32" or field_type == "fixed64"\
                    or field_type == "sfixed32" or field_type == "sfixed64":
                        if len(str(field_value).strip()) <= 0:
                            return None
                        else:
                            return int(field_value)
            elif field_type == "double" or field_type == "float":
                    if len(str(field_value).strip()) <= 0:
                        return None
                    else:
                        return float(field_value)
            elif field_type == "string":
                field_value = field_value
                if len(str(field_value)) <= 0:
                    return None
                else:
                    return str(field_value)
            elif field_type == "bytes":
                field_value = field_value.encode('utf-8')
                if len(field_value) <= 0:
                    return None
                else:
                    return field_value
            else:
                return None
        except Exception as e:
            print("please check it, maybe type is wrong. e:%s" % e)
            raise


