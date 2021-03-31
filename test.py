import os


def mkd(path):
    i = 0
    while True:
        k = "打开我！最后一层啦"
        file_name = f"{path}{k}"
        os.makedirs(file_name)
        mkd(file_name + '\\')
        if i == 5:
            break
        i += 1


path = "G:\\"
mkd(path)