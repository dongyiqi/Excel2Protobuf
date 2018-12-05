##
# @file:   excel_to_protobuf.py
# @author: dongyiqi @  Triniti Interactive Limited
# @brief:  export excel to protobuf
# TODO: support export to C# or C++ optionally
##
# 确保所有表格的第一列都是唯一索引
#
# parameters
# -i --input_path input folder which contains excel files to convert.
#       This script converts all excel file from that folder
# -d --data_out folder where serialized binary protobuf file exported
# -s --csharp_out folder where auto generated C# script file(from protoc.exe) exported
# -c --cpp_out folder where auto generated C++ script file(from protoc.exe) exported
##
from excel_interpreter import WorkbookInterperter
from excel_parser import WorkbookParser
from Utils import *

import sys
import getopt
import time

temp_dir = "./_temp"
temp_proto_files_path = "%s/proto_files" % temp_dir
temp_proto_data_path = "%s/proto_data" % temp_dir
temp_autogenerated_scripts_path = "%s/autogenerated_scripts" % temp_dir


def safe_create_temp_dir():
    rmdir(temp_dir)
    makedir(temp_proto_files_path)
    makedir(temp_proto_data_path)
    makedir(temp_autogenerated_scripts_path)


def main():
    excels_dir = None
    data_out = None
    csharp_out = None
    cpp_out = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:d:s:c:-v"
                                   , ["input_path=", "data_out=", "csharp_out=", "cpp_out="])
        for o, a in opts:
            if o in ("-i", "--input_path"):
                excels_dir = a
            elif o in ("-d", "--data_out"):
                data_out = a
            elif o in ("-s", "--csharp_out"):
                csharp_out = a
            elif o in ("-c", "--cpp_out"):
                cpp_out = a
    except Exception as e:
        print("argv error:%s" % e)

    if excels_dir is None:
        print("-i --input_path excels source folder not set properly")
    #if data_out is None:
    #   print("-d --data_out export protobuf serialized data .pb folder not set properly")

    start_time = time.time()

    safe_create_temp_dir()

    excel_files2_convert = []
    for root, dirs, files in os.walk(excels_dir):
        for file in files:
            if os.path.splitext(file)[1] == ".xlsx" and not file.startswith('~$'):
                excel_files2_convert.append(excels_dir+"/"+file)

    for file in excel_files2_convert:
        export_excel2protobuff(file, data_out, csharp_out, cpp_out)

    print("time eplased %.2f" % (time.time() - start_time))


def export_excel2protobuff(xls_file_path, data_out, csharp_out, cpp_out):
    excel_interpreter = WorkbookInterperter(xls_file_path)
    excel_interpreter.interpreter()
    excel_interpreter.save(temp_proto_files_path, temp_autogenerated_scripts_path, csharp_out, cpp_out)

    # if data_out is not None:
    excel_serializer = WorkbookParser(xls_file_path, temp_autogenerated_scripts_path)
    excel_serializer.serialize(temp_proto_data_path, data_out)


# 参数1 输入excel文件路径 参数2 导出目录
if __name__ == '__main__':
    main()
