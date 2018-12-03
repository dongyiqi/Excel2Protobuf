from excel_interpreter import WorkbookInterperter
from Utils import makedir

import sys
import time


# 参数1 输入excel文件路径 参数2 导出目录
if __name__ == '__main__':
    print("start")
    start_time = time.time()

    src_path = sys.argv[1]
    out_path = sys.argv[2]
    out_protos_path = "%s/protos/" % out_path
    makedir(out_path)
    makedir(out_protos_path)

    excel_interpreter = WorkbookInterperter(src_path, out_protos_path)
    # excel_interpreter.interpreter()

    # inPath = sys.argv[0]
    print("time eplased %.2f" %(time.time()-start_time))
