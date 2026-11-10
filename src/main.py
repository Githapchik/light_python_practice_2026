import sys
import os
import datetime

# счётчики для отчёта
files_count = 0
dirs_count = 0
total_size = 0

def human_size(size):
    if size < 1024:
        return str(size) + " Б"
    elif size < 1024 * 1024:
        return str(round(size / 1024, 1)) + " КБ"
    else:
        return str(round(size / 1024 / 1024, 1)) + " МБ"

def print_help():
    print("Утилита для просмотра содержимого папки")
    print("Запуск: python laba.py <путь к папке> [фильтр]")
    print("Пример: python laba.py C:\\Temp .txt")
    print("Фильтр - необязательный параметр, ищет файлы по имени (например .txt)")

def list_dir(path, level=0, filter_str=""):
    # рекурсивный обход папки
    global files_count, dirs_count, total_size

    try:
        items = os.listdir(path)
    except PermissionError:
        return  # нет доступа - просто пропускаем папку

    items.sort()

    for name in items:
        full_path = os.path.join(path, name)
        indent = "    " * level  # отступ для вложенности

        if os.path.isdir(full_path):
            dirs_count += 1
            print(indent + name + "/")
            list_dir(full_path, level + 1, filter_str)
        else:
            # если задан фильтр - показываем только подходящие файлы
            if filter_str != "" and filter_str.lower() not in name.lower():
                continue
            size = os.path.getsize(full_path)
            files_count += 1
            total_size += size
            print(indent + name + " (" + human_size(size) + ")")

def main():
    # проверяем аргументы
    if len(sys.argv) < 2:
        print("Ошибка: не указан путь к папке!")
        print()
        print_help()
        sys.exit(1)

    # справка
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print_help()
        sys.exit(0)

    path = sys.argv[1]

    # фильтр, если есть
    filter_str = ""
    if len(sys.argv) > 2:
        filter_str = sys.argv[2]

    # проверяем путь
    if not os.path.exists(path):
        print("Ошибка: такой папки не существует:", path)
        sys.exit(1)

    if not os.path.isdir(path):
        print("Ошибка: это не папка:", path)
        sys.exit(1)

    print("Содержимое папки:", os.path.abspath(path))
    if filter_str != "":
        print("Фильтр:", filter_str)
    print()

    # обход
    list_dir(path, 0, filter_str)

    # отчёт
    print()
    print("======== ОТЧЁТ ========")
    print("Папок:", dirs_count)
    print("Файлов:", files_count)
    print("Общий размер:", human_size(total_size))
    print("=======================")

    # сохраняем отчёт в txt
    report_name = "report.txt"
    with open(report_name, "w", encoding="utf-8") as f:
        f.write("Журнал работы утилиты\n")
        f.write("Дата: " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M") + "\n")
        f.write("Папка: " + os.path.abspath(path) + "\n")
        if filter_str != "":
            f.write("Фильтр: " + filter_str + "\n")
        f.write("\n")
        f.write("Папок: " + str(dirs_count) + "\n")
        f.write("Файлов: " + str(files_count) + "\n")
        f.write("Общий размер: " + human_size(total_size) + "\n")

    print()
    print("Отчёт сохранён в файл:", report_name)

if __name__ == "__main__":
    main()
