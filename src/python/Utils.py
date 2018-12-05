import os
import shutil


def makedir(dir2make):
    if not os.path.exists(dir2make):
        os.makedirs(dir2make)


def rmdir(dir2remove):
    if os.path.exists(dir2remove):
        shutil.rmtree(dir2remove, True)


def copyfile(src, des):
    shutil.copy(src, des)
