import sys
import os

def main():
    # Проверка количества аргументов командной строки
    if len(sys.argv) != 2:
        print("Ошибка! Укажите путь к папке")
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

if __name__ == "__main__":
    main()