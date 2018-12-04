##
# @file:   excel_to_protobuf.py
# @author: dongyiqi @  Triniti Interactive Limited
# @brief:  export excel to protobuf
# TODO: support export to C# or C++ optionally
##
# 确保所有表格的第一列都是唯一索引
#
##
from excel_interpreter import WorkbookInterperter
from excel_parser import WorkbookParser
from Utils import makedir

import sys
import time


# 参数1 输入excel文件路径 参数2 导出目录
if __name__ == '__main__':
    print("start")
    start_time = time.time()

    src_path = sys.argv[1]
    out_path = sys.argv[2]
    makedir(out_path)

    out_protos_path = "%s/protos/" % out_path
    makedir(out_protos_path)

    out_protos_python_path = "%s/protos_python/" % out_path
    makedir(out_protos_python_path)

    out_protos_csharp_path = "%s/protos_csharp/" % out_path
    makedir(out_protos_csharp_path)

    excel_interpreter = WorkbookInterperter(src_path)
    excel_interpreter.flush(out_protos_path, out_protos_python_path, out_protos_csharp_path)

    excel_parser = WorkbookParser(src_path, out_protos_python_path)
    # inPath = sys.argv[0]
    print("time eplased %.2f" % (time.time()-start_time))
