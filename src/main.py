import sys
import os

def main():
    # Проверка количества аргументов командной строки
    if len(sys.argv) != 2:
        print("Ошибка! Укажите путь к папке")
        print("Использование: python main.py путь к нужной папке")
        sys.exit(1)

    # Получаем путь из аргументов командной строки
    folder_path = sys.argv[1]

    # Проверка существования пути
    if not os.path.exists(folder_path):
        print(f"Ошибка: путь '{folder_path}' не существует.")
        sys.exit(1)

    # Проверяем, что это папка, а не файл
    if not os.path.isdir(folder_path):
        print(f"Ошибка: '{folder_path}' — не является папкой.")
        sys.exit(1)

    print(f"Успешный старт программы. Выбранная папка: {folder_path}")
    list_directory(folder_path)

def list_directory(path, indent_level=0):
    indent = "  " * indent_level  # отступ: 2 пробела на уровень для визуализации вложенности

    try:
        entries = os.listdir(path)
    except PermissionError:
        print(f"{indent}[Нет доступа к содержимому]")
        return
    except FileNotFoundError:
        print(f"{indent}[Папка не найдена]")
        return
    except OSError as e:
        print(f"{indent}[Ошибка доступа: {e}]")
        return

    entries.sort()  # Сортировка в алфавитном порядке

    for entry in entries:
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            # Вывод Папки. Папки помечаются слэшем 
            print(f"{indent}{entry}/")
            list_directory(full_path, indent_level + 1)
        else:
            # Вывод файл
            print(f"{indent}{entry}")

if __name__ == "__main__":
    main()