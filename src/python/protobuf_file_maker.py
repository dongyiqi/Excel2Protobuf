# TAP的空格数
TAP_BLANK_NUM = 4


class ProtobufFile:
    def __init__(self, protobuf_name):
        self._protobuf_name = protobuf_name
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

    def layout_file_header(self):
        """生成PB文件的描述信息"""
        self._output.append("/**\n")
        self._output.append("* @file:   " + self._protobuf_name + "\n")
        self._output.append("* @author: dongyiqi <dongyiqi @ Triniti Interactive Limited>\n")
        self._output.append("* @brief:  这个文件是通过工具自动生成的，建议不要手动修改\n")
        self._output.append("*/\n")
        self._output.append("""syntax = "proto3";\n""")
        self._output.append("\n")
        self._output.append("package Triniti;\n")

    def increase_indentation(self):
        # 增加缩进
        self._indentation += TAP_BLANK_NUM

    def decrease_indentation(self):
        # 减少缩进
        self._indentation -= TAP_BLANK_NUM

    def layout_struct_head(self, struct_name):
        # 生成结构头
        self._output.append("\n")
        self._output.append(" " * self._indentation + "message " + struct_name + "{\n")

    def layout_struct_tail(self):
        # 生成结构尾
        self._output.append(" " * self._indentation + "}\n")
        self._output.append("\n")

    def write2file(self, write_path):
        # 输出到文件
        pb_file = open(write_path, "w+")
        pb_file.writelines(self._output)
        pb_file.close()
