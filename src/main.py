import sys
import os

def show_help():
    print("Инструкция по запуску:")
    print("python main.py путь_к_папке фильтр")
    print()
    print("Параметры:")
    print("путь_к_папке — обязательный путь для анализа")
    print("фильтр — необязательный фильтр (по расширению или имени)")
    print()
    print("Примеры:")
    print("python main.py C:\\Users\\user - вариант без фильтра")
    print("python main.py C:\\Users\\user .txt - вариант с фильтром по расширению")
    print("python main.py C:\\Users\\user report - вариант с фильтром по имени")

def main():
    folder_path = sys.argv[1]
    filter_pattern = sys.argv[2] if len(sys.argv) > 2 else None

    # Проверка существования пути
    if not os.path.exists(folder_path):
        print(f"Ошибка: путь '{folder_path}' не существует.")
        sys.exit(1)

    # Проверяем, что это папка, а не файл
    if not os.path.isdir(folder_path):
        print(f"Ошибка: '{folder_path}' — не является папкой.")
        sys.exit(1)

    print(f"Успешный старт программы. Выбранная папка: {folder_path}")
    if filter_pattern:
        print(f"Применяется фильтр: {filter_pattern}")
    else:
        print("Фильтр не указан — отображаются все элементы.")

    stats = {
        "files": 0,
        "dirs": 0,
        "size": 0
    }

    list_directory(folder_path, filter_pattern, stats)

    print("\n--- Статистика ---")
    print(f"Папок: {stats['dirs']}")
    print(f"Файлов: {stats['files']}")
    print(f"Общий размер: {stats['size']} байт ({_format_size(stats['size'])})")


def _format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def list_directory(path, filter_pattern, stats, indent_level=0):
    indent = "  " * indent_level

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

    entries.sort()

    for entry in entries:
        full_path = os.path.join(path, entry)

        # Фильтрация
        if filter_pattern is not None:
            if filter_pattern.startswith("."):
                # Фильтр по расширению
                if not entry.lower().endswith(filter_pattern.lower()):
                    continue
            else:
                # Фильтр по подстроке в имени
                if filter_pattern.lower() not in entry.lower():
                    continue

        if os.path.isdir(full_path):
            stats["dirs"] += 1
            print(f"{indent}{entry}/")
            list_directory(full_path, filter_pattern, stats, indent_level + 1)
        else:
            stats["files"] += 1
            try:
                file_size = os.path.getsize(full_path)
                stats["size"] += file_size
                print(f"{indent}{entry} ({file_size} B)")
            except OSError:
                # Если не удалось получить размер, просто выводится имя
                print(f"{indent}{entry}")


if __name__ == "__main__":
    main()
