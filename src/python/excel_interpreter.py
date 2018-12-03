import xlrd
from protobuf_file_maker import ProtobufFile
from Utils import makedir

# 这一行还表示重复的最大个数，或结构体元素数
FIELD_NAME_ROW = 0
FIELD_TYPE_ROW = 1
FIELD_COMMENT_ROW = 2


class WorkbookInterperter:
    def __init__(self, excel_file_path, out_dir):
        try:
            self._workbook = xlrd.open_workbook(excel_file_path)
            self._sheetsInterpreter = []
            for sheet in self._workbook.sheets():
                self._sheetsInterpreter.append(SheetInterpreter(sheet))
        except BaseException:
            print("open xls file(%s) failed!" % excel_file_path)
            raise

        for sheetInterpreter in self._sheetsInterpreter:
            sheetInterpreter.interpreter()
            sheetInterpreter.write2file(out_dir)


class SheetInterpreter:
    def __init__(self, sheet):
        self._sheet = sheet
        self._protofile = ProtobufFile(sheet.name)
        self._row_count = len(self._sheet.col_values(0))
        self._col_count = len(self._sheet.row_values(0))
        # print("sheetname:%s rowcount:%d colcount:%d" % (self._sheet.name, self._row_count, self._col_count))

    def write2file(self, write_dir):
        file_path = ("%s%s.proto" % (write_dir, self._sheet.name))
        # print("path:%s" % file_path)
        self._protofile.write2file(file_path)

    def interpreter(self):
        # print("interpreter sheet:%s" % self._sheet.name)
        self._protofile.layout_file_header()
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
        if not self._verify_field_type(field_type):
            print("unknow field type:%s" %field_type)
        # skip the field name started with symbol #
        if field_name.startswith('#'):
            return
        self._protofile.layout_struct_field(field_type, field_name, field_comment)

    @staticmethod
    def _verify_field_type(field_type):
        if field_type == "int32" or field_type == "int64" \
                or field_type == "uint32" or field_type == "uint64" \
                or field_type == "sint32" or field_type == "sint64" \
                or field_type == "fixed32" or field_type == "fixed64" \
                or field_type == "sfixed32" or field_type == "sfixed64" \
                or field_type == "float" or field_type == "double"\
                or field_type == "string" or field_type == "bytes":
            return True
        else:
            print("unexpected field type:%s" % field_type)
            return False
