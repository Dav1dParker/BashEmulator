from zipfile import ZipFile
import sys

"""
ДЗ №1. Эмулятор командной строки
Разработать эмулятор командной строки vshell.
В качестве аргумента vshell принимает образ файловой системы известного формата (tar, zip).

Обратите внимание: программа должна запускаться прямо из командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя.
В vshell должны поддерживаться команды pwd, ls, cd и cat.
Ваша задача сделать работу vshell как можно более похожей на сеанс bash в Linux.
Реализовать vshell можно на Python или других ЯП, но кроссплатформенным образом.
"""






def slash_cut(path):
    for letter in path:
        if letter == "/":
            path = path[1:]
        else:
            break
    return path


def ls(path, files):
    path = slash_cut(path)
    for file in files:
        if path in file.filename:
            file_names = file.filename[len(path):].split("/")
            file_names = list(filter(None, file_names))
            if len(file_names) > 1 or not file_names:
                continue
            print(file_names[0])


def cd(path, extension_path, files):
    if "root:" in extension_path:
        path = extension_path[len("root:"):]
    else:
        path += "/" + extension_path
    path = slash_cut(path)

    global local_path
    if path == "":
        local_path = ""
        return True

    if "../" in path:
        path = path[path.find("../") + 3:]
        if len(path) == 0:
            local_path = local_path[:len(local_path) - len(local_path.split("/")[-1]) - 1]
            return True
        else:
            local_path = local_path[:len(local_path) - len(local_path.split("/")[-1]) - 1]
            cd(local_path, path, all_files)
            return True
    for file in files:
        if (path + '/') == file.filename:
            local_path = "/" + path
            return True
    return False


def cat(path, extension_path, zip_file):
    backpath = path
    if "root:" in extension_path: 
        path = extension_path[len("root:"):]
    else:
        path += "/" + extension_path
    path = slash_cut(path)

    #Обработка .//
    global local_path
    back_local_path = local_path
    if "../" in path:
        path = path[path.find("../") + 2:]
        local_path = local_path[:len(local_path) - len(local_path.split("/")[-1]) - 1]
        path = slash_cut("/" if not local_path else local_path + path)

    flag = False
    for file in ZipFile(zip_file).filelist:
        if (path in file.filename) and ('.' in path) and ('.' != path):
            flag = True
            with ZipFile(zip_file) as files:
                with files.open(path, 'r') as file:
                    for line in file.readlines():
                        print(line.decode('utf8').strip())
            break
    path = backpath
    local_path = back_local_path
    if not flag:
        print("Can`t open this file")


try:
    sys.argv[1] #Указан ли zip файл
except IndexError:
    exit(0)
zipfile = ZipFile(sys.argv[1])
ROOT_PATH = "root:"
local_path = ""
command = input(ROOT_PATH + "/> ")
all_files = zipfile.filelist
flag = 0

while command != "exit":
    flag = 0
    command = command.split(" ")
    if command[0] == "pwd":
        print("  " + ROOT_PATH + ("/" if not local_path else local_path)) # ("/" if not local_path else local_path) проверка пуст ли local_path

    elif command[0] == "ls":
        ls(local_path, all_files)

    elif command[0] == "cd":
        try:
            command[1]
        except IndexError:
            print("Wrong syntax")
            flag = 1
        if flag == 0:
            if cd(local_path, command[1], all_files):
                pass
            else:
                print("The path does not exist")

    elif command[0] == "cat":
        try:
            command[1]
        except IndexError:
            print("Wrong syntax")
            flag = 1
        if flag == 0:
            cat(local_path, command[1], sys.argv[1])

    else:
        print("Unknown command")
    command = input(ROOT_PATH + ("/" if not local_path else local_path) + "> ")