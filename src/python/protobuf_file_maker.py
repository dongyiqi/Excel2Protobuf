# TAP的空格数
TAP_BLANK_NUM = 4


class ProtobufFile:
    def __init__(self, protobuf_name, namespace):
        # self._protobuf_name = protobuf_name
        # 将所有的输出先写到一个list， 最后统一写到文件 buffer
        self._output = []
        # 排版缩进空格数
        self._indentation = 0
        # field number 结构嵌套时使用列表
        # 新增一个结构，行增一个元素，结构定义完成后弹出
        self._field_index_list = [1]
        # 当前行是否输出，避免相同结构重复定义
        self._is_layout = True
        # 保存所有结构的名字
        self._struct_name_list = []
        # field_index
        self._field_index = 0
        self._layout_file_header(protobuf_name, namespace)

    def _layout_file_header(self, protobuf_name, namespace):
        """生成PB文件的描述信息"""
        self._output.append("/**\n")
        self._output.append("* @file:   " + protobuf_name + "\n")
        self._output.append("* @author: dongyiqi <dongyiqi @ Triniti Interactive Limited>\n")
        self._output.append("* @brief:  这个文件是通过工具自动生成的，建议不要手动修改\n")
        self._output.append("*/\n")
        self._output.append("""syntax = "proto3";\n""")
        self._output.append("\n")

        self._output.append("package %s;\n" % (namespace if namespace is not None else "TrinitiData"))

    def _get_add_field_index(self):
        self._field_index += 1
        return self._field_index

    def layout_struct_field(self, field_type, field_name, comment):
        self._output.append(" " * self._indentation + "/** " + comment + " */\n")
        self._output.append(" " * self._indentation + field_type
                            + " " + field_name + " = " + str(self._get_add_field_index()) + ";\n")

    def increase_indentation(self):
        # 增加缩进
        self._indentation += TAP_BLANK_NUM

    def decrease_indentation(self):
        # 减少缩进
        self._indentation -= TAP_BLANK_NUM

    def layout_struct_head(self, struct_name):
        self._field_index = 0
        # 生成结构头
        self._output.append("\n")
        self._output.append(" " * self._indentation + "message " + struct_name + "{\n")

    def layout_struct_tail(self):
        # 生成结构尾
        self._output.append(" " * self._indentation + "}\n")
        self._output.append("\n")

    def laytout_sheets(self, workbook_name, sheet_names):
        # 定义总入口
        self._output.append("message " + workbook_name + "_Data {\n")
        index = 0
        for sheet_name in sheet_names:
            index += 1
            # self._output.append("   repeated %s %s_items = %d;\n" % (sheet_name, sheet_name, index))
            self._output.append("   map<uint32,  %s> %s_items = %d;\n" % (sheet_name, sheet_name, index))
        self._output.append("\n}\n")
    """"
    def layout_array(self, sheet_name):
        # 输出数组定义
        self._output.append("message " + sheet_name + "_Data {\n")
        self._output.append("    repeated " + sheet_name + " items = 1;\n}\n")
        # self._output.append("message " + sheet_name + "_Data {\n")
        # self._output.append("    map<uint32, " + sheet_name + "> items = 1;\n}\n")
    """

    def write2file(self, write_path):
        # 输出到文件
        pb_file = open(write_path, "w+")
        pb_file.writelines(self._output)
        pb_file.close()
