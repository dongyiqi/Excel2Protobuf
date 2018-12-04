import xlrd
import os
from protobuf_file_maker import ProtobufFile
# 这一行还表示重复的最大个数，或结构体元素数
FIELD_NAME_ROW = 0
FIELD_TYPE_ROW = 1
FIELD_COMMENT_ROW = 2


class WorkbookInterperter:
    def __init__(self, excel_file_path):
            (excel_file_dir, excel_file_name_withext) = os.path.split(excel_file_path)
            (self._excel_file_name, excel_file_name_ext) = os.path.splitext(excel_file_name_withext)
            self._protofile = ProtobufFile(self._excel_file_name)
            self._sheetsInterpreter = []

            try:
                self._workbook = xlrd.open_workbook(excel_file_path)
            except Exception as e:
                print("open xls file(%s) failed! error:%s" % (excel_file_path, e))
                raise

            try:
                for sheet in self._workbook.sheets():
                    self._sheetsInterpreter.append(SheetInterpreter(sheet, self._protofile))
            except BaseException:
                print("open xls file(%s) failed!" % excel_file_path)
                raise

            for sheetInterpreter in self._sheetsInterpreter:
                sheetInterpreter.interpreter()

    def flush(self, out_protos_path, out_protos_python_path, out_protos_csharp_path):
        self._write2file(out_protos_path)
        try:
            # protoc compile python src file
            command = "protoc -I %s --python_out=%s %s" \
                      % (out_protos_path, out_protos_python_path, self._excel_file_name + ".proto")
            os.system(command)
            # protoc compile C# src file
            command = "protoc -I %s --csharp_out=%s %s" \
                      % (out_protos_path, out_protos_csharp_path, self._excel_file_name + ".proto")
            os.system(command)
        except Exception as e:
            print("protoc failed!")
            print(e)
            raise

    def _write2file(self, write_dir):
        file_path = ("%s%s.proto" % (write_dir, self._excel_file_name))
        # print("path:%s" % file_path)
        self._protofile.write2file(file_path)


class SheetInterpreter:
    def __init__(self, sheet, protofile):
        self._sheet = sheet
        self._protofile = protofile
        self._row_count = len(self._sheet.col_values(0))
        self._col_count = len(self._sheet.row_values(0))
        # print("sheetname:%s rowcount:%d colcount:%d" % (self._sheet.name, self._row_count, self._col_count))

    def interpreter(self):
        # print("interpreter sheet:%s" % self._sheet.name)
        self._protofile.layout_struct_head(self._sheet.name)
        self._protofile.increase_indentation()

        for i in range(self._col_count):
            self._interpreter_field(i)

        self._protofile.decrease_indentation()
        self._protofile.layout_struct_tail()
        self._protofile.layout_array(self._sheet.name)

    def _interpreter_field(self, col_index):
        field_name = str(self._sheet.cell_value(FIELD_NAME_ROW, col_index)).strip()
        field_type = str(self._sheet.cell_value(FIELD_TYPE_ROW, col_index)).strip()
        field_comment = str(self._sheet.cell_value(FIELD_COMMENT_ROW, col_index)).strip()
        if field_name.startswith('#'):
            return
        if not self._verify_field_type(self._sheet.name,field_name, field_type):
            print("unknow field type:%s" % field_type)
        # skip the field name started with symbol #

        self._protofile.layout_struct_field(field_type, field_name, field_comment)

    @staticmethod
    def _verify_field_type(sheet_name, field_name, field_type):
        if field_type.startswith("repeated"):
            field_type = field_type.split(' ')[1]

        if field_type == "int32" or field_type == "int64" \
                or field_type == "uint32" or field_type == "uint64" \
                or field_type == "sint32" or field_type == "sint64" \
                or field_type == "fixed32" or field_type == "fixed64" \
                or field_type == "sfixed32" or field_type == "sfixed64" \
                or field_type == "float" or field_type == "double"\
                or field_type == "string" or field_type == "bytes"\
                or field_type == "bool":
            return True
        else:
            print("unexpected field sheet_name:%s name:%s type:%s " % (sheet_name, field_name, field_type))
            return False
