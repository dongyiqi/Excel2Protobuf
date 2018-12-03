import os


def makedir(dir2make):
    if not os.path.exists(dir2make):
        os.makedirs(dir2make)
